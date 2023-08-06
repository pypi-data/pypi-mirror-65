from urllib.parse import urlparse, ParseResult


class _Environment:

    _catalogue_accounts_environment_map = {
        'catalogue.datalake.ihsmarkit.com': 'catalogue.datalake.ihsmarkit.com',
        'catalogue-uat.datalake.ihsmarkit.com': 'catalogue-uat.datalake.ihsmarkit.com',
        'catalogue-uat2.datalake.ihsmarkit.com': 'client-uat.datalake.ihsmarkit.com',  # Old to new.
        'client-uat.datalake.ihsmarkit.com': 'client-uat.datalake.ihsmarkit.com',
        'catalogue-dev.udpmarkit.net': 'catalogue-dev.udpmarkit.net',
        'catalogue-qa.udpmarkit.net': 'catalogue-qa.udpmarkit.net',
        'catalogue-qa2.udpmarkit.net': 'catalogue-qa2.udpmarkit.net',
    }

    _catalogue_consumption_environment_map = {
        'catalogue.datalake.ihsmarkit.com': 'consumption.datalake.ihsmarkit.com',  # noqa
        'catalogue-uat.datalake.ihsmarkit.com': 'consumption-uat.datalake.ihsmarkit.com',  # noqa
        'catalogue-uat2.datalake.ihsmarkit.com': 'consumption-uat2.datalake.ihsmarkit.com',  # noqa
        'client-uat.datalake.ihsmarkit.com': 'consumption-uat2.datalake.ihsmarkit.com',  # noqa
        'catalogue-dev.udpmarkit.net': 'consumption-dev.udpmarkit.net',  # noqa
        'catalogue-qa.udpmarkit.net': 'consumption-qa.udpmarkit.net',  # noqa
        'catalogue-qa2.udpmarkit.net': 'consumption-qa2.udpmarkit.net',  # noqa
    }

    def __init__(self, api_root):
        """
        Class to manage the different endpoints

        :param str root_url: The root url of the catalogue
        """
        catalogue_parse_result = urlparse(api_root)

        self.catalogue = ParseResult(
            catalogue_parse_result.scheme, catalogue_parse_result.netloc,
            '', '', '', ''
        ).geturl()

        accounts_host = self._catalogue_accounts_environment_map.get(
            catalogue_parse_result.netloc
        )

        self.accounts = ParseResult(
            catalogue_parse_result.scheme, accounts_host, '', '', '', ''
        ).geturl()


        consumption_host = self._catalogue_consumption_environment_map.get(
            catalogue_parse_result.netloc
        )

        self.consumption = ParseResult(
            'https', consumption_host, '', '', '', ''
        ).geturl()