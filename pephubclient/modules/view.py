import logging

import peppy

from pephubclient.constants import (
    PEPHUB_VIEW_SAMPLE_URL,
    PEPHUB_VIEW_URL,
    ResponseStatusCodes,
)
from pephubclient.exceptions import ResponseError
from pephubclient.helpers import RequestManager
from pephubclient.models import ProjectDict

_LOGGER = logging.getLogger("pephubclient")


class PEPHubView(RequestManager):
    """
    Class for managing views in PEPhub.

    Provides methods for getting, creating, updating and removing views. This class
    aims to wrap the Views API for easier maintenance and better user experience.
    """

    def __init__(self, jwt_data: str | None = None) -> None:
        """
        Args:
            jwt_data: JWT token for authorization.
        """
        self.__jwt_data = jwt_data

    def get(
        self, namespace: str, name: str, tag: str, view_name: str, raw: bool = False
    ) -> peppy.Project | dict:
        """
        Get view from project in PEPhub.

        Args:
            namespace: Namespace of project.
            name: Name of project.
            tag: Tag of project.
            view_name: Name of the view.
            raw: If True, return raw response.

        Returns:
            peppy.Project object or dictionary of the project (view).
        """
        url = self._build_view_request_url(
            namespace=namespace, name=name, view_name=view_name
        )

        url = url + self.parse_query_param(pep_variables={"tag": tag})

        response = self.send_request(
            method="GET", url=url, headers=self.parse_header(self.__jwt_data)
        )
        if response.status_code == ResponseStatusCodes.OK:
            output = self.decode_response(response, output_json=True)
            if raw:
                return output
            output = ProjectDict(**output).model_dump(by_alias=True)
            return peppy.Project.from_dict(output)
        elif response.status_code == ResponseStatusCodes.NOT_EXIST:
            raise ResponseError("View does not exist, or you are unauthorized.")
        else:
            raise ResponseError(
                f"Internal server error. Unexpected return value. Error: {response.status_code}"
            )

    def create(
        self,
        namespace: str,
        name: str,
        tag: str,
        view_name: str,
        description: str | None = None,
        sample_list: list | None = None,
        no_fail: bool = False,
    ) -> None:
        """
        Create view in project in PEPhub.

        Args:
            namespace: Namespace of project.
            name: Name of project.
            tag: Tag of project.
            view_name: Name of the view.
            description: Description of the view.
            sample_list: List of sample names.
            no_fail: Whether to raise an error if the view was not added to the project.
        """
        if not sample_list or not isinstance(sample_list, list):
            raise ValueError("Sample list must be a list of sample names.")

        url = self._build_view_request_url(
            namespace=namespace, name=name, view_name=view_name
        )

        url = url + self.parse_query_param(pep_variables={"tag": tag})

        response = self.send_request(
            method="POST",
            url=url,
            headers=self.parse_header(self.__jwt_data),
            params={"description": description, "no_fail": no_fail},
            json=sample_list,
        )
        if response.status_code == ResponseStatusCodes.ACCEPTED:
            _LOGGER.info(
                f"View '{view_name}' created in project '{namespace}/{name}:{tag}' successfully."
            )
            return None
        elif response.status_code == ResponseStatusCodes.NOT_EXIST:
            raise ResponseError(
                f"Project '{namespace}/{name}:{tag}' or one of the samples does not exist."
            )
        elif response.status_code == ResponseStatusCodes.CONFLICT:
            raise ResponseError(f"View '{view_name}' already exists in the project.")
        else:
            raise ResponseError(f"Unexpected return value.{response.status_code}")

    def delete(self, namespace: str, name: str, tag: str, view_name: str) -> None:
        """
        Delete view from project in PEPhub.

        Args:
            namespace: Namespace of project.
            name: Name of project.
            tag: Tag of project.
            view_name: Name of the view.
        """
        url = self._build_view_request_url(
            namespace=namespace, name=name, view_name=view_name
        )

        url = url + self.parse_query_param(pep_variables={"tag": tag})

        response = self.send_request(
            method="DELETE", url=url, headers=self.parse_header(self.__jwt_data)
        )

        if response.status_code == ResponseStatusCodes.ACCEPTED:
            _LOGGER.info(
                f"View '{view_name}' deleted from project '{namespace}/{name}:{tag}' successfully."
            )
            return None
        elif response.status_code == ResponseStatusCodes.NOT_EXIST:
            raise ResponseError("View does not exists, or you are unauthorized.")
        elif response.status_code == ResponseStatusCodes.UNAUTHORIZED:
            raise ResponseError("You are unauthorized to delete this view.")
        else:
            raise ResponseError("Unexpected return value. ")

    def add_sample(
        self,
        namespace: str,
        name: str,
        tag: str,
        view_name: str,
        sample_name: str,
    ) -> None:
        """
        Add sample to view in project in PEPhub.

        Args:
            namespace: Namespace of project.
            name: Name of project.
            tag: Tag of project.
            view_name: Name of the view.
            sample_name: Name of the sample.
        """
        url = self._build_view_request_url(
            namespace=namespace,
            name=name,
            view_name=view_name,
            sample_name=sample_name,
        )

        url = url + self.parse_query_param(pep_variables={"tag": tag})

        response = self.send_request(
            method="POST",
            url=url,
            headers=self.parse_header(self.__jwt_data),
        )
        if response.status_code == ResponseStatusCodes.ACCEPTED:
            _LOGGER.info(
                f"Sample '{sample_name}' added to view '{view_name}' in project '{namespace}/{name}:{tag}' successfully."
            )
            return None
        elif response.status_code == ResponseStatusCodes.NOT_EXIST:
            raise ResponseError(
                f"Sample '{sample_name}' or project {namespace}/{name}:{tag} does not exist."
            )
        elif response.status_code == ResponseStatusCodes.CONFLICT:
            raise ResponseError(f"Sample '{sample_name}' already exists in the view.")
        else:
            raise ResponseError(
                f"Unexpected return value. Error: {response.status_code}"
            )

    def remove_sample(
        self,
        namespace: str,
        name: str,
        tag: str,
        view_name: str,
        sample_name: str,
    ) -> None:
        """
        Remove sample from view in project in PEPhub.

        Args:
            namespace: Namespace of project.
            name: Name of project.
            tag: Tag of project.
            view_name: Name of the view.
            sample_name: Name of the sample.
        """
        url = self._build_view_request_url(
            namespace=namespace,
            name=name,
            view_name=view_name,
            sample_name=sample_name,
        )

        url = url + self.parse_query_param(pep_variables={"tag": tag})

        response = self.send_request(
            method="DELETE",
            url=url,
            headers=self.parse_header(self.__jwt_data),
        )
        if response.status_code == ResponseStatusCodes.ACCEPTED:
            _LOGGER.info(
                f"Sample '{sample_name}' removed from view '{view_name}' in project '{namespace}/{name}:{tag}' successfully."
            )
            return None
        elif response.status_code == ResponseStatusCodes.NOT_EXIST:
            raise ResponseError(
                f"Sample '{sample_name}' or project {namespace}/{name}:{tag} does not exist. "
            )
        elif response.status_code == ResponseStatusCodes.UNAUTHORIZED:
            raise ResponseError(
                "You are unauthorized to remove this sample from the view."
            )
        else:
            raise ResponseError(
                f"Unexpected return value. Error: {response.status_code}"
            )

    @staticmethod
    def _build_view_request_url(
        namespace: str, name: str, view_name: str, sample_name: str | None = None
    ) -> str:
        """
        Build URL for view request.

        Args:
            namespace: Namespace of project.
            name: Name of project.
            view_name: Name of view.
            sample_name: Name of the sample.

        Returns:
            URL string.
        """
        if sample_name:
            return PEPHUB_VIEW_SAMPLE_URL.format(
                namespace=namespace,
                project=name,
                view_name=view_name,
                sample_name=sample_name,
            )
        return PEPHUB_VIEW_URL.format(
            namespace=namespace,
            project=name,
            view_name=view_name,
        )
