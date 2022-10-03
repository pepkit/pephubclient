from typing import Optional
from pydantic import BaseModel

PEPHUB_BASE_URL = "https://pephub.databio.org/pep/"
DEFAULT_FILENAME = "pep_project.csv"


class RegistryPath(BaseModel):
    protocol: Optional[str]
    namespace: str
    item: str
    subitem: Optional[str]
    tag: Optional[str]
