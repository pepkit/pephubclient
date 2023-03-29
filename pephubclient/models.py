from pydantic import BaseModel, Field, Extra
from typing import Optional


class JWTDataResponse(BaseModel):
    jwt_token: str


class ClientData(BaseModel):
    client_id: str


class ProjectDict(BaseModel):
    """
    Project dict (raw) model
    """
    description: Optional[str] = ""
    config: dict = Field(alias="_config")
    subsample_dict: Optional[dict] = Field(alias="_subsample_dict")
    name: str
    sample_dict: dict = Field(alias="_sample_dict")

    class Config:
        allow_population_by_field_name = True
        extra = Extra.allow
