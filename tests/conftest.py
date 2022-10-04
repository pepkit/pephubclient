import pytest


@pytest.fixture
def requests_get_mock(mocker):
    return mocker.patch("requests.get")


@pytest.fixture
def input_return_mock(monkeypatch):
    return monkeypatch.setattr("builtins.input", lambda: None)


@pytest.fixture
def test_access_token():
    return "test_access_token"
