import warnings

from dli.client.dli_client import DliClient
from dli import __version__
from distutils.version import StrictVersion
import requests
import json

DEPRECATED_AGE = 1


def version_check(package_name):
    url = f"https://pypi.python.org/pypi/{package_name}/json"
    print(f'version_check url {url}')
    try:
        data = requests.get(url).json()
        versions = list(x for x in data["releases"].keys() if 'b' not in x)
        versions = sorted(versions)
        versions.reverse()

        offset = versions.index(__version__)

        if offset > DEPRECATED_AGE:
            warnings.warn("You are using an old version of the SDK, please upgrade"
                          "using `pip install [dli] --upgrade` "
                          "before the SDK no longer functions as expected",
                          PendingDeprecationWarning)
    except:
        # Version check has been see to fail by Gilberto with an SSLError
        # when doing the handshake with pypi.
        pass


def start_session(
    api_key,
    root_url="https://catalogue.datalake.ihsmarkit.com/__api",
    host=None,
    debug=False,
    strict=True,
):
    """
    Entry point for the Data Lake SDK, returns a client instance that
    can be used to consume or register datasets.

    Example for starting a session:

        from dli.client import session
        dl = session.start_session(api_key)

    :param str api_key: Your API key, can be retrieved from your dashboard in
                        the Catalogue UI.
    :param str root_url: Optional. The environment you want to point to. By default it
                        points to Production.
    :param str host: Optional. Advanced usage, meant to force a hostname when DNS resolution
                     is not reacheable from the user's network.
                     This is meant to be used in conjunction with an
                     IP address as the root url.
                     Example: catalogue.datalake.ihsmarkit.com

    :param bool debug: Optional. Log SDK operations to a file in the current working
                       directory with the format "sdk-{end of api key}-{timestamp}.log"

    :param bool strict: Optional. When True, all exception messages and stack
                        trace are printed. When False, a shorter message is
                        printed and `None` should be returned.

    :returns: Data Lake interface client
    :rtype: dli.client.dli_client.DliClient

    """

    version_check('dli')
    return DliClient(api_key, root_url, host, debug=debug, strict=strict)
