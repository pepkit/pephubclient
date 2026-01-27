import logging
from typing import Union, List

from pephubclient.helpers import RequestManager
from pephubclient.constants import ResponseStatusCodes
from pephubclient.schemas.constants import (
    PEPHUB_SCHEMA_VERSION_URL,
    PEPHUB_SCHEMA_VERSIONS_URL,
    PEPHUB_SCHEMA_NEW_SCHEMA_URL,
    PEPHUB_SCHEMA_NEW_VERSION_URL,
    PEPHUB_SCHEMA_RECORD_URL,
    LATEST_VERSION,
)
from pephubclient.exceptions import ResponseError
from pephubclient.schemas.models import (
    SchemaVersionResult,
    NewSchemaVersionModel,
    NewSchemaRecordModel,
    UpdateSchemaRecordFields,
    UpdateSchemaVersionFields,
)

_LOGGER = logging.getLogger("pephubclient")


class PEPHubSchema(RequestManager):
    """
    Class for managing schemas in PEPhub and provides methods for
        getting, creating, updating and removing schemas records and schema versions.
    """

    def __init__(self, jwt_data: str = None):
        """
        :param jwt_data: jwt token for authorization
        """

        self.__jwt_data = jwt_data

    def get(
        self, namespace: str, schema_name: str, version: str = LATEST_VERSION
    ) -> dict:
        """
        Get schema value for specific schema version.

        :param: namespace: namespace of schema
        :param: schema_name: name of schema
        :param: version: version of schema

        :return: Schema object as dictionary
        """

        pephub_response = self.send_request(
            method="GET",
            url=PEPHUB_SCHEMA_VERSION_URL.format(
                namespace=namespace, schema_name=schema_name, version=version
            ),
            headers=self.parse_header(self.__jwt_data),
            cookies=None,
        )
        if pephub_response.status_code == ResponseStatusCodes.OK:
            decoded_response = self.decode_response(pephub_response, output_json=True)
            return decoded_response

        if pephub_response.status_code == ResponseStatusCodes.NOT_EXIST:
            raise ResponseError("Schema doesn't exist, or you are unauthorized.")
        if pephub_response.status_code == ResponseStatusCodes.INTERNAL_ERROR:
            raise ResponseError(
                f"Internal server error. Unexpected return value. Error: {pephub_response.status_code}"
            )
        else:
            raise ResponseError(
                f"Unexpected Status code return. Error: {pephub_response.status_code}"
            )

    def get_versions(self, namespace: str, schema_name: str) -> SchemaVersionResult:
        """
        Get list of versions

        :param namespace: Namespace of the schema record
        :param schema_name: Name of the schema record

        :return: {
            pagination: PaginationResult
            results: List[SchemaVersionAnnotation]
        }
        """

        pephub_response = self.send_request(
            method="GET",
            url=PEPHUB_SCHEMA_VERSIONS_URL.format(
                namespace=namespace, schema_name=schema_name
            ),
            headers=self.parse_header(self.__jwt_data),
            cookies=None,
        )

        if pephub_response.status_code == ResponseStatusCodes.OK:
            decoded_response = self.decode_response(pephub_response, output_json=True)
            return SchemaVersionResult(**decoded_response)

        if pephub_response.status_code == ResponseStatusCodes.NOT_EXIST:
            raise ResponseError("Schema doesn't exist, or you are unauthorized.")
        if pephub_response.status_code == ResponseStatusCodes.INTERNAL_ERROR:
            raise ResponseError(
                f"Internal server error. Unexpected return value. Error: {pephub_response.status_code}"
            )
        else:
            raise ResponseError(
                f"Unexpected Status code return. Error: {pephub_response.status_code}"
            )

    def create_schema(
        self,
        namespace: str,
        schema_name: str,
        schema_value: dict,
        version: str = "1.0.0",
        description: str = None,
        maintainers: str = None,
        contributors: str = None,
        release_notes: str = None,
        tags: Union[str, List[str], dict, None] = None,
        lifecycle_stage: str = None,
        private: bool = False,
    ) -> None:
        """
        Create a new schema record + version in the database

        :param namespace: Namespace of the schema
        :param schema_name: Name of the schema record
        :param schema_value: Schema value itself in dict format
        :param version: First version of the schema
        :param description: Schema description
        :param maintainers: Schema maintainers
        :param contributors: Schema contributors of current version
        :param release_notes: Release notes for current version
        :param tags: Tags of the current version. Can be str, list[str], or dict
        :param lifecycle_stage: Stage of the schema record
        :param private: Weather project should be public or private. Default: False (public)

        :raise: ResponseError if status not 202.
        :return: None
        """

        url = PEPHUB_SCHEMA_NEW_SCHEMA_URL.format(namespace=namespace)
        request_body = NewSchemaRecordModel(
            schema_name=schema_name,
            description=description,
            maintainers=maintainers,
            lifecycle_stage=lifecycle_stage,
            private=private,
            contributors=contributors,
            release_notes=release_notes,
            tags=tags,
            version=version,
            schema_value=schema_value,
        ).model_dump(exclude_none=True)

        pephub_response = self.send_request(
            method="POST",
            url=url,
            headers=self.parse_header(self.__jwt_data),
            cookies=None,
            json=request_body,
        )

        if pephub_response.status_code == ResponseStatusCodes.ACCEPTED:
            _LOGGER.info(
                f"Schema '{namespace}/{schema_name}:{version}' successfully created in PEPhub"
            )
            return None

        elif pephub_response.status_code == ResponseStatusCodes.UNAUTHORIZED:
            raise ResponseError(
                "User not authorized or doesn't have permission to write to this namespace"
            )

        else:
            raise ResponseError(
                f"Unexpected error. Status code: {pephub_response.status_code}"
            )

    def add_version(
        self,
        namespace: str,
        schema_name: str,
        schema_value: dict,
        version: str = "1.0.0",
        contributors: str = None,
        release_notes: str = None,
        tags: Union[str, List[str], dict, None] = None,
    ) -> None:
        """
        Add new version to the schema registry

        :param namespace: Namespace of the schema
        :param schema_name: Name of the schema record
        :param schema_value: Schema value itself in dict format
        :param version: First version of the schema
        :param contributors: Schema contributors of current version
        :param release_notes: Release notes for current version
        :param tags: Tags of the current version. Can be str, list[str], or dict

        :raise: ResponseError if status not 202.
        :return: None
        """
        url = PEPHUB_SCHEMA_NEW_VERSION_URL.format(
            namespace=namespace, schema_name=schema_name
        )
        request_body = NewSchemaVersionModel(
            contributors=contributors,
            release_notes=release_notes,
            tags=tags,
            version=version,
            schema_value=schema_value,
        ).model_dump(exclude_none=True, exclude_unset=True)

        pephub_response = self.send_request(
            method="POST",
            url=url,
            headers=self.parse_header(self.__jwt_data),
            cookies=None,
            json=request_body,
        )

        if pephub_response.status_code == ResponseStatusCodes.ACCEPTED:
            _LOGGER.info(
                f"Schema version '{namespace}/{schema_name}:{version}' successfully created in PEPhub"
            )
            return None

        elif pephub_response.status_code == ResponseStatusCodes.UNAUTHORIZED:
            raise ResponseError(
                "User not authorized or doesn't have permission to write to this namespace"
            )

        else:
            raise ResponseError(
                f"Unexpected error. Status code: {pephub_response.status_code}"
            )

    def update_record(
        self,
        namespace: str,
        schema_name: str,
        update_fields: Union[dict, UpdateSchemaRecordFields],
    ) -> None:
        """
        Update schema registry data

        :param namespace: Namespace of the schema
        :param schema_name: Name of the schema version
        :param update_fields: dict or pydantic model UpdateSchemaRecordFields:
            {
                maintainers: str,
                lifecycle_stage: str,
                private: bool,
                name: str,
                description: str,
            }

        :raise: ResponseError if status not 202.
        :return: None
        """

        if isinstance(update_fields, dict):
            update_fields = UpdateSchemaRecordFields(**update_fields)

        update_fields = update_fields.model_dump(exclude_none=True, exclude_unset=True)

        url = PEPHUB_SCHEMA_RECORD_URL.format(
            namespace=namespace, schema_name=schema_name
        )

        pephub_response = self.send_request(
            method="PATCH",
            url=url,
            headers=self.parse_header(self.__jwt_data),
            cookies=None,
            json=update_fields,
        )

        if pephub_response.status_code == ResponseStatusCodes.ACCEPTED:
            _LOGGER.info(
                f"Schema record '{namespace}/{schema_name}' was updated successfully!"
            )
            return None

        elif pephub_response.status_code == ResponseStatusCodes.NOT_EXIST:
            raise ResponseError("Schema doesn't exist in PEPhub")

        elif pephub_response.status_code == ResponseStatusCodes.UNAUTHORIZED:
            raise ResponseError(
                "User not authorized or doesn't have permission to write to this namespace"
            )

        else:
            raise ResponseError(
                f"Unexpected error. Status code: {pephub_response.status_code}"
            )

    def update_version(
        self,
        namespace: str,
        schema_name: str,
        version: str,
        update_fields: Union[dict, UpdateSchemaVersionFields],
    ) -> None:
        """
        Update released version of the schema.

        :param namespace: Namespace of the schema
        :param schema_name: Name of the schema version
        :param version: Schema version
        :param update_fields: dict or pydantic model UpdateSchemaVersionFields:
            {
                contributors: str,
                schema_value: str,
                release_notes: str,
            }

        :raise: ResponseError if status not 202.
        :return: None
        """

        url = PEPHUB_SCHEMA_VERSION_URL.format(
            namespace=namespace, schema_name=schema_name, version=version
        )

        if isinstance(update_fields, dict):
            update_fields = UpdateSchemaVersionFields(**update_fields)

        update_fields = update_fields.model_dump(exclude_unset=True, exclude_none=True)

        pephub_response = self.send_request(
            method="PATCH",
            url=url,
            headers=self.parse_header(self.__jwt_data),
            cookies=None,
            json=update_fields,
        )

        if pephub_response.status_code == ResponseStatusCodes.ACCEPTED:
            _LOGGER.info(
                f"Schema version '{namespace}/{schema_name}:{version}' was updated successfully!"
            )
            return None

        elif pephub_response.status_code == ResponseStatusCodes.NOT_EXIST:
            raise ResponseError("Schema doesn't exist in PEPhub")

        elif pephub_response.status_code == ResponseStatusCodes.UNAUTHORIZED:
            raise ResponseError(
                "User not authorized or doesn't have permission to write to this namespace"
            )

        else:
            raise ResponseError(
                f"Unexpected error. Status code: {pephub_response.status_code}"
            )

    def delete_schema(self, namespace: str, schema_name: str) -> None:
        """
        Delete schema from the database

        :param namespace: Namespace of the schema
        :param schema_name: Name of the schema version
        """

        url = PEPHUB_SCHEMA_RECORD_URL.format(
            namespace=namespace, schema_name=schema_name
        )

        pephub_response = self.send_request(
            method="DELETE",
            url=url,
            headers=self.parse_header(self.__jwt_data),
            cookies=None,
        )

        if pephub_response.status_code == ResponseStatusCodes.ACCEPTED:
            _LOGGER.info(
                f"Schema record '{namespace}/{schema_name}' was updated successfully!"
            )
            return None

        elif pephub_response.status_code == ResponseStatusCodes.NOT_EXIST:
            raise ResponseError("Schema doesn't exist in PEPhub")

        elif pephub_response.status_code == ResponseStatusCodes.UNAUTHORIZED:
            raise ResponseError(
                "User not authorized or doesn't have permission to write to this namespace"
            )

        else:
            raise ResponseError(
                f"Unexpected error. Status code: {pephub_response.status_code}"
            )

    def delete_version(
        self,
        namespace: str,
        schema_name: str,
        version: str,
    ) -> None:
        """
        Delete schema Version

        :param namespace: Namespace of the schema
        :param schema_name: Name of the schema
        :param version: Schema version

        :raise: ResponseError if status not 202.
        :return: None
        """

        url = PEPHUB_SCHEMA_VERSION_URL.format(
            namespace=namespace, schema_name=schema_name, version=version
        )

        pephub_response = self.send_request(
            method="DELETE",
            url=url,
            headers=self.parse_header(self.__jwt_data),
            cookies=None,
        )

        if pephub_response.status_code == ResponseStatusCodes.ACCEPTED:
            _LOGGER.info(
                f"Schema version '{namespace}/{schema_name}:{version}' was updated successfully!"
            )
            return None

        elif pephub_response.status_code == ResponseStatusCodes.NOT_EXIST:
            raise ResponseError("Schema doesn't exist in PEPhub")

        elif pephub_response.status_code == ResponseStatusCodes.UNAUTHORIZED:
            raise ResponseError(
                "User not authorized or doesn't have permission to write to this namespace"
            )

        else:
            raise ResponseError(
                f"Unexpected error. Status code: {pephub_response.status_code}"
            )
