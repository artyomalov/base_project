from fastapi import Response, status, Query
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from config import settings
from common import generate_url

from files.apps.user.services import (
    UserServices,
    AuthUserServices,
    user_services,
    auth_user_services,
)
from files.apps.user.schemas import (
    CreateUserSchema,
    UpdateUserPasswordSchema,
    UserSchema,
)


class GenerateURLS:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def _generate_urls(self, username: str):
        subdivision_url = generate_url(
            base_url=self.base_url,
            urls=["users", username],
        )

        return {
            "user_url": subdivision_url,
        }


class UserEndpoints(GenerateURLS):
    def __init__(
        self,
        services: UserServices,
        base_url: str,
    ):
        super().__init__(base_url=base_url)

        self.services = services

    async def list_users(
        self,
        request: Request,
        usernames: str | None = Query(
            default=None,
            description='string of usernames splitted by "|"',
            example="username|username",
        ),
        names: str | None = Query(
            default=None,
            description='string of names splitted by "|"',
            example="name|name",
        ),
        emails: str | None = Query(
            default=None,
            description='string of emails splitted by "|"',
            example="email|email",
        ),
        is_superuser: bool = Query(default=None),
        is_staff: bool = Query(default=None),
        is_active: bool = Query(default=None),
        limit: int | None = Query(default=20),
        offset: int | None = Query(default=0),
    ):
        if usernames:
            usernames = usernames.split("|")
        if names:
            names = names.split("|")
        if emails:
            emails = emails.split("|")

        users_dto = await self.services.list_users(
            usernames=usernames,
            names=names,
            emails=emails,
            is_superuser=is_superuser,
            is_staff=is_staff,
            is_active=is_active,
            limit=limit,
            offset=offset,
        )

        users_list_response = []
        for user in users_dto:
            urls = self._generate_urls(username=user.username)
            users_list_response.append({**user.model_dump(), "urls": urls})

        return JSONResponse(
            content=jsonable_encoder(users_list_response),
            status_code=status.HTTP_200_OK,
        )

    async def get_user(
        self,
        request: Request,
        username: str,
    ):

        user_dto = await self.services.get_user(username=username)

        urls = self._generate_urls(username=user_dto.username)

        return JSONResponse(
            content=jsonable_encoder({**user_dto.model_dump(), "urls": urls}),
            status_code=status.HTTP_200_OK,
        )

    async def create_user(self, request: Request, body: CreateUserSchema):
        user_dto = await self.services.create_user(data=body)

        urls = self._generate_urls(username=user_dto.username)

        return JSONResponse(
            content=jsonable_encoder({**user_dto.model_dump(), "urls": urls}),
            status_code=status.HTTP_201_CREATED,
        )

    async def update_user(
        self,
        request: Request,
        body: UserSchema,
    ):
        user_dto = await self.services.update_user(data=body)
        return JSONResponse(
            content=jsonable_encoder(user_dto), status_code=status.HTTP_200_OK
        )

    async def update_user_password(
        self,
        request: Request,
        username: str,
        body: UpdateUserPasswordSchema,
    ):
        await self.services.update_user_password(username=username, data=body)
        return Response(status_code=status.HTTP_200_OK)

    async def delete_user(self, request: Request, username: str):
        await self.services.delete_user(username=username)
        return Response(status_code=status.HTTP_204_NO_CONTENT)


class UserAuthEndpoints(GenerateURLS):
    def __init__(self, services: AuthUserServices, base_url: str):

        super().__init__(base_url=base_url)
        self.services = services

    async def issue_access_refresh_token_and_get_user_data(
        self, body: CreateUserSchema
    ):

        user_and_token_data_dict = (
            await self.services.issue_access_refresh_token_and_get_user_data(
                username=body.username, password=body.password
            )
        )

        urls = self._generate_urls(
            username=user_and_token_data_dict["user_data"]["username"]
        )

        user_and_token_data_dict["user_data"]["urls"] = urls

        return JSONResponse(
            jsonable_encoder({**user_and_token_data_dict}),
            status_code=status.HTTP_200_OK,
        )

    async def issue_new_access_if_refresh_is_valid(
        self,
        request: Request,
    ) -> JSONResponse:
        refresh = request.headers.get("authorization")
        access_token = await self.services.issue_new_access_if_refresh_is_valid(
            refresh.refresh_token
        )
        return JSONResponse(
            jsonable_encoder({"access": access_token}),
            status_code=status.HTTP_200_OK,
        )


user_auth_endpoints = UserAuthEndpoints(
    services=auth_user_services, base_url=settings.BASE_URL
)
user_endpoints = UserEndpoints(services=user_services, base_url=settings.BASE_URL)
