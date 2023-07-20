from typing import Optional

import pydantic
from pydantic import BaseModel, Extra, Field
from peppy.const import CONFIG_KEY, SUBSAMPLE_RAW_LIST_KEY, SAMPLE_RAW_DICT_KEY


class ProjectDict(BaseModel):
    """
    Project dict (raw) model
    """

    config: dict = Field(alias=CONFIG_KEY)
    subsample_list: Optional[list] = Field(alias=SUBSAMPLE_RAW_LIST_KEY)
    sample_list: list = Field(alias=SAMPLE_RAW_DICT_KEY)

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
