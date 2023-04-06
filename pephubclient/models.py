from typing import Optional

import pydantic
from pydantic import BaseModel, Extra, Field


class ProjectDict(BaseModel):
    """
    Project dict (raw) model
    """

    description: Optional[str] = ""
    config: dict = Field(alias="_config")
    subsample_dict: Optional[list] = Field(alias="_subsample_dict")
    name: str
    sample_dict: dict = Field(alias="_sample_dict")

    class Config:
        allow_population_by_field_name = True
        extra = Extra.allow


class ProjectUploadData(BaseModel):
    """
    Model used in post request to upload project
    """

    pep_dict: ProjectDict
    tag: Optional[str] = "default"
    is_private: Optional[bool] = False
    overwrite: Optional[bool] = False

    @pydantic.validator("tag")
    def tag_should_not_be_none(cls, v):
        return v or "default"
