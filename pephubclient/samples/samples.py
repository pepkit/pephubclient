from ..files_manager import FilesManager


class Samples:
    """
    Class for managing samples in PEPhub and provides methods for
        getting, creating, updating and removing samples.
    This class is not related to peppy.Sample class.
    """

    def __init__(self):
        self.jwt_data = ""

    def get(
        self,
        namespace: str,
        name: str,
        tag: str,
        sample_name: str = None,
    ):
        ...

    def create(
        self,
        namespace: str,
        name: str,
        tag: str,
        sample_name: str,
        sample_dict: dict,
    ):
        ...

    def update(
        self,
        namespace: str,
        name: str,
        tag: str,
        sample_name: str,
        sample_dict: dict,
    ):
        ...

    def remove(self, namespace: str, name: str, tag: str, sample_name: str):
        ...
