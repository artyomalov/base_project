from logging import getLogger

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request

from files import api_v1_router
from files.exceptions import JWTTokenHasNotBeenProvidedError

from files.apps.user import (
    verify_jwt_access_token,
    check_user_is_authorized_to_use_route,
)


logger = getLogger("common.base_logger")


def create_app():
    """
    App initialization.
    Register middleware, includes routers
    """
    app = FastAPI(title="Itrum_task")

    logger.info("REGISTER MIDDLEWARE")

    @app.middleware("http")
    async def user_is_authorized_to_use_route_middleware(
        request: Request,
        call_next,
    ):
        return await check_user_is_authorized_to_use_route(
            request=request,
            call_next=call_next,
        )

    # why second middleware is executed first
    @app.middleware("http")
    async def jwt_middleware(
        request: Request,
        call_next,
    ):
        return await verify_jwt_access_token(
            request=request,
            call_next=call_next,
        )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    logger.info("REGISTER ROUTES")
    app.include_router(api_v1_router)

    logger.info("REGISTER EXCEPTION HANDLER")

    @app.exception_handler(JWTTokenHasNotBeenProvidedError)
    async def register_jwt_token_has_not_been_provided_error(
        request: Request,
        error: JWTTokenHasNotBeenProvidedError,
    ):
        logger.error(str(error))

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "error": "'Authorization' header has not been provided or not valid"
            },
        )

    return app
