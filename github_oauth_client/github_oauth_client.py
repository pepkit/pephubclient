import json
from typing import Type
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
from helpers import RequestManager


class GitHubOAuthClient(RequestManager):
    """
    Class responsible for authorization with GitHub.
    """

    def get_access_token(self, client_data: ClientData):
        """
        Requests user with specified ClientData.client_id to enter the verification code, and then
        responds with GitHub access token.
        """
        device_code = self._get_device_verification_code(client_data)
        return self._request_github_for_access_token(device_code, client_data)

    def _get_device_verification_code(self, client_data: ClientData) -> str:
        """
        Send the request for verification codes, parse the response and return device code.

        Returns:
            Device code which is needed later to obtain the access code.
        """
        resp = GitHubOAuthClient.send_request(
            method="POST",
            url=f"{GITHUB_BASE_LOGIN_URL}{GITHUB_VERIFICATION_CODES_ENDPOINT}",
            params={"client_id": client_data.client_id},
            headers=HEADERS,
        )
        verification_codes_response = self._handle_github_response(
            resp, VerificationCodesResponseModel
        )
        print(
            f"User verification code: {verification_codes_response.user_code}, "
            f"please enter the code here: {verification_codes_response.verification_uri} and"
            f"hit enter when you are done with authentication on the website"
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
        response = GitHubOAuthClient.send_request(
            method="POST",
            url=f"{GITHUB_BASE_LOGIN_URL}{GITHUB_OAUTH_ENDPOINT}",
            params={
                "client_id": client_data.client_id,
                "device_code": device_code,
                "grant_type": GRANT_TYPE,
            },
            headers=HEADERS,
        )
        return self._handle_github_response(
            response, AccessTokenResponseModel
        ).access_token

    @staticmethod
    def _handle_github_response(response: requests.Response, model: Type[BaseModel]):
        """
        Decode the response from GitHub and pack the returned data into appropriate model.

        Args:
            response: Response from GitHub.
            model: Model that the data will be packed to.

        Returns:
            Response data as an instance of correct model.
        """
        try:
            content = json.loads(GitHubOAuthClient.decode_response(response))
        except json.JSONDecodeError:
            raise ResponseError("Something went wrong with GitHub response")

        try:
            return model(**content)
        except ValidationError:
            raise ErrorHandler.parse_github_response_error(content) or ResponseError()
