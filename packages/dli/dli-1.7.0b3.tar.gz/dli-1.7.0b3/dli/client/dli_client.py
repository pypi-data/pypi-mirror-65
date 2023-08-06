import datetime
import sys
from json import JSONDecodeError
from logging.handlers import RotatingFileHandler
import warnings

import jwt
import requests
import logging
import socket
from pythonjsonlogger.jsonlogger import JsonFormatter
from http.cookiejar import CookiePolicy
from wrapt import ObjectProxy
from http import HTTPStatus
from urllib.parse import urljoin, urlparse, parse_qs
from collections import defaultdict
from pathlib import Path

from dli import __version__
from dli.analytics import AnalyticsHandler
from dli.client.adapters import DLIBearerAuthAdapter, DLIAccountsV1Adapter, \
    DLIInterfaceV1Adapter
from dli.client.environments import _Environment
from dli.siren import siren_to_entity
from dli.client.components.auto_reg_metadata import AutoRegMetadata
from dli.client.components.datafile import Datafile
from dli.client.components.dataset import Dataset, Dictionary
from dli.client.components.me import Me
from dli.client.components.package import Package
from dli.client.components.search import Search
from dli.client.components.accounts import Accounts
from dli.client.exceptions import (
    DatalakeException, InsufficientPrivilegesException,
    InvalidPayloadException, UnAuthorisedAccessException,
    CatalogueEntityNotFoundException, AuthenticationFailure
)
from dli.models.paginator import Paginator
from dli.modules.dataset import DatasetModule
from dli.modules.package import PackageModule
from dli.models.dictionary import DictionaryModel
from dli.models.file import FileModel
from dli.models.instance import InstanceModel, \
    InstancesCollection as InstancesCollection_
from dli.models.package import PackageModel
from dli.models.dataset import DatasetModel
from dli.siren import PatchedSirenBuilder


class ModelDescriptor:
    """
    This class is responsible for extending the base type passed
    into the __init__ method with the instance of DliClient it has
    been created within, following the descriptor pattern.

    What this means practicably, is that under _client attribute of the 'new'
    type (class instance) there is a backreference to the DliClient,
    which then permits the type to access the shared session object of DliClient,
    rather than having to pass the session into each instance.

    Using an instance instantiated from the base type will not have the
    _client attribute available.
    """

    def __init__(self, model_cls=None):
        self.model_cls = model_cls

    def __get__(self, instance, owner):
        """Returns a model thats bound to the client instance"""
        return type(
            self.model_cls.__name__, (self.model_cls, ),
            {
                '_client': instance
            }
        )


class DliClient(Accounts, AutoRegMetadata,
                Datafile, Dataset, Dictionary,
                Me, Package, Search):
    """
    Definition of a client. This client mixes in utility functions for
    manipulating packages, datasets and datafiles.
    """

    Dataset = ModelDescriptor(DatasetModel)
    Instance = ModelDescriptor(InstanceModel)
    _InstancesCollection = ModelDescriptor(InstancesCollection_)
    _Pagination = ModelDescriptor(Paginator)
    _File = ModelDescriptor(FileModel)
    _Package = ModelDescriptor(PackageModel)
    _DictionaryV2 = ModelDescriptor(DictionaryModel)

    _packages = ModelDescriptor(PackageModule)
    _datasets = ModelDescriptor(DatasetModule)

    _environment_class = _Environment
    _session = None

    def __init__(self, api_key, api_root, host=None, debug=None, strict=True):
        self._environment = self._environment_class(api_root)
        self.api_key = api_key
        self.host = host
        self.debug = debug
        self.strict = strict

        self._setup_logging()
        self._session = self._new_session()
        self._analytics_handler = AnalyticsHandler(self)
        self.logger.info(
            'Starting SDK session',
            extra={'jwt': self._session.decoded_token,
                   'target': self._environment,
                   'strict' : strict,
                   'version': __version__
                   }
        )

        self.packages = self._packages()
        self.datasets = self._datasets()

        if api_key is not None:
            warnings.warn(
                'The parameter `api_key` is going to become deprecated in the future. We will be contacting users in '
                'the following months to explain how to migrate them to a new login flow.',
                PendingDeprecationWarning
            )

    def _setup_logging(self):

        self.logger = logging.getLogger('dli.client_{}'.format(
            self.api_key[:5]
        ))

        json_format = JsonFormatter(
            '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            json_indent=2
        )

        handler = None
        chosen_level = None
        switcher = {
            "error": logging.ERROR,
            "warn": logging.WARNING,
            "debug": logging.DEBUG,
            "info": logging.INFO
        }

        if self.debug:
            # If debug - create a log file or stdout
            to, _, level = str(self.debug).partition(":")

            if to == "stdout":
                handler = logging.StreamHandler(stream=sys.stdout)
                chosen_level = switcher.get(level.lower(), logging.DEBUG)

        if not handler:
            log_folder = "logs/"
            Path(log_folder).mkdir(parents=True, exist_ok=True)

            handler = RotatingFileHandler(
                f'{log_folder}sdk.log', mode='w', backupCount=3)
            chosen_level = logging.DEBUG

        handler.setFormatter(json_format)
        handler.setLevel(chosen_level)
        self.logger.addHandler(handler)
        self.logger.setLevel(chosen_level)

    def _new_session(self):
        return Session(
            self.api_key,
            self._environment,
            self.host,
            logger=self.logger
        )

    @property
    def session(self):
        # if the session expired, then reauth
        # and create a new context
        if self._session.has_expired:
            self._session = self._new_session()
        return self._session


class Session(requests.Session):

    def __init__(
        self, api_key, environment, host, auth_key=None, logger=None
    ):
        super().__init__()
        self.logger = logger
        self.api_key = api_key
        self._environment = environment
        self.host = host
        self.siren_builder = PatchedSirenBuilder()
        self.auth_key = auth_key or self._get_auth_key()
        self.decoded_token = self._get_decoded_token()
        self.token_expires_on = self._get_expiration_date()

        # mount points to add headers to specific routing requests
        self._set_mount_adapters()

        # Don't allow cookies to be set.
        # The new API will reject requests with both a cookie
        # and a auth header (as there's no predictable crediential to choose).
        #
        # However the old API, once authenticated using a Bearer token, will
        # as a side effect of a request return a oidc_id_token which matches
        # the auth header. This is ignored.
        self.cookies.set_policy(BlockAll())

    def request(self, method, url, *args, **kwargs):
        if not urlparse(url).netloc:
            url = urljoin(self._environment.catalogue, url)

        kwargs.pop('hooks', None)
        hooks = {'response': self._response_hook}

        try:
            return super().request(method, url, hooks=hooks, *args, **kwargs)
        except socket.error as e:
            raise ValueError(
                'Unable to process request due to a networking issue '
                'root cause could be a bad connection, '
                'not being on the correct VPN, '
                'or a network timeout '
            ) from e

    @property
    def has_expired(self):
        # We subtract timedelta from the expiration time in order to allow a safety window for
        # a code block to execute after a check has been asserted.
        return datetime.datetime.utcnow() > (self.token_expires_on - datetime.timedelta(minutes=1))

    def _response_hook(self, response, *args, **kwargs):
        # Apologies for the ugly code. The startswith siren check
        # is to make this only relevant to the old API.
        response = Response(response, self.siren_builder)

        if self.logger:
            self.logger.debug(
                'Response',
                extra={
                    # 'content': response.content,
                    'status': response.status_code,
                    'method': response.request.method,
                    'request': response.request.url,
                    'headers': response.request.headers
                }
            )

        if not response.ok:
            exceptions = defaultdict(
                lambda: DatalakeException,
                {HTTPStatus.BAD_REQUEST: InvalidPayloadException,
                 HTTPStatus.UNPROCESSABLE_ENTITY: InvalidPayloadException,
                 HTTPStatus.UNAUTHORIZED: UnAuthorisedAccessException,
                 HTTPStatus.FORBIDDEN: InsufficientPrivilegesException,
                 HTTPStatus.NOT_FOUND: CatalogueEntityNotFoundException}
            )

            try:
                message = response.json()
            except (JSONDecodeError, ValueError):
                message = response.text

            raise exceptions[response.status_code](
                message=message,
                params=parse_qs(urlparse(response.request.url).query),
                response=response
            )

        return response

    def _set_mount_adapters(self):
        self.mount(
            urljoin(self._environment.catalogue, '__api/'),
            DLIInterfaceV1Adapter(self)
        )

        self.mount(
            urljoin(self._environment.catalogue, '__api_v2/'),
            DLIBearerAuthAdapter(self)
        )

        self.mount(
            self._environment.consumption, DLIBearerAuthAdapter(self)
        )

        self.mount(
            urljoin(self._environment.accounts, 'api/identity/v1/'),
            DLIAccountsV1Adapter(self)
        )

        self.mount(
            urljoin(self._environment.accounts, 'api/identity/v2/'),
            DLIBearerAuthAdapter(self)
        )

        self.mount(
            self._environment.consumption, DLIBearerAuthAdapter(self)
        )

    def _get_decoded_token(self):
        return jwt.decode(self.auth_key, verify=False)

    def _get_expiration_date(self):
        default_timeout = (
            datetime.datetime.utcnow() +
            datetime.timedelta(minutes=55)
        )

        if 'exp' not in self.decoded_token:
            return default_timeout

        return datetime.datetime.utcfromtimestamp(
            self.decoded_token['exp']
        ) - datetime.timedelta(minutes=5)

    def _get_auth_key(self):
        try:
            response = self.post(
                '/__api/start-session', headers={
                    'Authorization': 'Bearer {}'.format(self.api_key)
                }
            )
        except DatalakeException as e:
            raise AuthenticationFailure(
                message='Could not authenticate API key'
            ) from e

        return response.text


class Response(ObjectProxy):

    def __init__(self, wrapped, builder, *args, **kwargs):
        super(Response, self).__init__(wrapped, *args, **kwargs)
        self.builder = builder

    def to_siren(self):
        # Pypermedias terminology, not mine
        python_object = self.builder._construct_entity(
            self.json()
        ).as_python_object()

        # Keep the response availible
        python_object._raw_response = self

        return python_object

    def to_many_siren(self, relation):
        return [
            siren_to_entity(c) for c in
            self.to_siren().get_entities(rel=relation)
        ]


class BlockAll(CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False
