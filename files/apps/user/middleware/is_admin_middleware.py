from fastapi import Request, status
from fastapi.responses import JSONResponse

from config import settings


async def check_user_is_authorized_to_use_route(request: Request, call_next):
    path = request.scope.get("path")
    if path and path in settings.auth_jwt.ADMIN_ROUTES and not request.state.is_staff:
        return JSONResponse(
            content={"error": "User does not have admin rights"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    response = await call_next(request)

    return response
