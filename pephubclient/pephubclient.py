import json
import peppy
import requests
from pephubclient.constants import PEPHUB_URL, RegistryPath
from peppy import Project
from pephubclient.exceptions import IncorrectQueryStringError
from ubiquerg import parse_registry_path
from pydantic.error_wrappers import ValidationError
from typing import Optional


class PEPHubClient:
    """
    Main class responsible for providing Python interface for PEPhub.
    """

    def load_pep(self, query_string: str, variables: Optional[dict] = None) -> Project:
        request_data = self.get_request_data_from_string(query_string)
        pephub_response = self.request_pephub(request_data, variables)
        return self.parse_pephub_response(pephub_response)

    @staticmethod
    def get_request_data_from_string(query_string: str) -> RegistryPath:
        """
        Parse provided query string to extract project name, sample name, etc.

        Args:
            query_string: Passed by user. Contain information needed to locate the project.

        Returns:
            Parsed query string.
        """
        try:
            return RegistryPath(**parse_registry_path(query_string))
        except (ValidationError, TypeError):
            raise IncorrectQueryStringError(query_string=query_string)

    @staticmethod
    def request_pephub(registry_path_data: RegistryPath, variables: Optional[dict] = None) -> requests.Response:
        """
        Send request to PEPhub to obtain the project.

        Args:
            registry_path_data: Information about project, namespace, version, etc.
            variables: Optional array of variables that will be passed to parametrize PEP project from PEPhub.
        """
        endpoint = registry_path_data.namespace + "/" + registry_path_data.item
        variables_string = PEPHubClient._parse_variables(variables)
        full_url = PEPHUB_URL + endpoint + variables_string
        return requests.get(full_url, verify=False)

    @staticmethod
    def parse_pephub_response(pephub_response: requests.Response) -> peppy.Project:
        """
        Parse the response from PEPhub and provide returned data as peppy.Project object.

        Args:
            pephub_response: Raw response object from PEPhub.

        Returns:

        """
        response_as_dictionary = json.loads(pephub_response.content.decode("utf-8"))
        return Project()

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
