from unittest.mock import patch, MagicMock

import pytest
from dli.client.components.urls import package_urls


class TestPackageModel:
    def test_display_package(
        self, capsys, dataset_request_index, test_client,
        package_request_v2
    ):
        test_client._session.get.return_value.json.side_effect = [
            dataset_request_index
        ]

        package = test_client._Package(package_request_v2)

        package.contents()
        captured = capsys.readouterr()
        assert captured.out == (
            '\nDATASET "TestDataset" [PARQUET]\n'
            '>> Shortcode: TestDataset\n'
            '>> Available Date Range: 2019-05-06 to 2020-01-01\n'
            '>> ID: 5b01376e-975d-11e9-8832-7e5ef76d533f\n'
            '>> Published: Monthly by IHS Markit\n'
            '>> Accessible: False\n'
            '\ndescription'
            '\n---------------------------------------'
            '-----------------------------------------\n'
        )

    @pytest.mark.xfail(
        reason='The packages() and datasets() endpoints are disabled')
    def test_retrieve_datasets_given_package(self, test_client,
                                             package_request, package_request_v2,
                                             dataset_request_index):
        test_client._session.get.return_value.json.side_effect = [
            package_request, package_request_v2, dataset_request_index
        ]

        pp = test_client.packages(search_term="", only_mine=False)
        ds = pp["Test Package"].datasets()
        assert len(ds) == 1


class TestPackageModule:

    @pytest.mark.xfail(
        reason='The packages() and datasets() endpoints are disabled')
    def test_search_packages(
        self, test_client, package_request, dataset_request_index
    ):
        with patch('dli.modules.package.Paginator') as mock_paginator:
            test_client.packages(search_term='abc')
            assert (
                mock_paginator.call_args_list[0][0][0] ==
                '/__api/search/packages/?query=abc'
            )

            assert (
                mock_paginator.call_args_list[1][0][0] ==
                '/__api/me/consumed_packages/'
            )

            mock_paginator.reset_mock()

            test_client.packages(search_term='abc', only_mine=False)
            assert mock_paginator.call_count == 1
            assert (
                mock_paginator.call_args_list[0][0][0] ==
                '/__api/search/packages/?query=abc'
            )

    def test_retrieve_package_by_get(
        self, test_client, package_request, dataset_request_index
    ):
        name = package_request['entities'][0]['properties']['name']
        package_request_v2 = {
            'data': {
                'id': package_request['entities'][0]['properties']['packageId'],
                'attributes': {'name': name}
            }
        }

        test_client._session.get.return_value.json.side_effect = [
                MagicMock(), package_request_v2
        ]

        test_package = test_client.packages._get('Test Package')
        assert test_package.name == name
