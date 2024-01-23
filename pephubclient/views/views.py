class Views:
    def __init__(self, jwt_data: str):
        self._jwt_data = jwt_data

    def get(self, namespace: str, name: str, tag: str, view_name: str):
        ...

    def create(
        self, namespace: str, name: str, tag: str, view_name: str, view_dict: dict
    ):
        ...

    def delete(self, namespace: str, name: str, tag: str, view_name: str):
        ...

    def add_sample(
        self,
        namespace: str,
        name: str,
        tag: str,
        view_name: str,
        sample_name: str,
    ):
        ...

    def remove_sample(
        self,
        namespace: str,
        name: str,
        tag: str,
        view_name: str,
        sample_name: str,
    ):
        ...
