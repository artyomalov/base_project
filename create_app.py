from logging import getLogger

from fastapi import FastAPI, status, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from files import api_v1_router
from files.exceptions import JWTTokenHasNotBeenProvidedError

# from files.apps.user import (
#     verify_jwt_access_token,
#     check_user_is_authorized_to_use_route,
# )


from fastapi import APIRouter, Depends, Request, HTTPException, status
from logging import getLogger
from jwt import InvalidSignatureError, ExpiredSignatureError, DecodeError
from sqlalchemy.exc import IntegrityError, NoResultFound

from config import settings
from files.apps import user_router, CreateUserSchema
from files.apps.user.services import verify_user_services
from files.exceptions import (
    JWTTokenHasNotBeenProvidedError,
    ValidationError,
    UnprocessableEntityError,
    IsNotActiveError,
    InvalidPasswordError,
)

logger = getLogger("common.base_logger")


class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):
    def __init__(
        self,
        *args,
        public_routes: list[str],
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.public_routes = public_routes

    async def __call__(self, request: Request):
        path = request.scope.get("path")

        if (path and path in self.public_routes) or request.method == "OPTIONS":
            return None

        return await super().__call__(request)


oauth2_scheme = CustomOAuth2PasswordBearer(
    "api/v1/auth/login",
    public_routes=settings.auth_jwt.ALLOW_ANY_ROUTES,
    scheme_name="CreateUserSchema",
)


async def verify_jwt_access_token(token: str = Depends(oauth2_scheme)):
    try:
        if not token:
            return

    except JWTTokenHasNotBeenProvidedError as error:
        logger.error(str(error))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="'Authorization' header has not been provided or not valid",
        )
    except ValidationError as error:
        str_error = str(error)
        logger.error(str_error)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str_error)
    except InvalidSignatureError as error:
        logger.error(str(error))
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token is not valid. Token verification failed.",
        )
    except DecodeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="JWT token is not valid",
        )
    except ExpiredSignatureError as error:
        logger.error(str(error))
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Token has been expired."
        )
    except IsNotActiveError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User  is not active"
        )
    except NoResultFound as error:
        logger.error(str(error))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Data does not exist"
        )
    except IntegrityError as error:
        logger.error(str(error))
        if "UniqueViolationError" in str(error.orig):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Inserted data must be unique",
            )
        if "ForeignKeyViolationError" in str(error.orig):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Row with foreign key you trying to insert does not exist",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
    except InvalidPasswordError as error:
        str_error = str(error)
        logger.error(str_error)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str_error)
    except UnprocessableEntityError as error:
        str_error = str(error)
        logger.error(str_error)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Incoming data is not valid",
        )


logger = getLogger("logger")


def create_app():
    """
    App initialization.
    Register middleware, includes routers
    """
    app = FastAPI(title="MPSearch", dependencies=[Depends(verify_jwt_access_token)])

    logger.info("REGISTER MIDDLEWARE")

    # @app.middleware("http")
    # async def user_is_authorized_to_use_route_middleware(
    #     request: Request,
    #     call_next,
    # ):
    #     return await check_user_is_authorized_to_use_route(
    #         request=request,
    #         call_next=call_next,
    #     )

    # why second middleware is executed first
    # @app.middleware("http")
    # async def jwt_middleware(
    #     request: Request,
    #     call_next,
    # ):
    #     return await verify_jwt_access_token(
    #         request=request,
    #         call_next=call_next,
    #     )

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
