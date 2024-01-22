import json
from typing import Any, Callable, Optional
import os
import pandas as pd
from peppy.const import (
    NAME_KEY,
    DESC_KEY,
    CONFIG_KEY,
    SUBSAMPLE_RAW_LIST_KEY,
    SAMPLE_RAW_DICT_KEY,
)

import requests
from requests.exceptions import ConnectionError

from ubiquerg import parse_registry_path
from pydantic import ValidationError

from pephubclient.exceptions import PEPExistsError, ResponseError
from pephubclient.constants import RegistryPath
from pephubclient.files_manager import FilesManager


class RequestManager:
    @staticmethod
    def send_request(
        method: str,
        url: str,
        headers: Optional[dict] = None,
        cookies: Optional[dict] = None,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> requests.Response:
        return requests.request(
            method=method,
            url=url,
            verify=False,
            cookies=cookies,
            headers=headers,
            params=params,
            json=json,
        )

    @staticmethod
    def decode_response(response: requests.Response, encoding: str = "utf-8") -> str:
        """
        Decode the response from GitHub and pack the returned data into appropriate model.

        :param response: Response from GitHub.
        :param encoding: Response encoding [Default: utf-8]
        :return: Response data as an instance of correct model.
        """

        try:
            return response.content.decode(encoding)
        except json.JSONDecodeError as err:
            raise ResponseError(f"Error in response encoding format: {err}")


class MessageHandler:
    """
    Class holding print function in different colors
    """

    RED = 9
    YELLOW = 11
    GREEN = 40

    @staticmethod
    def print_error(text: str) -> None:
        print(f"\033[38;5;9m{text}\033[0m")

    @staticmethod
    def print_success(text: str) -> None:
        print(f"\033[38;5;40m{text}\033[0m")

    @staticmethod
    def print_warning(text: str) -> None:
        print(f"\033[38;5;11m{text}\033[0m")


def call_client_func(func: Callable[..., Any], **kwargs) -> Any:
    """
    Catch exceptions in functions called through cli.

    :param func: The function to call.
    :param kwargs: The keyword arguments to pass to the function.
    :return: The result of the function call.
    """

    try:
        func(**kwargs)
    except ConnectionError as err:
        MessageHandler.print_error(f"Failed to connect to server. Try later. {err}")
    except ResponseError as err:
        MessageHandler.print_error(f"{err}")
    except PEPExistsError as err:
        MessageHandler.print_warning(f"PEP already exists. {err}")
    except OSError as err:
        MessageHandler.print_error(f"{err}")


def is_registry_path(input_string: str) -> bool:
    """
    Check if input is a registry path to pephub
    :param str input_string: path to the PEP (or registry path)
    :return bool: True if input is a registry path
    """
    if input_string.endswith(".yaml"):
        return False
    try:
        RegistryPath(**parse_registry_path(input_string))
    except (ValidationError, TypeError):
        return False
    return True


def save_raw_pep(
    reg_path: str,
    project_dict: dict,
    force: bool = False,
) -> None:
    """
    Save project locally.

    :param dict project_dict: PEP dictionary (raw project)
    :param bool force: overwrite project if exists
    :return: None
    """
    reg_path_model = RegistryPath(**parse_registry_path(reg_path))
    folder_path = FilesManager.create_project_folder(registry_path=reg_path_model)

    def full_path(fn: str) -> str:
        return os.path.join(folder_path, fn)

    project_name = project_dict[CONFIG_KEY][NAME_KEY]
    sample_table_filename = "sample_table.csv"
    yaml_full_path = full_path(f"{project_name}_config.yaml")
    sample_full_path = full_path(sample_table_filename)
    if not force:
        extant = [p for p in [yaml_full_path, sample_full_path] if os.path.isfile(p)]
        if extant:
            raise PEPExistsError(f"{len(extant)} file(s) exist(s): {', '.join(extant)}")

    config_dict = project_dict.get(CONFIG_KEY)
    config_dict[NAME_KEY] = project_name
    config_dict[DESC_KEY] = project_dict[CONFIG_KEY][DESC_KEY]
    config_dict["sample_table"] = sample_table_filename

    sample_pandas = pd.DataFrame(project_dict.get(SAMPLE_RAW_DICT_KEY, {}))

    subsample_list = [
        pd.DataFrame(sub_a) for sub_a in project_dict.get(SUBSAMPLE_RAW_LIST_KEY) or []
    ]

    filenames = []
    for idx, subsample in enumerate(subsample_list):
        fn = f"subsample_table{idx + 1}.csv"
        filenames.append(fn)
        FilesManager.save_pandas(subsample, full_path(fn), not_force=False)
    config_dict["subsample_table"] = filenames

    FilesManager.save_yaml(config_dict, yaml_full_path, not_force=False)
    FilesManager.save_pandas(sample_pandas, sample_full_path, not_force=False)

    if config_dict.get("subsample_table"):
        for number, subsample in enumerate(subsample_list):
            FilesManager.save_pandas(
                subsample,
                os.path.join(folder_path, config_dict["subsample_table"][number]),
                not_force=False,
            )

    MessageHandler.print_success(
        f"Project was downloaded successfully -> {folder_path}"
    )
    return None
