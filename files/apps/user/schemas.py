from typing_extensions import Annotated
from pydantic import BaseModel, AfterValidator, ConfigDict

from files.apps.user.validators import validate_email, validate_string_is_not_empty


class CreateUserSchema(BaseModel):
    username: str = Annotated[str, AfterValidator(validate_email)]
    password: Annotated[str, AfterValidator(validate_string_is_not_empty)]


class UpdateUserPasswordSchema(BaseModel):
    username: str
    current_password: str
    new_password: str


class UserSchema(BaseModel):
    username: str
    email: Annotated[str | None, AfterValidator(validate_email)] = None
    password: bytes | None = None
    name: Annotated[str | None, AfterValidator(validate_string_is_not_empty)] = None
    avatar: str | None = None
    about: str | None = None
    phone_number: Annotated[
        str | None, AfterValidator(validate_string_is_not_empty)
    ] = None
    is_supeuser: bool | None = None
    is_staff: bool | None = None
    is_active: bool | None = None

    # model_config = ConfigDict(extra="allow")


class TokenDataSchema(BaseModel):
    access_token: Annotated[str, AfterValidator(validate_string_is_not_empty)]
    refresh_token: Annotated[str, AfterValidator(validate_string_is_not_empty)]


class UserLoginResponseSchema(BaseModel):
    token_data: TokenDataSchema
    user_data: UserSchema


# filter schema
class UserFilterSchema(BaseModel):
    username: list[str] | None = None
    name: str | None = None
    is_supeuser: bool = None
    is_staff: bool = None
    is_active: bool = None
    limit: int = (20,)
    offset: int = (0,)
