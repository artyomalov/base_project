from config import settings

from fastapi import Request

from files.apps.iam.db_requests import UserDbRequests, user_db_requests
from files.apps.iam.utils import PasswordHandlingUtil, JWTCreatorUtil, jwt_actions_util
from files.exceptions import (
    IsNotActiveError,
    ValidationError,
    DoesNotExistError,
    JWTTokenHasNotBeenProvidedError,
    InvalidPasswordError,
)


class AuthUserServices:
    def __init__(
        self,
        db_requests: UserDbRequests,
    ):
        self.db_requests = db_requests

    async def _get_user_and_check_if_user_is_active(
        self, username: str
    ) -> "UserSchema":
        user_data_dto = await self.db_requests.get_user(
            username=username, load_password_flag=True
        )

        if not user_data_dto:
            raise DoesNotExistError("User does not exist")

        if not user_data_dto.is_active:
            raise IsNotActiveError("User has been disabled")

        return user_data_dto

    async def issue_access_refresh_token_and_get_user_data(
        self, username: str, password: str
    ) -> dict:
        user_data_dto = await self._get_user_and_check_if_user_is_active(
            username=username
        )

        password_is_valid = PasswordHandlingUtil.validate_password(
            password=password, hashed_password=user_data_dto.password
        )

        if not password_is_valid:
            raise InvalidPasswordError()

        jwt_creator = JWTCreatorUtil(
            username=username,
            access_token_expire_time=settings.auth_jwt.access_token_expire_time,
            refresh_token_expire_time=settings.auth_jwt.refresh_token_expire_time,
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
            access_token_expire_time=settings.auth_jwt.access_token_expire_time,
            refresh_token_expire_time=settings.auth_jwt.refresh_token_expire_time,
            username=user_dto.username,
        )

        return jwt_creator.create_access_token()


class VerifyUserService:
    def __init__(self, db_requests):
        self.db_requests = db_requests

    @staticmethod
    def get_token_and_check_if_it_is_not_none(request: Request = None) -> str:
        authorization_header = request.headers.get("authorization")
        if not authorization_header:
            raise JWTTokenHasNotBeenProvidedError()

        jwt_access_token = authorization_header.split(" ")[1]
        return jwt_access_token

    @staticmethod
    def check_payload_type(payload: dict) -> dict:
        if payload.get("related_entity_type") == settings.auth_jwt.REFRESH_TOKEN_TYPE:
            raise ValidationError(
                f"Invalid token record_type",
            )

        return payload

    async def get_user_from_db(self, payload: dict):
        username: str | None = payload.get("sub")
        user_id_is_main_is_active_dto = (
            await self.db_requests.get_user_id_and_status_db_request(username=username)
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


auth_user_services = AuthUserServices(
    db_requests=user_db_requests,
)
verify_user_service = VerifyUserService(db_requests=user_auth_db_requests)
