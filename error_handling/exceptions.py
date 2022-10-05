class BasePephubclientException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class IncorrectQueryStringError(BasePephubclientException):
    def __init__(self, query_string: str = None):
        self.query_string = query_string
        super().__init__(
            f"PEP data with passed namespace and project ({self.query_string}) name not found."
        )


class ResponseError(BasePephubclientException):
    default_message = "The response looks incorrect and must be verified manually."

    def __init__(self, message: str = None):
        super().__init__(message or self.default_message)


class AuthorizationPendingError(BasePephubclientException):
    ...
