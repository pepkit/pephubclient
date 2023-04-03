import os
from unittest.mock import Mock

import pytest

from pephubclient.exceptions import ResponseError
from pephubclient.pephubclient import PEPHubClient

SAMPLE_PEP = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "tests",
    "data",
    "sample_pep",
    "subsamp_config.yaml",
)


class TestSmoke:
    def test_login(self, mocker, device_code_return, test_jwt):
        """
        Test if device login request was sent to pephub
        """
        requests_mock = mocker.patch(
            "requests.request",
            return_value=Mock(content=device_code_return, status_code=200),
        )
        pephub_response_mock = mocker.patch(
            "pephubclient.pephub_oauth.pephub_oauth.PEPHubAuth._handle_pephub_response",
            return_value=device_code_return,
        )
        pephub_exchange_code_mock = mocker.patch(
            "pephubclient.pephub_oauth.pephub_oauth.PEPHubAuth._exchange_device_code_on_token",
            return_value=test_jwt,
        )

        pathlib_mock = mocker.patch(
            "pephubclient.files_manager.FilesManager.save_jwt_data_to_file"
        )

        PEPHubClient().login()

        assert requests_mock.called
        assert pephub_response_mock.called
        assert pephub_exchange_code_mock.called
        assert pathlib_mock.called

    def test_logout(self, mocker):
        os_remove_mock = mocker.patch("os.remove")
        PEPHubClient().logout()

        assert os_remove_mock.called

    def test_pull(self, mocker, test_jwt, test_raw_pep_return):
        jwt_mock = mocker.patch(
            "pephubclient.files_manager.FilesManager.load_jwt_data_from_file",
            return_value=test_jwt,
        )
        requests_mock = mocker.patch(
            "requests.request",
            return_value=Mock(content="some return", status_code=200),
        )
        mocker.patch(
            "pephubclient.pephubclient.PEPHubClient._handle_pephub_response",
            return_value=test_raw_pep_return,
        )
        save_yaml_mock = mocker.patch(
            "pephubclient.files_manager.FilesManager.save_yaml"
        )
        save_sample_mock = mocker.patch(
            "pephubclient.files_manager.FilesManager.save_pandas"
        )
        mocker.patch("pephubclient.files_manager.FilesManager.crete_project_folder")

        PEPHubClient().pull("some/project")

        assert jwt_mock.called
        assert requests_mock.called
        assert save_yaml_mock.called
        assert save_sample_mock.called

    @pytest.mark.parametrize(
        "status_code, expected_error_message",
        [
            (
                404,
                "File does not exist, or you are unauthorized.",
            ),
            (
                500,
                "Internal server error.",
            ),
            (501, "Unknown error occurred. Status: 501"),
        ],
    )
    def test_pull_with_pephub_error_response(
        self, mocker, test_jwt, status_code, expected_error_message
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

    def test_push(self, mocker, test_jwt):
        requests_mock = mocker.patch(
            "requests.request", return_value=Mock(status_code=202)
        )

        PEPHubClient().push(
            SAMPLE_PEP,
            namespace="s_name",
            name="name",
        )

        assert requests_mock.called

    @pytest.mark.parametrize(
        "status_code, expected_error_message",
        [
            (
                409,
                "Project already exists. Set force to overwrite project.",
            ),
            (
                401,
                "Unauthorized! Failure in uploading project.",
            ),
            (233, "Unexpected Response Error."),
        ],
    )
    def test_push_with_pephub_error_response(
        self, mocker, status_code, expected_error_message
    ):
        mocker.patch("requests.request", return_value=Mock(status_code=status_code))
        with pytest.raises(ResponseError, match=expected_error_message):
            PEPHubClient().push(
                SAMPLE_PEP,
                namespace="s_name",
                name="name",
            )
