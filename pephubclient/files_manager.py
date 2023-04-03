import os
import pathlib
from contextlib import suppress

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
    def crete_project_folder(registry_path: RegistryPath) -> str:
        """
        Create new project folder
        :param registry_path: project registry path
        :return: folder_path
        """
        folder_name = FilesManager._create_filename_to_save_downloaded_project(
            registry_path
        )
        folder_path = os.path.join(os.path.join(os.getcwd(), folder_name))
        pathlib.Path(folder_path).mkdir(parents=True, exist_ok=True)
        return folder_path

    @staticmethod
    def save_yaml(config: dict, full_path: str, force: bool = True):
        if FilesManager.file_exists(full_path) and not force:
            raise PEPExistsError("Yaml file already exists. File won't be updated")
        with open(full_path, "w") as outfile:
            yaml.dump(config, outfile, default_flow_style=False)

    @staticmethod
    def save_pandas(df: pandas.DataFrame, full_path: str, force: bool = True):
        if FilesManager.file_exists(full_path) and not force:
            raise PEPExistsError("Csv file already exists. File won't be updated")
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
        filename = []

        if registry_path.namespace:
            filename.append(registry_path.namespace)
        if registry_path.item:
            filename.append(registry_path.item)

        filename = "_".join(filename)

        if registry_path.tag:
            filename = filename + ":" + registry_path.tag

        return filename
