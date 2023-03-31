from pydantic import BaseModel, Field, Extra
from typing import Optional


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
    _tag: Optional[str] = "default"
    is_private: Optional[bool] = False
    overwrite: Optional[bool] = False

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, tag):
        if tag:
            self._tag = tag
        else:
            self._tag = "default"
