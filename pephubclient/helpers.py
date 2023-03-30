import json
from typing import Optional, NoReturn
import requests

from pephubclient.exceptions import ResponseError


class RequestManager:
    @staticmethod
    def send_request(
        method: str,
        url: str,
        headers: Optional[dict] = None,
        cookies: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> requests.Response:
        return requests.request(
            method=method,
            url=url,
            verify=False,
            cookies=cookies,
            headers=headers,
            params=params,
        )

    @staticmethod
    def decode_response(response: requests.Response) -> str:
        """
        Decode the response from GitHub and pack the returned data into appropriate model.

        :param response: Response from GitHub.
        :return: Response data as an instance of correct model.
        """
        try:
            return response.content.decode("utf-8")
        except json.JSONDecodeError:
            raise ResponseError()


class MessageHandler:
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
