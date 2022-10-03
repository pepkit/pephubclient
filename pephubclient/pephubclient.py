import os
from typing import Optional, Union

import peppy
import requests
from peppy import Project
from pydantic.error_wrappers import ValidationError
from ubiquerg import parse_registry_path

from pephubclient.constants import PEPHUB_BASE_URL, RegistryPath
from pephubclient.exceptions import IncorrectQueryStringError


class PEPHubClient:
    """
    Main class responsible for providing Python interface for PEPhub.
    """

    CONVERT_ENDPOINT = "convert?filter=csv"
    TMP_FILE_NAME = "pep_project.csv"

    def __init__(self):
        self.registry_path_data: Union[RegistryPath, None] = None

    def load_pep(self, query_string: str, variables: Optional[dict] = None) -> Project:
        self.set_registry_data(query_string)
        pephub_response = self.request_pephub(variables)
        return self.parse_pephub_response(pephub_response)

    def set_registry_data(self, query_string: str) -> None:
        """
        Parse provided query string to extract project name, sample name, etc.

        Args:
            query_string: Passed by user. Contain information needed to locate the project.

        Returns:
            Parsed query string.
        """
        try:
            self.registry_path_data = RegistryPath(**parse_registry_path(query_string))
        except (ValidationError, TypeError):
            raise IncorrectQueryStringError(query_string=query_string)

    def request_pephub(self, variables: Optional[dict] = None) -> requests.Response:
        """
        Send request to PEPhub to obtain the project data.

        Args:
            variables: Optional array of variables that will be passed to parametrize PEP project from PEPhub.
        """
        url = self._build_request_url()

        if variables:
            variables_string = PEPHubClient._parse_variables(variables)
            url += variables_string
        return requests.get(url, verify=False)

    def parse_pephub_response(
        self, pephub_response: requests.Response
    ) -> peppy.Project:
        """
        Save the csv data as file, read this data and return as peppy.Project object.

        Args:
            pephub_response: Raw response object from PEPhub.

        Returns:
            Peppy project instance.
        """
        self._save_response(pephub_response)
        project = Project(self.TMP_FILE_NAME)
        self._delete_file(self.TMP_FILE_NAME)
        return project

    def _build_request_url(self):
        endpoint = (
            self.registry_path_data.namespace
            + "/"
            + self.registry_path_data.item
            + "/"
            + PEPHubClient.CONVERT_ENDPOINT
        )
        return PEPHUB_BASE_URL + endpoint

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

    def _save_response(self, pephub_response: requests.Response) -> None:
        with open(self.TMP_FILE_NAME, "w") as f:
            f.write(pephub_response.content.decode("utf-8"))

    @staticmethod
    def _delete_file(filename: str) -> None:
        os.remove(filename)
