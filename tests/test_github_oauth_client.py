from github_oauth_client.github_oauth_client import GitHubOAuthClient
from unittest.mock import Mock
import pytest
from exceptions import GitHubResponseError


def test_get_device_verification_code(mocker, input_return_mock):
    response = Mock(
        content=b"{"
        b'"device_code": "test_device_code", '
        b'"user_code": "test_user_code", '
        b'"verification_uri": "test_verification_uri"}'
    )

    post_request_mock = mocker.patch("requests.post", return_value=response)

    assert GitHubOAuthClient().get_device_verification_code() == "test_device_code"
    assert post_request_mock.called


@pytest.mark.parametrize(
    "response_content",
    [
        b"not json content",
        b'{"user_code": "test_user_code"}',
        b'{"device_code": "test_device_code"}',
    ],
)
def test_get_device_verification_code_raises_correct_exception(
    mocker, input_return_mock, response_content
):
    response = Mock(content=response_content)
    post_request_mock = mocker.patch("requests.post", return_value=response)

    with pytest.raises(GitHubResponseError):
        GitHubOAuthClient().get_device_verification_code()

    assert post_request_mock.called


def test_get_access_token(mocker, test_access_token):
    response = Mock(content=b'{"access_token": "test_access_token"}')
    post_request_mock = mocker.patch("requests.post", return_value=response)

    assert GitHubOAuthClient().get_access_token("test_device_code") == test_access_token
    assert post_request_mock.called


def test_login(mocker, input_return_mock, test_access_token):
    side_effects = [
        Mock(
            content=b"{"
            b'"device_code": "test_device_code", '
            b'"user_code": "test_user_code", '
            b'"verification_uri": "test_verification_uri"}'
        ),
        Mock(content=b'{"access_token": "test_access_token"}'),
    ]
    post_request_mock = mocker.patch("requests.post", side_effect=side_effects)

    client = GitHubOAuthClient()
    client.login()

    assert hasattr(client, "access_token")
    assert client.access_token == test_access_token
    assert post_request_mock.called
