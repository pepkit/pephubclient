from pephubclient.helpers import RequestManager
from pephubclient.constants import PEPHUB_SAMPLE_URL
import json


class PEPHubSample(RequestManager):
    """
    Class for managing samples in PEPhub and provides methods for
        getting, creating, updating and removing samples.
    This class is not related to peppy.Sample class.
    """

    def __init__(self, jwt_data: str = None):
        """
        :param jwt_data: jwt token for authorization
        """

        self.__jwt_data = jwt_data

    def get(
        self,
        namespace: str,
        name: str,
        tag: str,
        sample_name: str = None,
    ) -> dict:
        """
        Get sample from project in PEPhub.

        :param namespace: namespace of project
        :param name: name of project
        :param tag: tag of project
        :param sample_name: sample name
        :return: Sample object
        """
        url = self._build_sample_request_url(
            namespace=namespace, name=name, sample_name=sample_name
        )

        url = url + self.parse_query_param(pep_variables={"tag": tag})

        response = self.send_request(
            method="GET", url=url, headers=self.parse_header(self.__jwt_data)
        )
        output = dict(json.loads(self.decode_response(response)))
        return output

    def create(
        self,
        namespace: str,
        name: str,
        tag: str,
        sample_name: str,
        sample_dict: dict,
        overwrite: bool = False,
    ) -> None:
        """
        Create sample in project in PEPhub.

        :param namespace: namespace of project
        :param name: name of project
        :param tag: tag of project
        :param sample_dict: sample dict
        :param sample_name: sample name
        :param overwrite: overwrite sample if it exists
        :return: None
        """
        url = self._build_sample_request_url(
            namespace=namespace,
            name=name,
            sample_name=sample_name,
        )

        url = url + self.parse_query_param(
            pep_variables={"tag": tag, "overwrite": overwrite}
        )

        response = self.send_request(
            method="POST",
            url=url,
            headers=self.parse_header(self.__jwt_data),
            json=sample_dict,
        )
        output = self.decode_response(response)
        return output

    def update(
        self,
        namespace: str,
        name: str,
        tag: str,
        sample_name: str,
        sample_dict: dict,
    ):
        """
        Update sample in project in PEPhub.

        :param namespace: namespace of project
        :param name: name of project
        :param tag: tag of project
        :param sample_name: sample name
        :param sample_dict: sample dict, that contain elements to update, or
        :return: None
        """

        url = self._build_sample_request_url(
            namespace=namespace, name=name, sample_name=sample_name
        )

        url = url + self.parse_query_param(pep_variables={"tag": tag})

        response = self.send_request(
            method="PATCH",
            url=url,
            headers=self.parse_header(self.__jwt_data),
            json=sample_dict,
        )
        output = self.decode_response(response)
        return output

    def remove(self, namespace: str, name: str, tag: str, sample_name: str):
        """
        Remove sample from project in PEPhub.

        :param namespace: namespace of project
        :param name: name of project
        :param tag: tag of project
        :param sample_name: sample name
        :return: None
        """
        url = self._build_sample_request_url(
            namespace=namespace, name=name, sample_name=sample_name
        )

        url = url + self.parse_query_param(pep_variables={"tag": tag})

        response = self.send_request(
            method="DELETE",
            url=url,
            headers=self.parse_header(self.__jwt_data),
        )
        output = self.decode_response(response)
        return output

    @staticmethod
    def _build_sample_request_url(namespace: str, name: str, sample_name: str) -> str:
        """
        Build url for sample request.

        :param namespace: namespace where project will be uploaded
        :return: url string
        """
        return PEPHUB_SAMPLE_URL.format(
            namespace=namespace, project=name, sample_name=sample_name
        )