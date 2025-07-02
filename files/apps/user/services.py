from config import settings

from fastapi import Request

from files.apps.user.schemas import (
    UpdateUserPasswordSchema,
    UserSchema,
    CreateUserSchema,
)
from files.apps.user.repository import (
    UserRepository,
    UserAuthRepository,
    user_repository,
    user_auth_repository,
)
from files.apps.user.utils import (
    PasswordHandlingUtil,
    JWTCreatorUtil,
    generate_image_url,
    generate_image_uuid_name,
    jwt_actions_util,
    save_base64_image_to_fs,
)
from files.exceptions import (
    IsNotActiveError,
    ValidationError,
    DoesNotExistError,
    JWTTokenHasNotBeenProvidedError,
    InvalidPasswordError,
    UnprocessableEntityError,
)


class AuthUserServices:
    def __init__(
        self,
        repository: UserRepository,
    ):
        self.repository = repository

    async def _get_user_and_check_if_user_is_active(
        self,
        username: str,
    ) -> UserSchema:
        user_data_dto: UserSchema = await self.repository.get_user(
            username=username,
            load_password=True,
        )

        if not user_data_dto:
            raise DoesNotExistError("User does not exist")

        if not user_data_dto.is_active:
            raise IsNotActiveError("User has been disabled")

        return user_data_dto

    async def issue_access_refresh_token_and_get_user_data(
        self, username: str, password: str
    ) -> dict:
        user_data_dto: UserSchema = await self._get_user_and_check_if_user_is_active(
            username=username
        )

        password_is_valid = PasswordHandlingUtil.validate_password(
            password=password, hashed_password=user_data_dto.password
        )

        if not password_is_valid:
            raise InvalidPasswordError()

        jwt_creator = JWTCreatorUtil(
            username=user_data_dto.username,
            access_token_expire_time=settings.auth_jwt.ACCESS_TOKEN_EXPIRE_TIME,
            refresh_token_expire_time=settings.auth_jwt.REFRESH_TOKEN_EXPIRE_TIME,
        )

        return {
            "user_data": user_data_dto.model_dump(
                exclude={
                    "password",
                }
            ),
            "token_data": {
                "access": jwt_creator.create_access_token(),
                "refresh": jwt_creator.create_refresh_token(),
            },
        }

    async def issue_new_access_if_refresh_is_valid(self, token: bytes) -> bytes:
        token_data = jwt_actions_util.decode_jwt(token=token)
        token_type = token_data.get("token_type")

        if not token_type:
            raise DoesNotExistError("Token_type has not been provided")
        if token_type == settings.auth_jwt.ACCESS_TOKEN_TYPE:
            raise ValidationError("Invalid token type")

        username = token_data.get("sub")
        user_dto = await self._get_user_and_check_if_user_is_active(username=username)

        jwt_creator = JWTCreatorUtil(
            username=user_dto.username,
            access_token_expire_time=settings.auth_jwt.ACCESS_TOKEN_EXPIRE_TIME,
            refresh_token_expire_time=settings.auth_jwt.REFRESH_TOKEN_EXPIRE_TIME,
        )

        return jwt_creator.create_access_token()


class VerifyUserServices:
    def __init__(self, repository: UserAuthRepository):
        self.repository = repository

    def get_token_and_check_if_it_is_not_none(self, request: Request = None) -> str:
        authorization_header = request.headers.get("authorization")
        if not authorization_header:
            raise JWTTokenHasNotBeenProvidedError(
                class_name=self.__class__.__name__,
                method_name=self.get_token_and_check_if_it_is_not_none.__name__,
            )

        jwt_access_token = authorization_header.split(" ")[1]
        return jwt_access_token

    def check_payload_type(self, payload: dict) -> dict:
        if payload.get("related_entity_type") == settings.auth_jwt.REFRESH_TOKEN_TYPE:
            raise ValidationError(
                f"Invalid token record_type",
            )

        return payload

    async def get_user_from_db(self, payload: dict):
        username: str | None = payload.get("sub")
        user_id_is_main_is_active_dto = await self.repository.get_user_id_and_status(
            username=username
        )

        return user_id_is_main_is_active_dto

    async def verify_user_access_token_and_get_username_is_active_is_admin(
        self, contain_token_data: Request | str
    ):
        """
        Extracts access token from request object if provided data is instance
        of Request adn verify that access token is valid. If provided data is
        instance of str, just verify token
        """
        jwt_access_token = contain_token_data
        if isinstance(jwt_access_token, Request):
            jwt_access_token = self.get_token_and_check_if_it_is_not_none(
                request=contain_token_data
            )
        payload = jwt_actions_util.decode_jwt(token=jwt_access_token)
        payload = self.check_payload_type(payload=payload)

        user_username_is_main_is_active_dto = await self.get_user_from_db(
            payload=payload
        )

        if not user_username_is_main_is_active_dto.is_active:
            raise IsNotActiveError()

        return user_username_is_main_is_active_dto


class UserServices:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    @staticmethod
    def _hash_user_password(password: str) -> bytes:
        hashed_password: bytes = PasswordHandlingUtil.hash_password(password=password)
        return hashed_password

    async def get_user(self, username: str) -> UserSchema:
        user = await self.repository.get_user(username=username)
        return user

    async def list_users(
        self,
        usernames: list[str] | None = None,
        names: list[str] | None = None,
        emails: list[str] | None = None,
        is_superuser: bool = None,
        is_staff: bool = None,
        is_active: bool = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[UserSchema]:
        users_dto = await self.repository.list_users(
            usernames=usernames,
            names=names,
            emails=emails,
            is_superuser=is_superuser,
            is_staff=is_staff,
            is_active=is_active,
            limit=limit,
            offset=offset,
        )

        return users_dto

    async def create_user(
        self,
        data: CreateUserSchema,
    ) -> UserSchema:
        username = data.username
        password = data.password

        if not username:
            raise UnprocessableEntityError(
                message="Username has not been provided",
                class_name=self.__class__.__name__,
                method_name=self.create_user.__name__,
            )
        if not password:
            raise UnprocessableEntityError(
                message="Password has not been provided",
                class_name=self.__class__.__name__,
                method_name=self.create_user.__name__,
            )

        hashed_password = self._hash_user_password(password=password)
        data.password = hashed_password

        print("create", ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        user_dto = await self.repository.create_user(data=data)

        return user_dto

    async def update_user(
        self,
        data: UserSchema,
    ) -> None:

        if (
            data.is_staff is not None
            or data.is_active is not None
            or data.is_supeuser is not None
        ):
            raise UnprocessableEntityError(
                message="is_staff/is_active/is_supeuser field can't be updated by this method. Please use appropriate \
                method to update this data",
                class_name=self.__class__.__name__,
                method_name=self.update_user.__name__,
            )

        if data.avatar is None:
            await self.repository.update_user(data=data)
        else:
            image_name = generate_image_uuid_name(settings.IMAGE_AVATAR_TYPE)
            avatar = generate_image_url(
                image_name=image_name,
                image_type=settings.IMAGE_AVATAR_TYPE,
            )
            data.avatar = avatar

            await self.repository.update_user(data=data)
            await save_base64_image_to_fs(
                base64_string=avatar,
                image_name=image_name,
                path_to_fs_directory="avatars",
            )

    async def update_user_password(self, data: UpdateUserPasswordSchema) -> None:
        if not data.current_password or not data.new_password:
            raise UnprocessableEntityError(
                message="Password data has not been provided",
                class_name=self.__class__.__name__,
                method_name=self.update_user.__name__,
            )

        hashed_current_password = await self.repository.get_user_password(
            username=data.username
        )

        current_password_is_valid = PasswordHandlingUtil.validate_password(
            password=data.current_password,
            hashed_password=hashed_current_password,
        )
        if not current_password_is_valid:
            raise InvalidPasswordError()

        hashed_password = self._hash_user_password(password=data.new_password)

        await self.repository.update_user_password(
            username=data.username,
            new_password=hashed_password,
        )

    async def delete_user(
        self,
        username: int,
    ) -> None:
        await self.repository.delete_user(username=username)


auth_user_services = AuthUserServices(repository=user_repository)
verify_user_services = VerifyUserServices(repository=user_auth_repository)
user_services = UserServices(repository=user_repository)
