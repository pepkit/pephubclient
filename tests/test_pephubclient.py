from pephubclient.pephubclient import PEPHubClient
import pytest
from pephubclient.constants import RegistryPath
from pephubclient.exceptions import IncorrectQueryStringError


@pytest.mark.parametrize(
    "query_string",
    [
        "",
    ]
)
def test_get_request_data_from_string_raises_error_for_incorrect_query_string(query_string):
    with pytest.raises(IncorrectQueryStringError) as e:
        PEPHubClient().get_request_data_from_string(query_string)

    assert e.value.query_string == query_string


@pytest.mark.parametrize(
    "query_string, expected_output",
    [
        ("geo/GSE124224", RegistryPath(namespace="geo", item="GSE124224")),
    ]
)
def test_get_request_data_from_string_parses_data_correctly(query_string, expected_output):
    assert PEPHubClient().get_request_data_from_string(query_string) == expected_output


@pytest.mark.parametrize(
    "registry_path, variables, expected_url",
    [
        (RegistryPath(namespace="geo", item="123"), {"DATA": "test"}, "https://pephub.databio.org/pep/geo/123?DATA=test"),
        (RegistryPath(namespace="geo", item="123"), {"DATA": "test", "VARIABLE": "value"}, "https://pephub.databio.org/pep/geo/123?DATA=test&VARIABLE=value"),
        (RegistryPath(namespace="geo", item="123"), {}, "https://pephub.databio.org/pep/geo/123?DATA=test&VARIABLE=value"),
    ]
)
def test_request_pephub_creates_correct_url(registry_path, variables, expected_url, requests_get_mock):
    PEPHubClient().request_pephub(registry_path, variables)

    assert requests_get_mock.called_with(expected_url)
