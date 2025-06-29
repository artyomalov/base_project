from fastapi import APIRouter

from files.apps import user_router, user_auth_router, subdivision_router, project_router


api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(router=user_auth_router)
api_v1_router.include_router(router=user_router)
api_v1_router.include_router(router=subdivision_router)
api_v1_router.include_router(router=project_router)
