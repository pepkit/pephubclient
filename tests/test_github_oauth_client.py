from github_oauth_client.github_oauth_client import GitHubOAuthClient
from unittest.mock import Mock, patch, mock_open
import pytest
from error_handling.exceptions import GitHubResponseError


def test_get_device_verification_code(mocker, input_return_mock):
    response = Mock(
        content=b"{"
        b'"device_code": "test_device_code", '
        b'"user_code": "test_user_code", '
        b'"verification_uri": "test_verification_uri"}'
    )

    post_request_mock = mocker.patch("requests.post", return_value=response)

    assert (
        GitHubOAuthClient("/test/directory/")._get_device_verification_code()
        == "test_device_code"
    )
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
        GitHubOAuthClient("/test/directory/")._get_device_verification_code()

    assert post_request_mock.called


def test_get_access_token(mocker, test_access_token):
    response = Mock(content=b'{"access_token": "test_access_token"}')
    post_request_mock = mocker.patch("requests.post", return_value=response)

    assert (
        GitHubOAuthClient("/test/directory/")._get_access_token("test_device_code")
        == test_access_token
    )
    assert post_request_mock.called


def test_login(mocker, input_return_mock, test_access_token):
    post_request_mock = mocker.patch(
        "requests.post",
        side_effect=[
            Mock(
                content=b"{"
                b'"device_code": "test_device_code", '
                b'"user_code": "test_user_code", '
                b'"verification_uri": "test_verification_uri"}'
            ),
            Mock(content=b'{"access_token": "test_access_token"}'),
        ],
    )
    get_request_mock = mocker.patch(
        "requests.get",
        return_value=Mock(content=b'{"login": "test_user", "id": 12345}'),
    )
    pathlib_exist_mock = mocker.patch("pathlib.Path.mkdir")
    open_mock = mocker.patch("builtins.open")

    client = GitHubOAuthClient("/test/directory/")
    client.login()

    assert hasattr(client, "access_token")
    assert client.access_token == test_access_token
    assert post_request_mock.called
    assert get_request_mock.called
    assert open_mock.called
    assert pathlib_exist_mock.called


def test_logout(mocker):
    os_remove_mock = mocker.patch("os.remove")

    GitHubOAuthClient("/test/directory/").logout()

    assert os_remove_mock.called


def test_retrieve_logged_user_data(mocker):
    json_load_mock = mocker.patch(
        "json.load", return_value={"login": "test_user", "id": 1234}
    )
    with patch("builtins.open", new_callable=mock_open()) as open_mock:
        logged_user_data = GitHubOAuthClient(
            "/test/directory"
        ).retrieve_logged_user_data()

    assert json_load_mock.called
    assert open_mock.called
    assert logged_user_data.login == "test_user"
    assert logged_user_data.id == 1234


def test_retrieve_logged_user_data_file_does_not_exist():
    GitHubOAuthClient("/test/directory").retrieve_logged_user_data()
