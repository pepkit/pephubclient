from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Union, List
import datetime


class PaginationResult(BaseModel):
    page: int = 0
    page_size: int = 10
    total: int


class SchemaVersionAnnotation(BaseModel):
    """
    Schema version annotation model
    """

    namespace: str
    schema_name: str
    version: str
    contributors: Optional[str] = ""
    release_notes: Optional[str] = ""
    tags: Dict[str, Union[str, None]] = {}
    release_date: datetime.datetime
    last_update_date: datetime.datetime


class SchemaVersionResult(BaseModel):
    pagination: PaginationResult
    results: List[SchemaVersionAnnotation]


class NewSchemaVersionModel(BaseModel):
    """
    Model for creating a new schema version from json
    """

    contributors: Union[str, None] = None
    release_notes: Union[str, None] = None
    tags: Optional[Union[List[str], str, Dict[str, str], List[Dict[str, str]]]] = (
        None,
    )
    version: str
    schema_value: dict

    model_config = ConfigDict(extra="forbid")


class NewSchemaRecordModel(NewSchemaVersionModel):
    """
    Model for creating a new schema record from json
    """

    schema_name: str
    description: Union[str, None] = None
    maintainers: Union[str, None] = None
    lifecycle_stage: Union[str, None] = None
    private: bool = False

    model_config = ConfigDict(extra="forbid")


class UpdateSchemaRecordFields(BaseModel):
    maintainers: Optional[Union[str, None]] = None
    lifecycle_stage: Optional[Union[str, None]] = None
    private: Optional[bool] = None
    name: Optional[Union[str, None]] = None
    description: Optional[Union[str, None]] = None

    model_config = ConfigDict(extra="forbid")


class UpdateSchemaVersionFields(BaseModel):
    contributors: Optional[Union[str, None]] = None
    schema_value: Optional[Union[str, None]] = None
    release_notes: Optional[Union[str, None]] = None

    model_config = ConfigDict(extra="forbid")
