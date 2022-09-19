from pydantic import BaseModel
from typing import Optional


PEPHUB_URL = "https://pephub.databio.org/pep/"


class RegistryPath(BaseModel):
    protocol: Optional[str]
    namespace: str
    item: str
    subitem: Optional[str]
    tag: Optional[str]
