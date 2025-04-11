from pephubclient import PEPHubClient
from unittest.mock import Mock

example_schema = {
    "a": "b",
    "c": 1,
}
versions_example = {
    "pagination": {"page": 0, "page_size": 100, "total": 1},
    "results": [
        {
            "namespace": "databio",
            "schema_name": "test_test",
            "version": "bbb",
            "contributors": None,
            "release_notes": None,
            "tags": {},
            "release_date": "2025-04-02T18:27:22.829003Z",
            "last_update_date": "2025-04-02T18:27:22.829009Z",
        }
    ],
}


# @pytest.mark.skip("Tests are not implemented yet")
class TestSchemas:

    def test_get_schema(self, mocker, test_jwt):
        jwt_mock = mocker.patch(
            "pephubclient.files_manager.FilesManager.load_jwt_data_from_file",
            return_value=test_jwt,
        )
        requests_mock = mocker.patch(
            "requests.request",
            return_value=Mock(content="some return", status_code=200),
        )
        mocker.patch(
            "pephubclient.helpers.RequestManager.decode_response",
            return_value=example_schema,
        )

        phc = PEPHubClient()
        schema_value = phc.schema.get(namespace="databio", schema_name="pep")

        assert jwt_mock.called
        assert requests_mock.called
        assert schema_value == example_schema

    def test_get_schema_versions(self, mocker, test_jwt):
        jwt_mock = mocker.patch(
            "pephubclient.files_manager.FilesManager.load_jwt_data_from_file",
            return_value=test_jwt,
        )
        requests_mock = mocker.patch(
            "requests.request",
            return_value=Mock(content="some return", status_code=200),
        )
        mocker.patch(
            "pephubclient.helpers.RequestManager.decode_response",
            return_value=versions_example,
        )

        phc = PEPHubClient()

        schema_versions = phc.schema.get_versions(
            namespace="databio", schema_name="test_test"
        )

        assert jwt_mock.called
        assert requests_mock.called
        assert schema_versions

    def test_create_schema(self, mocker, test_jwt):
        jwt_mock = mocker.patch(
            "pephubclient.files_manager.FilesManager.load_jwt_data_from_file",
            return_value=test_jwt,
        )
        requests_mock = mocker.patch(
            "requests.request",
            return_value=Mock(content="some return", status_code=202),
        )

        phc = PEPHubClient()

        phc.schema.create_schema(
            namespace="tessttt",
            schema_name="test_test1",
            version="bbb",
            schema_value={"b2": "v"},
            contributors="Na",
        )

        assert jwt_mock.called
        assert requests_mock.called

    def test_update_schema(self, mocker, test_jwt):
        jwt_mock = mocker.patch(
            "pephubclient.files_manager.FilesManager.load_jwt_data_from_file",
            return_value=test_jwt,
        )
        requests_mock = mocker.patch(
            "requests.request",
            return_value=Mock(content="some return", status_code=202),
        )

        phc = PEPHubClient()

        phc.schema.update_record(
            namespace="test_test",
            schema_name="test_test",
            update_fields={
                "maintainers": "new_maintainer",
                "private": True,
                "lifecycle_stage": "development",
        )

        assert jwt_mock.called
        assert requests_mock.called

    def test_delete_schema(self, mocker, test_jwt):

        jwt_mock = mocker.patch(
            "pephubclient.files_manager.FilesManager.load_jwt_data_from_file",
            return_value=test_jwt,
        )
        requests_mock = mocker.patch(
            "requests.request",
            return_value=Mock(content="some return", status_code=202),
        )

        phc = PEPHubClient()

        phc.schema.delete_schema(
            namespace="test_test",
            schema_name="testttt",
        )

        assert jwt_mock.called
        assert requests_mock.called

    def test_add_version(self, mocker, test_jwt):
        jwt_mock = mocker.patch(
            "pephubclient.files_manager.FilesManager.load_jwt_data_from_file",
            return_value=test_jwt,
        )
        requests_mock = mocker.patch(
            "requests.request",
            return_value=Mock(content="some return", status_code=202),
        )

        phc = PEPHubClient()

        phc.schema.add_version(
            namespace="test_test",
            schema_name="test2",
            version="1.2.5",
            schema_value={"b": "v2"},
            contributors="Na",
        )

        assert jwt_mock.called
        assert requests_mock.called

    def test_update_version(self, mocker, test_jwt):
        jwt_mock = mocker.patch(
            "pephubclient.files_manager.FilesManager.load_jwt_data_from_file",
            return_value=test_jwt,
        )
        requests_mock = mocker.patch(
            "requests.request",
            return_value=Mock(content="some return", status_code=202),
        )

        phc = PEPHubClient()

        phc.schema.update_version(
            namespace="test_test",
            schema_name="test2",
            version="1.2.4",
            update_fields={
                "contributors": "new cont",
                "release_notes": "note new",
            },
        )

        assert jwt_mock.called
        assert requests_mock.called

    def test_delete_version(self, mocker, test_jwt):

        jwt_mock = mocker.patch(
            "pephubclient.files_manager.FilesManager.load_jwt_data_from_file",
            return_value=test_jwt,
        )
        requests_mock = mocker.patch(
            "requests.request",
            return_value=Mock(content="some return", status_code=202),
        )

        phc = PEPHubClient()

        phc.schema.delete_version(
            namespace="test2",
            schema_name="test_test",
            version="1.2.5",
        )

        assert jwt_mock.called
        assert requests_mock.called
