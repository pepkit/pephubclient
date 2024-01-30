class PEPHubView:
    """
    Class for managing views in PEPhub and provides methods for
        getting, creating, updating and removing views.

    This class aims to warp the Views API for easier maintenance and
    better user experience.
    """

    def __init__(self, jwt_data: str = None):
        """
        :param jwt_data: jwt token for authorization
        """

        self.__jwt_data = jwt_data

    def get(self, namespace: str, name: str, tag: str, view_name: str): ...

    def create(
        self, namespace: str, name: str, tag: str, view_name: str, view_dict: dict
    ): ...

    def delete(self, namespace: str, name: str, tag: str, view_name: str): ...

    def add_sample(
        self,
        namespace: str,
        name: str,
        tag: str,
        view_name: str,
        sample_name: str,
    ): ...

    def remove_sample(
        self,
        namespace: str,
        name: str,
        tag: str,
        view_name: str,
        sample_name: str,
    ): ...
