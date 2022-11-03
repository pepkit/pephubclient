import pytest
from unittest.mock import Mock, patch, mock_open
from pephubclient.pephubclient import PEPHubClient
from error_handling.exceptions import ResponseError


def test_login(mocker, test_jwt_response, test_client_data, test_access_token):
    mocker.patch(
        "github_oauth_client.github_oauth_client.GitHubOAuthClient.get_access_token",
        return_value=test_access_token,
    )
    pephub_request_mock = mocker.patch(
        "requests.request", return_value=Mock(content=test_jwt_response)
    )
    pathlib_mock = mocker.patch("pathlib.Path.mkdir")

    with patch("builtins.open", mock_open()) as open_mock:
        PEPHubClient().login(client_data=test_client_data)

    assert open_mock.called
    assert pephub_request_mock.called
    assert pathlib_mock.called


def test_logout(mocker):
    os_remove_mock = mocker.patch("os.remove")
    PEPHubClient().logout()

    assert os_remove_mock.called


def test_pull(mocker, test_jwt):
    mocker.patch(
        "pephubclient.files_manager.FilesManager.load_jwt_data_from_file",
        return_value=test_jwt,
    )
    mocker.patch(
        "requests.request", return_value=Mock(content=b"some_data", status_code=200)
    )
    save_project_mock = mocker.patch(
        "pephubclient.files_manager.FilesManager.save_pep_project"
    )

    PEPHubClient().pull("some/project")

    assert save_project_mock.called


@pytest.mark.parametrize(
    "status_code, expected_error_message",
    [
        (
            404,
            "Some error message",
        ),
        (
            403,
            "Some error message",
        ),
        (501, "Some error message"),
    ],
)
def test_pull_with_pephub_error_response(
    mocker, test_jwt, status_code, expected_error_message
):
    mocker.patch(
        "pephubclient.files_manager.FilesManager.load_jwt_data_from_file",
        return_value=test_jwt,
    )
    mocker.patch(
        "requests.request",
        return_value=Mock(
            content=b'{"detail": "Some error message"}', status_code=status_code
        ),
    )

    with pytest.raises(ResponseError) as e:
        PEPHubClient().pull("some/project")

    assert e.value.message == expected_error_message
