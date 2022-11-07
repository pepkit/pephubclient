import pytest
from pephubclient.models import ClientData
import json


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
def test_jwt():
    return (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJsb2dpbiI6InJhZmFsc3RlcGllbiIsImlkIjo0MzkyNjUyMiwib3JnYW5pemF0aW9ucyI6bnVsbH0."
        "mgBP-7x5l9cqufhzdVi0OFA78pkYDEymwPFwud02BAc"
    )


@pytest.fixture
def test_jwt_response(test_jwt):
    return json.dumps({"jwt_token": test_jwt}).encode("utf-8")


@pytest.fixture
def test_client_data():
    return ClientData(client_id="test_id")
