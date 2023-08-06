import os
import warnings

warnings.filterwarnings(
    'always', module="dli"
)

__version__ = '1.7.0b3'


def connect(api_key=None,
            root_url="https://catalogue.datalake.ihsmarkit.com/__api",
            debug=None,
            strict=None):

    from dli.client.session import start_session

    if api_key is not None:
        api_key = api_key
    elif os.environ.get("DLI_API_KEY") is not None:
        api_key = os.environ["DLI_API_KEY"]
    else:
        warnings.warn("You must provide your api_key by setting "
                      "`export DLI_API_KEY={key}` "
                      "or passing in api_key as kwarg argument")
        return

    root_url = root_url
    return start_session(
        api_key,
        root_url=root_url,
        host=None,
        debug=debug,
        strict=strict
    )
