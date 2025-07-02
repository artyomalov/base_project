from fastapi import APIRouter

from files.apps.user.schemas import (
    UserLoginResponseSchema,
    UserResponseSchema,
    UserSchema,
)
from files.apps.user.endpoints import user_endpoints, user_auth_endpoints


user_auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)
user_router = APIRouter(
    prefix="/users",
    tags=["user"],
)


user_auth_router.add_api_route(
    path="/login",
    methods=["POST"],
    endpoint=user_auth_endpoints.issue_access_refresh_token_and_get_user_data,
    response_model=UserLoginResponseSchema,
    summary="Login",
    description="Returns user data with urls and refresh/ access token",
)
user_auth_router.add_api_route(
    path="/refresh",
    methods=["POST"],
    endpoint=user_auth_endpoints.issue_new_access_if_refresh_is_valid,
    response_model=str,
    summary="Generate access",
    description="Generates new access token by valid refresh token",
)


user_router.add_api_route(
    methods=["GET"],
    endpoint=user_endpoints.list_users,
    path="",
    response_model=list[UserResponseSchema],
    summary="Get user",
    description="Lists users, with or without offset/limit/filter params",
)
user_router.add_api_route(
    methods=["GET"],
    endpoint=user_endpoints.get_user,
    path="/{username}",
    response_model=UserResponseSchema,
    summary="Get one user",
    description="Gets user by it's username",
)
user_router.add_api_route(
    methods=["POST"],
    endpoint=user_endpoints.create_user,
    path="",
    response_model=UserResponseSchema,
    summary="Create user",
    description="Creates new user with provided credentials",
)
user_router.add_api_route(
    methods=["PATCH"],
    endpoint=user_endpoints.update_user,
    path="/{username}",
    response_model=None,
    summary="Update user",
    description="Updates user data and avatar.\
        Does not update is_active, is_staff, \
        is_superuser fields",
)
user_router.add_api_route(
    methods=["PATCH"],
    endpoint=user_endpoints.update_user_password,
    path="/{username}/password",
    response_model=None,
    summary="Update user's password",
    description="Hashes and updates user's password",
)
user_router.add_api_route(
    methods=["DELETE"],
    endpoint=user_endpoints.delete_user,
    path="/{username}",
    response_model=None,
    summary="Deletes user",
    description="Deletes user and all related user's data from database",
)


# class UserRoutesRegistrator:
#     def __init__(
#         self,
#         router: APIRouter,
#         endpoints: UserEndpoints,
#     ):
#         self._router = router
#         self._endpoints = endpoints

#     def register_routes(self):
#         self._router.add_api_route(
#             methods=["GET"],
#             endpoint=self._endpoints.list_users,
#             path="/get-users",
#             response_model=list[UserSchema],
#             summary="Get user",
#             description="Lists users, with or without offset/limit/filter params",
#         )

#         self._router.add_api_route(
#             methods=["GET"],
#             endpoint=self._endpoints.get_user,
#             path="/get-user",
#             response_model=UserSchema,
#             summary="Get one user",
#             description="Gets user by it's username",
#         )

#         self._router.add_api_route(
#             methods=["POST"],
#             endpoint=self._endpoints.create_user,
#             path="/create-user",
#             response_model=UserSchema,
#             summary="Create user",
#             description="Creates new user with provided credentials",
#         )
#         self._router.add_api_route(
#             methods=["PATCH"],
#             endpoint=self._endpoints.update_user,
#             path="/update-user",
#             response_model=None,
#             summary="Update user",
#             description="Updates user data and avatar.\
#                 Does not update is_active, is_staff, \
#                 is_superuser fields",
#         )
#         self._router.add_api_route(
#             methods=["PATCH"],
#             endpoint=self._endpoints.update_user_password,
#             path="/update-user-password",
#             response_model=None,
#             summary="Update user's password",
#             description="Hashes and updates user's password",
#         )
#         self._router.add_api_route(
#             methods=["DELETE"],
#             endpoint=self._endpoints.delete_user,
#             path="/delete/{username}",
#             response_model=None,
#             summary="Deletes user",
#             description="Deletes user and all related user's data from database",
#         )

#     def get_router(self):
#         return self._router


# user_routes_registrator = UserRoutesRegistrator(
#     endpoints=user_endpoints,
#     router=user_router,
# )
