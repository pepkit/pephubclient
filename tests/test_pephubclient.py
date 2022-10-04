import pytest
from unittest.mock import Mock, patch, mock_open
from pephubclient import PEPHubClient
from pephubclient.constants import RegistryPath
from exceptions import IncorrectQueryStringError, PEPhubResponseError


@pytest.mark.parametrize("query_string", [""])
def test_get_request_data_from_string_raises_error_for_incorrect_query_string(
    query_string,
):
    with pytest.raises(IncorrectQueryStringError) as e:
        PEPHubClient()._set_registry_data(query_string)

    assert e.value.query_string == query_string


@pytest.mark.parametrize(
    "query_string, expected_output",
    [("geo/GSE124224", RegistryPath(namespace="geo", item="GSE124224"))],
)
def test_get_request_data_from_string_parses_data_correctly(
    query_string, expected_output
):
    pep_hub_client = PEPHubClient()
    pep_hub_client._set_registry_data(query_string)
    assert pep_hub_client.registry_path_data == expected_output


@pytest.mark.parametrize(
    "variables, expected_url",
    [
        (
            {"DATA": "test"},
            "https://pephub.databio.org/pep/test_geo_project/test_name/convert?filter=csv?DATA=test",
        ),
        (
            {"DATA": "test", "VARIABLE": "value"},
            "https://pephub.databio.org/pep/test_geo_project/test_name/convert?filter=csv?DATA=test&VARIABLE=value",
        ),
        (
            {},
            "https://pephub.databio.org/pep/test_geo_project/test_name/convert?filter=csv",
        ),
    ],
)
def test_request_pephub_creates_correct_url(variables, expected_url, requests_get_mock):
    pep_hub_client = PEPHubClient()
    pep_hub_client.registry_path_data = RegistryPath(
        namespace="test_geo_project", item="test_name"
    )
    pep_hub_client.request_pephub(variables)

    requests_get_mock.assert_called_with(expected_url, verify=False)


def test_load_pep(mocker):
    save_response_mock = mocker.patch(
        "pephubclient.pephubclient.PEPHubClient._save_response"
    )
    delete_file_mock = mocker.patch(
        "pephubclient.pephubclient.PEPHubClient._delete_file"
    )
    requests_get_mock = mocker.patch("requests.get", return_value=Mock(status_code=200))

    PEPHubClient(filename_to_save=None).load_pep("test/querystring")

    assert save_response_mock.called
    assert delete_file_mock.called_with(None)
    assert requests_get_mock.called


def test_delete_file(mocker):
    os_remove_mock = mocker.patch("os.remove")
    PEPHubClient()._delete_file("test-filename.csv")
    assert os_remove_mock.called


def test_save_response():
    with patch("builtins.open", mock_open()) as open_mock:
        PEPHubClient()._save_response(Mock())
    assert open_mock.called


def test_save_pep_locally(mocker, requests_get_mock):
    save_response_mock = mocker.patch(
        "pephubclient.pephubclient.PEPHubClient._save_response"
    )
    PEPHubClient().save_pep_locally("test/project")

    assert save_response_mock.called
    assert requests_get_mock.called


@pytest.mark.parametrize(
    "registry_path, expected_filename",
    [
        (
            RegistryPath(namespace="test", item="project", tag="2022"),
            "test_project:2022.csv",
        ),
        (RegistryPath(namespace="test", item="project", tag=""), "test_project.csv"),
    ],
)
def test_create_filename_to_save_downloaded_project(registry_path, expected_filename):
    pep_hub_client = PEPHubClient()
    pep_hub_client.registry_path_data = registry_path

    assert (
        pep_hub_client._create_filename_to_save_downloaded_project()
        == expected_filename
    )


def test_parse_pephub_response_raises_correct_error():
    with pytest.raises(PEPhubResponseError):
        PEPHubClient().parse_pephub_response(
            Mock(content=b'{"detail": "error message here"}', status_code=404)
        )
