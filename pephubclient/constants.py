from typing import Optional

from pydantic import BaseModel

PEPHUB_BASE_URL = "https://pephub.databio.org/pep/"


class RegistryPath(BaseModel):
    protocol: Optional[str]
    namespace: str
    item: str
    subitem: Optional[str]
    tag: Optional[str]
