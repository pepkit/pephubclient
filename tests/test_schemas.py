import pytest
from pephubclient import PEPHubClient

example_schema = {
    "a": "b",
    "c": 1,
}


@pytest.mark.skip("Tests are not implemented yet")
class TestSchemas:

    def test_get_schema(self):

        phc = PEPHubClient()

        schema_value = phc.schema.get(namespace="databio", schema_name="pep")

        schema_value

    def test_get_schema_versions(self):
        phc = PEPHubClient()

        schema_versions = phc.schema.get_versions(
            namespace="databio", schema_name="pep"
        )

        schema_versions

    def test_create_schema(self):
        phc = PEPHubClient()

        phc.schema.create_schema(
            namespace="pepkit",
            schema_name="test_test1",
            version="bbb",
            schema_value={"b2": "v"},
            contributors="Na",
        )

    def test_update_schema(self):
        phc = PEPHubClient()

        phc.schema.update_record(
            namespace="pepkit",
            schema_name="test_test",
            update_fields={
                "maintainers": "new_maintainer",
                "private": True,
                "lifecycle_stage": "I don't know",
            },
        )

    def test_delete_schema(self):
        phc = PEPHubClient()

        phc.schema.delete_schema(
            namespace="databio",
            schema_name="testttt",
        )

    def test_add_version(self):
        phc = PEPHubClient()

        phc.schema.add_version(
            namespace="pepkit",
            schema_name="test_test",
            version="1.2.5",
            schema_value={"b": "v2"},
            contributors="Na",
        )

    def test_update_version(self):
        phc = PEPHubClient()

        phc.schema.update_version(
            namespace="pepkit",
            schema_name="test_test",
            version="1.2.4",
            update_fields={
                "contributors": "new cont",
                "release_notes": "note new",
            },
        )

    def test_delete_version(self):
        phc = PEPHubClient()

        phc.schema.delete_version(
            namespace="pepkit",
            schema_name="test_test",
            version="1.2.5",
        )
