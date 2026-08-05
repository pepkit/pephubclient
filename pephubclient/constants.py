import os
from enum import Enum

from pydantic import BaseModel, field_validator

DEFAULT_BASE_URL: str = "https://pephub-api.databio.org/"
PEPHUB_BASE_URL: str = os.getenv("PEPHUB_BASE_URL", default=DEFAULT_BASE_URL)
# PEPHUB_BASE_URL = "http://0.0.0.0:8000/"

PEPHUB_SAMPLE_URL: str = f"{PEPHUB_BASE_URL}api/v1/projects/{{namespace}}/{{project}}/samples/{{sample_name}}"
PEPHUB_VIEW_URL: str = (
    f"{PEPHUB_BASE_URL}api/v1/projects/{{namespace}}/{{project}}/views/{{view_name}}"
)
PEPHUB_VIEW_SAMPLE_URL: str = f"{PEPHUB_BASE_URL}api/v1/projects/{{namespace}}/{{project}}/views/{{view_name}}/{{sample_name}}"


class RegistryPath(BaseModel):
    protocol: str | None = None
    namespace: str
    item: str
    subitem: str | None = None
    tag: str | None = "default"

    @field_validator("tag")
    def tag_should_not_be_none(cls, v: str | None) -> str:
        return v or "default"


class CachedToken(BaseModel):
    """Credentials persisted to the TOML cache file."""

    token: str | None = None
    base_url: str = DEFAULT_BASE_URL


class ResponseStatusCodes(int, Enum):
    OK = 200
    ACCEPTED = 202
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_EXIST = 404
    CONFLICT = 409
    INTERNAL_ERROR = 500


USER_DATA_FILE_NAME: str = "jwt.toml"

PH_HOME: str | None = os.getenv("PH_HOME")
if PH_HOME:
    _CACHE_DIR = PH_HOME
else:
    HOME_PATH = os.getenv("HOME") or os.path.expanduser("~")
    _CACHE_DIR = os.path.join(HOME_PATH, ".pephubclient")
PATH_TO_TOKEN_FILE: str = os.path.join(_CACHE_DIR, USER_DATA_FILE_NAME)
