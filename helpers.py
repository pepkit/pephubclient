import json

import requests

from error_handling.exceptions import ResponseError
from github_oauth_client.constants import ENCODING


def decode_response(response: requests.Response) -> str:
    """
    Decode the response from GitHub and pack the returned data into appropriate model.

    Args:
        response: Response from GitHub.
        model: Model that the data will be packed to.

    Returns:
        Response data as an instance of correct model.
    """
    try:
        return response.content.decode(ENCODING)
    except json.JSONDecodeError:
        raise ResponseError()
