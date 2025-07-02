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

employee_router = APIRouter(
    prefix="/subdivisions/{subdivision_id}/employees",
    tags=["employees"],
)

subdivision_router = APIRouter(
    prefix="/subdivisions",
    tags=["subdivisions"],
)

project_router = APIRouter(
    prefix="/subdivisions/{subdivision_id}/projects",
    tags=["projects"],
)

employee_router.add_api_route(
    path="",
    methods=["GET"],
    endpoint=employee_endpoints.list_employees,
    response_model=None,
    summary="List employees",
    description="Get employees(users) of concrete subdivision",
)
employee_router.add_api_route(
    path="/{user}",
    methods=["POST"],
    endpoint=employee_endpoints.create_employee,
    response_model=None,
    summary="Create employee",
    description="Creates many-to-many relationship between user and subdivision",
)
employee_router.add_api_route(
    path="/{user}",
    methods=["DELETE"],
    endpoint=employee_endpoints.delete_employee,
    response_model=None,
    summary="Delete employee",
    description="Removes many-to-many relationship between user and subdivision",
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
    description="List subdivisions",
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
    description="List subdivisions and returns projectdata and HATEOAS urls",
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
