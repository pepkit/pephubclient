from enum import Enum
from typing import Optional

from pydantic import BaseModel, validator

# PEPHUB_BASE_URL = "https://pephub.databio.org/"
PEPHUB_BASE_URL = "http://0.0.0.0:8000/"
PEPHUB_PEP_API_BASE_URL = f"{PEPHUB_BASE_URL}api/v1/projects/"
PEPHUB_PUSH_URL = f"{PEPHUB_BASE_URL}api/v1/namespaces/{{namespace}}/projects/json"


class RegistryPath(BaseModel):
    protocol: Optional[str]
    namespace: str
    item: str
    subitem: Optional[str]
    tag: Optional[str] = "default"

    @validator("tag")
    def tag_should_not_be_none(cls, v):
        if v:
            return v
        return "default"


class ResponseStatusCodes(int, Enum):
    OK = 200
    ACCEPTED = 202
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_EXIST= 404
    CONFLICT = 409
    INTERNAL_ERROR = 500
