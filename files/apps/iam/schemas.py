from typing_extensions import Annotated
from pydantic import BaseModel, AfterValidator

from files.apps.iam.validators import validate_email, string_is_not_empty_validator


class CreateUserSchema(BaseModel):
    email: str = Annotated[str, AfterValidator(validate_email)]
    password: str


class UserSchema(BaseModel):
    user_id: int

    email: Annotated[str | None, AfterValidator(validate_email)] = None

    name: Annotated[str | None, AfterValidator(string_is_not_empty_validator)] = None
    avatar: str | None = None
    about: str | None = None
    phone_number: Annotated[
        str | None, AfterValidator(string_is_not_empty_validator)
    ] = None

    is_supeuser: bool | None = None
    is_staff: bool | None = None
    is_active: bool | None = None
