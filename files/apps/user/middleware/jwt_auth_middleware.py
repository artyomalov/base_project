from logging import getLogger

from fastapi import Request, status
from fastapi.responses import JSONResponse
from jwt import InvalidSignatureError, ExpiredSignatureError, DecodeError
from sqlalchemy.exc import IntegrityError, NoResultFound

from config import settings

from files.apps.user.services import verify_user_services
from files.exceptions import (
    JWTTokenHasNotBeenProvidedError,
    ValidationError,
    UnprocessableEntityError,
    IsNotActiveError,
    InvalidPasswordError,
)

logger = getLogger("common.base_logger")


async def verify_jwt_access_token(request: Request, call_next):
    try:
        path = request.scope.get("path")
        if (
            path and path in settings.auth_jwt.ALLOW_ANY_ROUTES
        ) or request.method == "OPTIONS":
            response = await call_next(request)

            return response

        user_username_is_main_is_active_dto = await verify_user_services.verify_user_access_token_and_get_username_is_active_is_admin(
            request
        )
        request.state.username = user_username_is_main_is_active_dto.username
        request.state.is_active = user_username_is_main_is_active_dto.is_active
        request.state.is_admin = user_username_is_main_is_active_dto.is_admin
        # request.state.username = "root"
        # request.state.is_active = True
        # request.state.is_admin = True

        response = await call_next(request)

        return response
    except JWTTokenHasNotBeenProvidedError as error:
        # print(1)
        logger.error(str(error))

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "error": "'Authorization' header has not been provided or not valid"
            },
        )
    except ValidationError as error:
        # print(2)
        str_error = str(error)
        logger.error(str_error)

        return JSONResponse(
            content={"error": str_error},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except InvalidSignatureError as error:
        # print(3)
        logger.error(str(error))

        return JSONResponse(
            content={"error": "Token is not valid. Token verification failed."},
            status_code=status.HTTP_403_FORBIDDEN,
        )

    except DecodeError:
        # print(4)
        return JSONResponse(
            content={"error": "jwt token is not valid"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except ExpiredSignatureError as error:
        # print(5)
        logger.error(str(error))

        return JSONResponse(
            content={"error": "Token has been expired."},
            status_code=status.HTTP_403_FORBIDDEN,
        )

    except IsNotActiveError as error:
        # print(6)
        return JSONResponse(
            content={"error": "User is not active"},
            status_code=status.HTTP_403_FORBIDDEN,
        )
    # Handling db errors
    except NoResultFound as error:
        # If required data does ton exist(override to custom exception to avoid layers bounding
        # print(7)
        logger.error(str(error))
        return JSONResponse(
            content={"error": "Data does not exist"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    except IntegrityError as error:
        # print(8)
        logger.error(str(error))
        if "UniqueViolationError" in str(error.orig):
            return JSONResponse(
                content={"error": "Inserted data must be unique"},
                status_code=status.HTTP_409_CONFLICT,
            )
        if "ForeignKeyViolationError" in str(error.orig):
            return JSONResponse(
                content={
                    "error": "Row with foreign key you trying to insert does not exist"
                },
                status_code=status.HTTP_409_CONFLICT,
            )

        return JSONResponse(
            content={"error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except InvalidPasswordError as error:
        # print(10)
        str_error = str(error)
        logger.error(str_error)
        return JSONResponse(
            content={"error": str_error}, status_code=status.HTTP_401_UNAUTHORIZED
        )

    except UnprocessableEntityError as error:
        # print(11)
        str_error = str(error)
        logger.error(str_error)
        return JSONResponse(
            content={"error": "Incoming data is not valid"},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
