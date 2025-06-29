from fastapi import APIRouter

from files.apps.subdivision.endpoints import (
    employee_endpoints,
    subdivision_endpoints,
    project_endpoints,
)
from files.apps.subdivision.enums import DepartmentEnum
from files.apps.subdivision.schemas import (
    ProjectResponseSchema,
    ProjectSchema,
    SubdivisionResponseSchema,
    SubdivisionSchema,
)

subdivision_router = APIRouter(
    prefix="/subdivisions",
    tags=["subdivisions"],
)

project_router = APIRouter(
    prefix="/subdivisions/{subdivision_id}/projects",
    tags=["projects"],
)


subdivision_router.add_api_route(
    path="/departments",
    methods=["GET"],
    endpoint=subdivision_endpoints.list_departments,
    response_model=DepartmentEnum,
    summary="List departments",
    description="List available departments",
)

subdivision_router.add_api_route(
    path="",
    methods=["GET"],
    endpoint=subdivision_endpoints.list_subdivisions,
    response_model=list[SubdivisionResponseSchema],
    summary="List subdivisions",
    description="""List subdivisions\
        params:
            filter: ;
            offset: specifies how many records will be skipped;
            limit: max quantity of returned records""",
)

subdivision_router.add_api_route(
    path="/{subdivision_id}",
    methods=["GET"],
    endpoint=subdivision_endpoints.get_subdivision,
    response_model=SubdivisionResponseSchema,
    summary="Get subdivision",
    description="Get single subdivision",
)

subdivision_router.add_api_route(
    path="",
    methods=["POST"],
    endpoint=subdivision_endpoints.create_subdivision,
    response_model=SubdivisionResponseSchema,
    summary="Create subdivisions",
    description="Creates subdivisions and returns created model"
    "with links to projects and employees",
)


subdivision_router.add_api_route(
    path="/{subdivision_id}",
    methods=["PATCH"],
    endpoint=subdivision_endpoints.update_subdivision,
    response_model=SubdivisionSchema,
    summary="Update subdivision",
    description="Updates subdivision data",
)

subdivision_router.add_api_route(
    path="/{subdivision_id}",
    methods=["DELETE"],
    endpoint=subdivision_endpoints.delete_subdivision,
    response_model=None,
    summary="Delete subdivision",
    description="Deletes subdivision",
)

# project routes
project_router.add_api_route(
    path="",
    methods=["GET"],
    endpoint=project_endpoints.list_projects,
    response_model=list[ProjectResponseSchema],
    summary="List projects",
    description="""List subdivisions and returns projectdata
    and HATEOAS urls
    params:
        filter: ;
        offset: specifies how many records will be skipped;
        limit: max quantity of returned records""",
)

project_router.add_api_route(
    path="/{project_id}",
    methods=["GET"],
    endpoint=project_endpoints.get_project,
    response_model=ProjectResponseSchema,
    summary="Get project",
    description="Get subdivisions and returns projectdata",
)

project_router.add_api_route(
    path="",
    methods=["POST"],
    endpoint=project_endpoints.create_project,
    response_model=ProjectResponseSchema,
    summary="Create project",
    description="Creates project and returns created model",
)


project_router.add_api_route(
    path="/{project_id}",
    methods=["PATCH"],
    endpoint=project_endpoints.update_project,
    response_model=ProjectSchema,
    summary="Update project",
    description="Updates project",
)

project_router.add_api_route(
    path="/{project_id}",
    methods=["DELETE"],
    endpoint=project_endpoints.delete_project,
    response_model=None,
    summary="Delete project",
    description="Deletes project",
)
