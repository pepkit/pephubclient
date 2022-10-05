import os
import json
from typing import Optional
import peppy
import requests
import urllib3
from peppy import Project
from pydantic.error_wrappers import ValidationError
from ubiquerg import parse_registry_path
from github_oauth_client.models import HTTPMethod
from pephubclient.constants import (
    PEPHUB_BASE_URL,
    PEPHUB_PEP_API_BASE_URL,
    RegistryPath,
)
from pephubclient.models import JWTDataResponse
from pephubclient.models import ClientData
from helpers import decode_response
from error_handling.exceptions import ResponseError, IncorrectQueryStringError
from error_handling.constants import ERROR_CODES, ResponseStatusCodes
from github_oauth_client.github_oauth_client import GitHubOAuthClient
from pephubclient.files_manager import FilesManager

urllib3.disable_warnings()


class PEPHubClient:
    CONVERT_ENDPOINT = "convert?filter=csv"
    CLI_LOGIN_ENDPOINT = "auth/login_cli"
    USER_DATA_FILE_NAME = "jwt.txt"
    DEFAULT_PROJECT_FILENAME = "pep_project.csv"
    PATH_TO_FILE_WITH_JWT = (
        os.path.join(os.getenv("HOME"), ".pephubclient/") + USER_DATA_FILE_NAME
    )

    def __init__(self):
        self.registry_path = None
        self.github_client = GitHubOAuthClient()

    def login(self, client_data: ClientData) -> None:
        jwt = self._request_jwt_from_pephub(client_data)
        FilesManager.save_jwt_data_to_file(self.PATH_TO_FILE_WITH_JWT, jwt)

    def logout(self) -> None:
        FilesManager.delete_file_if_exists(self.PATH_TO_FILE_WITH_JWT)

    def pull(self, project_query_string: str):
        jwt = FilesManager.load_jwt_data_from_file(self.PATH_TO_FILE_WITH_JWT)
        self._save_pep_locally(project_query_string, jwt)

    def _save_pep_locally(
        self,
        query_string: str,
        jwt: Optional[str] = None,
        variables: Optional[dict] = None,
    ) -> None:
        """
        Request PEPhub and save the requested project on the disk.

        Args:
            query_string: Project namespace, eg. "geo/GSE124224"
            variables: Optional variables to be passed to PEPhub

        """
        self._set_registry_data(query_string)
        pephub_response = self._request_pephub("GET", variables=variables, jwt_data=jwt)
        decoded_response = self._handle_pephub_response(pephub_response)
        FilesManager.save_pep_project(decoded_response, registry_path=self.registry_path)

    def _load_pep(
        self,
        query_string: str,
        variables: Optional[dict] = None,
        jwt_data: Optional[str] = None,
    ) -> Project:
        """
        Request PEPhub and return the requested project as peppy.Project object.

        Args:
            query_string: Project namespace, eg. "geo/GSE124224"
            variables: Optional variables to be passed to PEPhub
            jwt_data: JWT token.

        Returns:
            Downloaded project as object.
        """
        self._set_registry_data(query_string)
        pephub_response = self._request_pephub(
            method="GET", variables=variables, jwt_data=jwt_data
        )
        parsed_response = self._handle_pephub_response(pephub_response)
        return self._load_pep_project(parsed_response)

    def _request_pephub(
        self,
        method: str,
        url: Optional[str] = None,
        headers: Optional[dict] = None,
        variables: Optional[dict] = None,
        jwt_data: Optional[str] = None,
    ) -> requests.Response:
        return requests.request(
            method=method,
            url=url or self._build_request_url(variables),
            verify=False,
            cookies=self._get_cookies(jwt_data),
            headers=headers,
        )

    @staticmethod
    def _handle_pephub_response(pephub_response: requests.Response):
        decoded_response = decode_response(pephub_response)

        if pephub_response.status_code in ERROR_CODES:
            raise ResponseError(
                message="The project does not exist or current user has no permissions to view it."
            )
        elif pephub_response.status_code != ResponseStatusCodes.OK_200:
            raise ResponseError(message=json.loads(decoded_response).get("detail"))
        else:
            return decoded_response

    def _request_jwt_from_pephub(self, client_data: ClientData) -> str:
        pephub_response = self._request_pephub(
            method=HTTPMethod.POST,
            url=PEPHUB_BASE_URL + self.CLI_LOGIN_ENDPOINT,
            headers={"access-token": self.github_client.get_access_token(client_data)},
        )
        return JWTDataResponse(
            **json.loads(decode_response(pephub_response))
        ).jwt_token

    def _set_registry_data(self, query_string: str) -> None:
        """
        Parse provided query string to extract project name, sample name, etc.

        Args:
            query_string: Passed by user. Contain information needed to locate the project.

        Returns:
            Parsed query string.
        """
        try:
            self.registry_path = RegistryPath(**parse_registry_path(query_string))
        except (ValidationError, TypeError):
            raise IncorrectQueryStringError(query_string=query_string)

    @staticmethod
    def _get_cookies(jwt_data: Optional[str] = None) -> dict:
        if jwt_data:
            return {"pephub_session": jwt_data}
        else:
            return {}

    def _load_pep_project(self, pep_project: str) -> peppy.Project:
        FilesManager.save_pep_project(pep_project, self.registry_path, filename=self.DEFAULT_PROJECT_FILENAME)
        project = Project(self.DEFAULT_PROJECT_FILENAME)
        FilesManager.delete_file_if_exists(self.DEFAULT_PROJECT_FILENAME)
        return project

    def _build_request_url(self, variables: dict) -> str:
        endpoint = (
            self.registry_path.namespace
            + "/"
            + self.registry_path.item
            + "/"
            + PEPHubClient.CONVERT_ENDPOINT
        )
        if variables:
            variables_string = PEPHubClient._parse_variables(variables)
            endpoint += variables_string
        return PEPHUB_PEP_API_BASE_URL + endpoint

    @staticmethod
    def _parse_variables(pep_variables: dict) -> str:
        """
        Grab all the variables passed by user (if any) and parse them to match the format specified
        by PEPhub API for query parameters.

        Returns:
            PEPHubClient variables transformed into string in correct format.
        """
        parsed_variables = []

        for variable_name, variable_value in pep_variables.items():
            parsed_variables.append(f"{variable_name}={variable_value}")

        return "?" + "&".join(parsed_variables)

