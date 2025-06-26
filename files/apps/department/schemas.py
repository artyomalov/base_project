from typing_extensions import Annotated
from datetime import datetime, UTC
from pydantic import BaseModel, AfterValidator, ConfigDict
from enums import DepartmentEnum
from files.apps.user.validators import validate_string_is_not_empty


class SubdivisionSchema(BaseModel):
    subdivision_id: int
    name: Annotated[str, AfterValidator(validate_string_is_not_empty)]
    description: Annotated[str | None, AfterValidator(validate_string_is_not_empty)] = (
        None
    )
    creation_time: datetime
    department: DepartmentEnum

    employees_link: Annotated[
        str | None, AfterValidator(validate_string_is_not_empty)
    ] = None
    subdivision_link: Annotated[
        str | None, AfterValidator(validate_string_is_not_empty)
    ] = None
    projects_link: Annotated[
        str | None, AfterValidator(validate_string_is_not_empty)
    ] = None


class ProjectSchema(BaseModel):
    project_id: int
    name: Annotated[str, AfterValidator(validate_string_is_not_empty)] = None
    completed: bool = False
    start_time: datetime
    complete_time: datetime | None = None
    description: Annotated[str | None, AfterValidator(validate_string_is_not_empty)] = (
        None
    )

    project_link: Annotated[
        str | None, AfterValidator(validate_string_is_not_empty)
    ] = None
    subdivision_link: Annotated[
        str | None, AfterValidator(validate_string_is_not_empty)
    ] = None
