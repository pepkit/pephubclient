import pathlib
from contextlib import suppress
import os
from typing import Optional
from pephubclient.constants import RegistryPath


class FilesManager:
    @staticmethod
    def save_jwt_data_to_file(path: str, jwt_data: str) -> None:
        pathlib.Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            f.write(jwt_data)

    @staticmethod
    def load_jwt_data_from_file(path: str) -> str:
        """
        Open the file with username and ID and load this data.
        """
        with suppress(FileNotFoundError):
            with open(path, "r") as f:
                return f.read()

    @staticmethod
    def delete_file_if_exists(filename: str) -> None:
        with suppress(FileNotFoundError):
            os.remove(filename)

    @staticmethod
    def save_pep_project(
        pep_project: str, registry_path: RegistryPath, filename: Optional[str] = None
    ) -> None:
        filename = filename or FilesManager._create_filename_to_save_downloaded_project(
            registry_path
        )
        with open(filename, "w") as f:
            f.write(pep_project)
        print(f"File downloaded -> {os.path.join(os.getcwd(), filename)}")

    @staticmethod
    def _create_filename_to_save_downloaded_project(registry_path: RegistryPath) -> str:
        """
        Takes query string and creates output filename to save the project to.

        Args:
            query_string: Query string that was used to find the project.

        Returns:
            Filename uniquely identifying the project.
        """
        filename = []

        if registry_path.namespace:
            filename.append(registry_path.namespace)
        if registry_path.item:
            filename.append(registry_path.item)

        filename = "_".join(filename)

        if registry_path.tag:
            filename = filename + ":" + registry_path.tag

        return filename + ".csv"
