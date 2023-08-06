import pytest

from dli.client.builders import DatasetBuilder
from tests.integration import random_name


@pytest.mark.xfail(
    reason='The packages() and datasets() endpoints are disabled')
@pytest.mark.integration
def test_package_search(client):
    packages = client.packages(
        search_term='0_MS_2019_08_19', only_mine=False
    )

    assert packages

    packages = client.packages(
        search_term='0_MS_2019_08_19', only_mine=True
    )

    assert packages


@pytest.mark.xfail(
    reason='The packages() and datasets() endpoints are disabled')
@pytest.mark.integration
def test_dataset_search(client, csv_dataset_builder):

    with client.with_accounts([
        'bdf5fce5-3891-4ec2-9752-2dd89ae37e03',
        '11390b62-bb5e-4851-b129-7cd62442c8f8'
    ]) as other_client:
        package = other_client.register_package(
            name=random_name(),
            description="my package description",
            topic="Automotive",
            access="Restricted",
            internal_data="Yes",
            data_sensitivity="Public",
            terms_and_conditions="Terms",
            publisher="my publisher",
            access_manager_id='11390b62-bb5e-4851-b129-7cd62442c8f8',
            tech_data_ops_id='bdf5fce5-3891-4ec2-9752-2dd89ae37e03',
            manager_id='bdf5fce5-3891-4ec2-9752-2dd89ae37e03'
        )


        dataset = other_client.register_dataset(
            DatasetBuilder(
                package_id=package.package_id,
                name='dataset-files-test-' + random_name(),
                description="My dataset description",
                content_type="Pricing",
                data_format='CSV',
                publishing_frequency="Weekly",
                taxonomy=[]
            ).with_external_storage(
                location="jdbc://connectionstring:1232/my-db"
            )
        )

    assert not client.get_dataset(dataset.id).has_access
    assert not client.datasets(only_mine=True, search_term=dataset.id)
    assert client.datasets(only_mine=False, search_term=dataset.id)


@pytest.mark.integration
def test_package_get(client, package):
     assert client.packages._get(package.name)


@pytest.mark.integration
def test_dataset_get_returns_none_bad_name(client):
     assert not client.datasets._get('not a short code')
