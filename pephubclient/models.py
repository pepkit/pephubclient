import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class ProjectDict(BaseModel):
    """
    Project dict (raw) model.

    Field names match the PEPHub raw-PEP payload and the peprs dialect
    (``config``/``samples``/``subsamples``), so no aliases are needed.
    """

    config: dict
    subsamples: list | None = None
    samples: list

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class ProjectUploadData(BaseModel):
    """
    Model used in post request to upload project.
    """

    pep_dict: ProjectDict
    tag: str | None = "default"
    is_private: bool | None = False
    overwrite: bool | None = False

    @field_validator("tag")
    def tag_should_not_be_none(cls, v: str | None) -> str:
        return v or "default"


class ProjectAnnotationModel(BaseModel):
    namespace: str
    name: str
    tag: str
    is_private: bool
    number_of_samples: int
    description: str
    last_update_date: datetime.datetime
    submission_date: datetime.datetime
    digest: str
    pep_schema: str | int | None = None
    pop: bool = False
    stars_number: int | None = 0
    forked_from: str | None = None


class SearchReturnModel(BaseModel):
    count: int
    limit: int
    offset: int
    results: list[ProjectAnnotationModel]
