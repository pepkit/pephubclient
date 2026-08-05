import logging

from pephubclient.constants import PEPHUB_SAMPLE_URL, ResponseStatusCodes
from pephubclient.exceptions import ResponseError
from pephubclient.helpers import RequestManager

_LOGGER = logging.getLogger("pephubclient")


class PEPHubSample(RequestManager):
    """
    Class for managing samples in PEPhub.

    Provides methods for getting, creating, updating and removing samples. This class
    is not related to the peppy.Sample class.
    """

    def __init__(self, jwt_data: str | None = None) -> None:
        """
        Args:
            jwt_data: JWT token for authorization.
        """
        self.__jwt_data = jwt_data

    def get(
        self,
        namespace: str,
        name: str,
        tag: str,
        sample_name: str | None = None,
    ) -> dict:
        """
        Get sample from project in PEPhub.

        Args:
            namespace: Namespace of project.
            name: Name of project.
            tag: Tag of project.
            sample_name: Sample name.

        Returns:
            Sample object.
        """
        url = self._build_sample_request_url(
            namespace=namespace, name=name, sample_name=sample_name
        )

        url = url + self.parse_query_param(pep_variables={"tag": tag})

        response = self.send_request(
            method="GET", url=url, headers=self.parse_header(self.__jwt_data)
        )
        if response.status_code == ResponseStatusCodes.OK:
            return self.decode_response(response, output_json=True)
        if response.status_code == ResponseStatusCodes.NOT_EXIST:
            raise ResponseError(
                f"Sample does not exist. Project: '{namespace}/{name}:{tag}'. Sample_name: '{sample_name}'"
            )
        elif response.status_code == ResponseStatusCodes.INTERNAL_ERROR:
            raise ResponseError("Internal server error. Unexpected return value.")
        else:
            raise ResponseError(
                f"Unexpected return value. Error: {response.status_code}"
            )

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

        Args:
            namespace: Namespace of project.
            name: Name of project.
            tag: Tag of project.
            sample_name: Sample name.
            sample_dict: Sample dict.
            overwrite: Overwrite sample if it exists.
        """
        url = self._build_sample_request_url(
            namespace=namespace,
            name=name,
            sample_name=sample_name,
        )

        url = url + self.parse_query_param(
            pep_variables={"tag": tag, "overwrite": overwrite}
        )

        # add sample name to sample_dict if it is not there
        if sample_name not in sample_dict.values():
            sample_dict["sample_name"] = sample_name

        response = self.send_request(
            method="POST",
            url=url,
            headers=self.parse_header(self.__jwt_data),
            json=sample_dict,
        )
        if response.status_code == ResponseStatusCodes.ACCEPTED:
            _LOGGER.info(
                f"Sample '{sample_name}' added to project '{namespace}/{name}:{tag}' successfully."
            )
            return None
        elif response.status_code == ResponseStatusCodes.NOT_EXIST:
            raise ResponseError(f"Project '{namespace}/{name}:{tag}' does not exist.")
        elif response.status_code == ResponseStatusCodes.CONFLICT:
            raise ResponseError(
                f"Sample '{sample_name}' already exists. Set overwrite to True to overwrite sample."
            )
        else:
            raise ResponseError(
                f"Unexpected return value. Error: {response.status_code}"
            )

    def update(
        self,
        namespace: str,
        name: str,
        tag: str,
        sample_name: str,
        sample_dict: dict,
    ) -> None:
        """
        Update sample in project in PEPhub.

        Args:
            namespace: Namespace of project.
            name: Name of project.
            tag: Tag of project.
            sample_name: Sample name.
            sample_dict: Sample dict that contains elements to update.
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
        if response.status_code == ResponseStatusCodes.ACCEPTED:
            _LOGGER.info(
                f"Sample '{sample_name}' updated in project '{namespace}/{name}:{tag}' successfully."
            )
            return None
        elif response.status_code == ResponseStatusCodes.NOT_EXIST:
            raise ResponseError(
                f"Sample '{sample_name}' or project {namespace}/{name}:{tag} does not exist. Error: {response.status_code}"
            )
        else:
            raise ResponseError(
                f"Unexpected return value. Error: {response.status_code}"
            )

    def remove(self, namespace: str, name: str, tag: str, sample_name: str) -> None:
        """
        Remove sample from project in PEPhub.

        Args:
            namespace: Namespace of project.
            name: Name of project.
            tag: Tag of project.
            sample_name: Sample name.
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
        if response.status_code == ResponseStatusCodes.ACCEPTED:
            _LOGGER.info(
                f"Sample '{sample_name}' removed from project '{namespace}/{name}:{tag}' successfully."
            )
            return None
        elif response.status_code == ResponseStatusCodes.NOT_EXIST:
            raise ResponseError(
                f"Sample '{sample_name}' or project {namespace}/{name}:{tag} does not exist. Error: {response.status_code}"
            )
        else:
            raise ResponseError(
                f"Unexpected return value. Error: {response.status_code}"
            )

    @staticmethod
    def _build_sample_request_url(namespace: str, name: str, sample_name: str) -> str:
        """
        Build URL for sample request.

        Args:
            namespace: Namespace where the project is located.
            name: Name of project.
            sample_name: Sample name.

        Returns:
            URL string.
        """
        return PEPHUB_SAMPLE_URL.format(
            namespace=namespace, project=name, sample_name=sample_name
        )
