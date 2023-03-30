from typing import Optional
from enum import Enum
from pydantic import BaseModel

# PEPHUB_BASE_URL = "https://pephub.databio.org/"
PEPHUB_BASE_URL = "http://0.0.0.0:8000/"
PEPHUB_PEP_API_BASE_URL = f"{PEPHUB_BASE_URL}api/v1/projects/"
PEPHUB_PUSH_URL = f"{PEPHUB_BASE_URL}api/v1/namespaces/{{namespace}}/projects/json"


class RegistryPath(BaseModel):
    protocol: Optional[str]
    namespace: str
    item: str
    subitem: Optional[str]
    tag: Optional[str]


class ResponseStatusCodes(int, Enum):
    FORBIDDEN_403 = 403
    NOT_EXIST_404 = 404
    OK_200 = 200
