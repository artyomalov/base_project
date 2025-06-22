from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response

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


class UserEndpoints:
    def __init__(self, services: UserServices):
        self.services = services

    async def get_users(
        self,
        request: Request,
        filter=None,
        limit=20,
        offset=0,
    ):

        users = await self.services.get_users(
            filter=filter,
            limit=limit,
            offset=offset,
        )

        return JSONResponse(
            content=(users),
            status_code=status.HTTP_200_OK,
        )

    async def get_user(
        self,
        request: Request,
        user_id: int,
    ):

        user = await self.services.get_user(user_id=user_id)
        return JSONResponse(
            content=(user),
            status_code=status.HTTP_200_OK,
        )

    async def create_user(self, request: Request, body: CreateUserSchema):
        user = await self.services.create_user(data=body)
        return JSONResponse(
            content=user,
            status_code=status.HTTP_201_CREATED,
        )

    async def update_user(
        self,
        request: Request,
        body: UserSchema,
    ):
        await self.services.update_user(data=body)
        return Response(status_code=status.HTTP_200_OK)

    async def update_user_password(
        self,
        request: Request,
        body: UpdateUserPasswordSchema,
    ):
        await self.services.update_user_password(data=body)
        return Response(status_code=status.HTTP_200_OK)

    async def delete_user(self, request: Request, user_id: int):
        await self.services.delete_user(user_id=user_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)


class UserAuthEndpoints:
    def __init__(
        self,
        services: AuthUserServices,
    ):
        self.services = services

    async def issue_access_refresh_token_and_get_user_data(
        self, body: CreateUserSchema
    ):

        user_and_token_data_dict = (
            await self.services.issue_access_refresh_token_and_get_user_data(
                email=body.email, password=body.password
            )
        )

        return JSONResponse(
            jsonable_encoder(user_and_token_data_dict),
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


user_auth_endpoints = UserAuthEndpoints(services=auth_user_services)
user_endpoints = UserEndpoints(services=user_services)
