from github_oauth_client.github_oauth_client import GitHubOAuthClient
from unittest.mock import Mock


def test_get_access_token(mocker, test_client_data, input_return_mock):
    post_request_mock = mocker.patch(
        "requests.request",
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
    GitHubOAuthClient().get_access_token(test_client_data)

    assert post_request_mock.called
