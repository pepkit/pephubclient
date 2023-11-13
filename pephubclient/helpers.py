import json
from typing import Any, Callable, NoReturn, Optional

import requests
from requests.exceptions import ConnectionError

from ubiquerg import parse_registry_path
from pydantic.error_wrappers import ValidationError

from pephubclient.exceptions import PEPExistsError, ResponseError
from pephubclient.constants import RegistryPath


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
    def print_error(text: str) -> NoReturn:
        print(f"\033[38;5;9m{text}\033[0m")

    @staticmethod
    def print_success(text: str) -> NoReturn:
        print(f"\033[38;5;40m{text}\033[0m")

    @staticmethod
    def print_warning(text: str) -> NoReturn:
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
