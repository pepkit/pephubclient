import json
from exceptions import GitHubResponseError
from typing import Type

import requests
from pydantic import BaseModel, ValidationError

from github_oauth_client.constants import (
    ENCODING,
    GITHUB_BASE_LOGIN_URL,
    GITHUB_CLIENT_CODE,
    GITHUB_OAUTH_ENDPOINT,
    GITHUB_VERIFICATION_CODES_ENDPOINT,
    GRANT_TYPE,
    HEADERS,
)
from github_oauth_client.models import (
    AccessTokenResponseModel,
    VerificationCodesResponseModel,
)


class GitHubOAuthClient:
    """
    Class responsible for authorization with GitHub.
    """

    def __init__(self):
        self.access_token: str = ""

    def login(self):
        """
        Login user using OAuth2.
        """
        device_code = self.get_device_verification_code()
        access_token = self.get_access_token(device_code)
        self.access_token = access_token

    def get_device_verification_code(self) -> str:
        """
        Send the request for verification codes, parse the response and return device code.

        Returns:
            Device code which is needed later to obtain the access code.
        """
        resp = self.send_github_request(
            endpoint=GITHUB_VERIFICATION_CODES_ENDPOINT,
            params={"client_id": GITHUB_CLIENT_CODE},
        )
        verification_codes_response = self._parse_github_response(
            resp, VerificationCodesResponseModel
        )
        print(
            f"User verification code: {verification_codes_response.user_code}, "
            f"please enter the code here: {verification_codes_response.verification_uri}"
        )
        # TODO: implement the following logic: if user closes the tab, then proceed with the program
        input()
        return verification_codes_response.device_code

    def get_access_token(self, device_code: str) -> str:
        """
        Send the request for access token, parse the response and return access token.

        Args:
            device_code: Device code from verification codes request.

        Returns:
            Access token.
        """
        resp = self.send_github_request(
            endpoint=GITHUB_OAUTH_ENDPOINT,
            params={
                "client_id": GITHUB_CLIENT_CODE,
                "device_code": device_code,
                "grant_type": GRANT_TYPE,
            },
        )
        access_token_response = self._parse_github_response(
            resp, AccessTokenResponseModel
        )
        return access_token_response.access_token

    @staticmethod
    def send_github_request(endpoint: str, params: dict) -> requests.Response:
        """
        Wrapper for sending the request to GitHub.

        Args:
            endpoint: String that will be added at the end of BASE_URL.
            params: Additional parameters.

        Returns:
            GitHub response.
        """
        return requests.post(
            url=f"{GITHUB_BASE_LOGIN_URL}{endpoint}", headers=HEADERS, params=params
        )

    @staticmethod
    def _parse_github_response(response: requests.Response, model: Type[BaseModel]):
        """
        Decode the response from GitHub and pack the returned data into appropriate model.

        Args:
            response: Response from GitHub.
            model: Model that the data will be packed to.

        Returns:
            Response data as an instance of correct model.
        """
        try:
            content = json.loads(response.content.decode(ENCODING))
            return model(**content)
        except (json.JSONDecodeError, ValidationError):
            raise GitHubResponseError()
