import pytest


@pytest.fixture
def requests_get_mock(mocker):
    return mocker.patch("requests.get")


"https://pephub.databio.org/pep/test_geo_project/test_name/123?DATA=test"
"https://pephub.databio.org/pep/test_geo_project/test_name/convert?filter=csv?DATA=test"
