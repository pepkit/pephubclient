from ..files_manager import FilesManager


class Samples:
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
