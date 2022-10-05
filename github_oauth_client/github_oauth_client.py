import json
from typing import Union, Type
from error_handling.error_handler import ErrorHandler
import requests
from github_oauth_client.constants import (
    GITHUB_BASE_LOGIN_URL,
    GITHUB_OAUTH_ENDPOINT,
    GITHUB_VERIFICATION_CODES_ENDPOINT,
    GRANT_TYPE,
    HEADERS,
)
from github_oauth_client.models import (
    AccessTokenResponseModel,
    VerificationCodesResponseModel,
)
from pephubclient.models import ClientData
from pydantic import BaseModel, ValidationError
from error_handling.exceptions import ResponseError
from helpers import decode_response


class GitHubOAuthClient:
    """
    Class responsible for authorization with GitHub. By default authorization credentials will be saved

    It has following methods in public interface:
      - login: logs user in by creating credentials file with user data
      - logout: logs user out by deleting credentials file with user data
      - retrieve_logged_user_data: loads credentials file with user data into memory
    """

    def get_access_token(self, client_data: ClientData):
        device_code = self._get_device_verification_code(client_data)
        return self._request_github_for_access_token(device_code, client_data)

    def _get_device_verification_code(self, client_data: ClientData) -> str:
        """
        Send the request for verification codes, parse the response and return device code.

        Returns:
            Device code which is needed later to obtain the access code.
        """
        resp = GitHubOAuthClient._send_github_request(
            endpoint=GITHUB_VERIFICATION_CODES_ENDPOINT,
            params={"client_id": client_data.client_id},
        )
        verification_codes_response = self._parse_github_response(
            resp, VerificationCodesResponseModel
        )
        print(
            f"User verification code: {verification_codes_response.user_code}, "
            f"please enter the code here: {verification_codes_response.verification_uri}"
        )
        input()

        return verification_codes_response.device_code

    def _request_github_for_access_token(
        self, device_code: str, client_data: ClientData
    ) -> str:
        """
        Send the request for access token, parse the response and return access token.

        Args:
            device_code: Device code from verification codes request.

        Returns:
            Access token.
        """
        response = GitHubOAuthClient._send_github_request(
            endpoint=GITHUB_OAUTH_ENDPOINT,
            params={
                "client_id": client_data.client_id,
                "device_code": device_code,
                "grant_type": GRANT_TYPE,
            },
        )
        access_token_response = self._parse_github_response(
            response, AccessTokenResponseModel
        )
        return access_token_response.access_token

    @staticmethod
    def _send_github_request(
        endpoint: str, params: Union[dict, None] = None
    ) -> requests.Response:
        """
        Wrapper for sending the request to GitHub.

        Args:
            endpoint: String that will be added at the end of BASE_URL.
            params: Additional parameters.
            headers: Headers.

        Returns:
            GitHub response.
        """
        return requests.post(
            url=f"{GITHUB_BASE_LOGIN_URL}{endpoint}", headers=HEADERS, params=params
        )

    def _parse_github_response(
        self, response: requests.Response, model: Type[BaseModel]
    ):
        """
        Decode the response from GitHub and pack the returned data into appropriate model.

        Args:
            response: Response from GitHub.
            model: Model that the data will be packed to.

        Returns:
            Response data as an instance of correct model.
        """
        content = json.loads(decode_response(response))

        try:
            return model(**content)
        except ValidationError:
            raise ErrorHandler.parse_github_response_error(content) or ResponseError()
