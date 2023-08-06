import warnings
import urllib

from collections import OrderedDict
from typing import Dict

from dli.models.dataset import DatasetModel
from dli.models.paginator import Paginator
from dli.client.components.urls import me_urls, search_urls, package_urls
from dli.models.package import PackageModel


class PackageModule:

    def __call__(self, search_term=None, only_mine=True) \
            -> Dict[str, PackageModel]:
        """
        See packages we can access at the top level.

        :param str search_term: The search phrase to search the catalogue
        with, and to pull back packages based on name, description etc.

        :param bool only_mine: Specify whether to collect packages only
        accessible to you (user) or to discover packages that you may
        want to discover.

        :returns: Ordered dictionary of id to PackageModel.
        :rtype: OrderedDict[id: str, PackageModel]
        """

        warnings.warn(
            "Sorry, we have had to disable this endpoint.",
            RuntimeWarning
        )
        return OrderedDict([])

        query = {}
        if search_term:
            query['query'] = search_term

        # First get the search term - if it's empty it will return everything
        search_paginator = Paginator(
            search_urls.search_packages + '?' + urllib.parse.urlencode(query),
            self._client._Package,
            self._client._Package._from_v1_response_to_v2
        )

        package_search = OrderedDict([(v.name, v) for v in search_paginator])

        if only_mine:
            consumed_paginator = Paginator(
                me_urls.consumed_packages,
                self._client._Package,
                self._client._Package._raw_dict
            )

            consumed_package_ids = set(
                package['packageId'] for package in consumed_paginator
            )

            # todo this should change to (v.shortcode, v) in future.
            # Short code is not exposed in the package API
            package_search = OrderedDict([
                (v.name, v) for v in package_search.values() if v.id in consumed_package_ids
            ])

        return package_search

    def _get(self, short_code) -> PackageModel:
        """
        Find a PackageModel with the matching short code. If not found then
        returns None.

        :param str short_code: The short code of the package to collect
        :returns: PackageModel with matching short code.
        :rtype: PackageModel
        """
        warnings.warn(
            'Getting a dataset by name, and package name or package ID'
            'will be deprecated in future. Short-codes will replace this.',
            PendingDeprecationWarning
        )
        params = {}

        # todo this should be by short code but EP doesnt seem to exist for this yet
        # so pass p_id
        params["name"] = short_code
        response = self._client.session.get(
            package_urls.package_index, params=params
        )
        return self._client._Package._from_v1_response_to_v2(response.json())

    def get_dataset(self, package_name, dataset_name) -> DatasetModel:
        """
        Find a PackageModel and DatasetModel with the matching short code
        within the package. If not found then returns None.

        :param package_id: str short_code: The short code of the package
            in which we search for a dataset.
        :param dataset_id: str short_code: The short code of the dataset
            to collect from within the package.
        :return: DatasetModel
        """
        params = {'name': package_name}
        package = self._client.session.get(
            package_urls.package_index, params=params
        ).json()

        params = {
            'filter[0][field]': 'name',
            'filter[0][operator]': 'eq',
            'filter[0][value]': dataset_name
        }

        dataset = self._client._session.get(
            package_urls.v2_package_datasets.format(
                id=package['properties']['packageId']),
            params=params
        )

        return dataset.json()
