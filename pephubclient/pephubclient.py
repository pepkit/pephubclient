import json
import peppy
import requests
from pephubclient.constants import PEPHUB_URL, RegistryPath
from peppy import Project
from pephubclient.exceptions import IncorrectQueryStringError
from ubiquerg import parse_registry_path
from pydantic.error_wrappers import ValidationError


class PEPHubClient:
    """
    Main class responsible for providing Python interface for PEP Hub.
    """

    def load_pep(self, query_string: str) -> Project:
        request_data = self.get_request_data_from_string(query_string)
        pephub_response = self.request_pephub(request_data)
        return self.parse_pephub_response(pephub_response)

    @staticmethod
    def get_request_data_from_string(query_string: str) -> RegistryPath:
        try:
            return RegistryPath(**parse_registry_path(query_string))
        except ValidationError:
            raise IncorrectQueryStringError(query_string=query_string)

    @staticmethod
    def request_pephub(registry_path_data: RegistryPath):
        endpoint = registry_path_data.namespace + "/" + registry_path_data.item + "/"
        filter_string = "convert?filter=csv"
        full_url = PEPHUB_URL + endpoint #+ filter_string
        return requests.get(full_url, verify=False)

    @staticmethod
    def parse_pephub_response(pephub_response: requests.Response) -> peppy.Project:
        response_as_dictionary = json.loads(pephub_response.content.decode("utf-8"))
        return Project()
