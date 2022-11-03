from enum import Enum


class ResponseStatusCodes(int, Enum):
    FORBIDDEN_403 = 403
    NOT_EXIST_404 = 404
    OK_200 = 200
