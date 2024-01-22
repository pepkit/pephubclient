import os
from contextlib import suppress
from pathlib import Path

import pandas
import yaml

from pephubclient.constants import RegistryPath
from pephubclient.exceptions import PEPExistsError


class FilesManager:
    @staticmethod
    def save_jwt_data_to_file(path: str, jwt_data: str) -> None:
        """
        Save jwt to provided path
        """
        Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
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
    def create_project_folder(
        registry_path: RegistryPath, parent_path: str, just_name: bool = False
    ) -> str:
        """
        Create new project folder

        :param registry_path: project registry path
        :param parent_path: parent path to create folder in
        :param just_name: if True, create folder with just name, not full path
        :return: folder_path
        """
        if just_name:
            folder_name = registry_path.item
        else:
            folder_name = FilesManager._create_filename_to_save_downloaded_project(
                registry_path
            )
        if parent_path:
            if not Path(parent_path).exists():
                raise OSError(f"Parent path does not exist. Provided path: {parent_path}")
        folder_path = os.path.join(parent_path or os.getcwd(), folder_name)
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        return folder_path

    @staticmethod
    def save_yaml(config: dict, full_path: str, not_force: bool = False):
        FilesManager.check_writable(path=full_path, force=not not_force)
        with open(full_path, "w") as outfile:
            yaml.dump(config, outfile, default_flow_style=False)

    @staticmethod
    def save_pandas(df: pandas.DataFrame, full_path: str, not_force: bool = False):
        FilesManager.check_writable(path=full_path, force=not not_force)
        df.to_csv(full_path, index=False)

    @staticmethod
    def file_exists(full_path: str) -> bool:
        return os.path.isfile(full_path)

    @staticmethod
    def delete_file_if_exists(filename: str) -> None:
        with suppress(FileNotFoundError):
            os.remove(filename)

    @staticmethod
    def _create_filename_to_save_downloaded_project(registry_path: RegistryPath) -> str:
        """
        Takes query string and creates output filename to save the project to.

        :param registry_path: Query string that was used to find the project.
        :return: Filename uniquely identifying the project.
        """
        filename = "_".join(filter(bool, [registry_path.namespace, registry_path.item]))
        if registry_path.tag:
            filename += f":{registry_path.tag}"
        return filename

    @staticmethod
    def check_writable(path: str, force: bool = True):
        if not force and os.path.isfile(path):
            raise PEPExistsError(f"File already exists and won't be updated: {path}")
