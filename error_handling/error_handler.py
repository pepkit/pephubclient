from error_handling.exceptions import AuthorizationPendingError
from typing import Union
import pydantic
from error_handling.models import GithubErrorModel
from contextlib import suppress


class ErrorHandler:
    @staticmethod
    def parse_github_response_error(github_response) -> Union[Exception, None]:
        with suppress(pydantic.ValidationError):
            GithubErrorModel(**github_response)
            return AuthorizationPendingError(
                message="You must first authorize with GitHub by using "
                "provided code."
            )
