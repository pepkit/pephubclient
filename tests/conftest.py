import pytest


@pytest.fixture
def requests_get_mock(mocker):
    return mocker.patch("requests.get")
