from typing import Any
from typing_extensions import Annotated
from datetime import datetime, UTC
from pydantic import BaseModel, AfterValidator, ConfigDict

from files.apps.subdivision.enums import DepartmentEnum
from files.apps.user.validators import validate_string_is_not_empty


class EmployeeSchema(BaseModel):
    user: str
    subdivision: int


class BaseSubdivisionSchema(BaseModel):
    name: Annotated[str, AfterValidator(validate_string_is_not_empty)]
    description: Annotated[str | None, AfterValidator(validate_string_is_not_empty)] = (
        None
    )
    department: DepartmentEnum


class SubdivisionSchema(BaseSubdivisionSchema):
    subdivision_id: int
    creation_time: datetime | None = None


class BaseProjectSchema(BaseModel):
    name: Annotated[str, AfterValidator(validate_string_is_not_empty)]
    completed: bool = False
    start_time: datetime | None = None
    complete_time: datetime | None = None
    description: Annotated[str | None, AfterValidator(validate_string_is_not_empty)] = (
        None
    )


class ProjectSchema(BaseProjectSchema):
    project_id: int
    subdivision_id: int


# Response models
class SubdivisionUrlsSchema(BaseModel):
    subdivision_url: str
    projects_url: str
    employees_url: str


class SubdivisionResponseSchema(SubdivisionSchema):
    urls: SubdivisionUrlsSchema


class ProjectUrlsSchema(BaseModel):
    project_url: str


class ProjectResponseSchema(SubdivisionSchema):
    urls: SubdivisionUrlsSchema
