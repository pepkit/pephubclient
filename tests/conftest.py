import pytest
from github_oauth_client.models import LoggedUserData


@pytest.fixture
def requests_get_mock(mocker):
    return mocker.patch("requests.get")


@pytest.fixture
def input_return_mock(monkeypatch):
    return monkeypatch.setattr("builtins.input", lambda: None)


@pytest.fixture
def test_access_token():
    return "test_access_token"


@pytest.fixture
def test_logged_user_data():
    return LoggedUserData(login="test_user", id=1234567)
