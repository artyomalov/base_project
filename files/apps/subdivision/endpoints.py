from fastapi import Response, status, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from config import settings
from common import generate_url

from files.apps.subdivision.services import (
    EmployeeService,
    ProjectService,
    SubdivisionService,
    employee_service,
    subdivision_service,
    project_service,
)
from files.apps.subdivision.schemas import (
    BaseSubdivisionSchema,
    BaseProjectSchema,
    SubdivisionSchema,
)

from files.apps.subdivision.enums import DepartmentEnum


class EmployeeEndpoints:
    def __init__(self, services: EmployeeService):
        self.services = services

    async def list_employees(
        self,
        subdivision_id: int,
    ):
        employees_dto = await self.services.list_employees(
            subdivision_id=subdivision_id
        )
        return JSONResponse(
            content=jsonable_encoder(employees_dto), status_code=status.HTTP_200_OK
        )

    async def create_employee(self, subdivision: int, user: str):
        await self.services.create_employee(
            subdivision=subdivision,
            user=user,
        )
        return Response(status_code=status.HTTP_201_CREATED)

    async def delete_employee(
        self,
        subdivision: int,
        user: str,
    ):
        await self.services.delete_employee(
            subdivision=subdivision,
            user=user,
        )
        return Response(status_code=status.HTTP_204_NO_CONTENT)


class SubdivisionEndpoints:
    def __init__(
        self,
        services: SubdivisionService,
        base_url: str,
    ):
        self.services = services
        self.base_url = base_url

    def _generate_urls(self, subdivision_id: int):
        subdivision_url = generate_url(
            base_url=self.base_url,
            urls=["subdivisions", subdivision_id],
        )
        projects_url = generate_url(
            base_url=self.base_url,
            urls=["subdivisions", subdivision_id, "projects"],
        )

        employees_url = generate_url(
            base_url=self.base_url,
            urls=["subdivisions", subdivision_id, "employees"],
        )

        return {
            "subdivision_url": subdivision_url,
            "projects_url": projects_url,
            "employees_url": employees_url,
        }

    @staticmethod
    async def list_departments():
        """
        Returns list of available departments
        """
        return JSONResponse(
            jsonable_encoder(DepartmentEnum.to_dict()),
            status_code=status.HTTP_200_OK,
        )

    async def list_subdivisions(
        self,
        names: str | None = Query(
            default=None,
            description='string of names splitted by "|"',
            example="name|name",
        ),
        departments: DepartmentEnum | None = Query(
            default=None,
            description=f'string of available departments splitted by "|". Get departments {settings.BASE_URL}/subdivisions/departments',
            example="Public Safety|Transportation",
        ),
        limit: int | None = Query(default=20),
        offset: int | None = Query(default=0),
    ):
        """
        Get list of subdivisions and generates
        links to projects and employees
        """

        if names:
            names = names.split("|")
        if departments:
            departments = departments.split("|")

        subdivisions_list_dto = await self.services.list_subdivisions(
            names=names,
            departments=departments,
            offset=offset,
            limit=limit,
        )

        subdivisions_list_response = []

        for subdivision in subdivisions_list_dto:
            urls = self._generate_urls(subdivision_id=subdivision.subdivision_id)
            subdivisions_list_response.append(
                {
                    **subdivision.model_dump(),
                    "urls": urls,
                }
            )

        return JSONResponse(
            content=jsonable_encoder(subdivisions_list_response),
            status_code=status.HTTP_200_OK,
        )

    async def get_subdivision(
        self,
        subdivision_id: int,
    ):
        """
        Get concrete subdivision and generates
        links to projects and employees
        """
        subdivision_dto = await self.services.get_subdivision(
            subdivision_id=subdivision_id
        )

        urls = self._generate_urls(subdivision_id=subdivision_dto.subdivision_id)

        return JSONResponse(
            content=jsonable_encoder({**subdivision_dto.model_dump(), "urls": urls}),
            status_code=status.HTTP_200_OK,
        )

    async def create_subdivision(self, data: BaseSubdivisionSchema):
        """
        Creates subdivision and generates
        subdivision's link
        """
        subdivision_dto = await self.services.create_subdivision(data=data)
        urls = self._generate_urls(subdivision_id=subdivision_dto.subdivision_id)

        return JSONResponse(
            content=jsonable_encoder({**subdivision_dto.model_dump(), "urls": urls}),
            status_code=status.HTTP_201_CREATED,
        )

    async def update_subdivision(
        self, subdivision_id: int, data: BaseSubdivisionSchema
    ):
        """
        Update subdivision
        """
        update_subdivision_dto = SubdivisionSchema(
            subdivision_id=subdivision_id,
            **data.model_dump(),
        )
        subdivision_dto = await self.services.update_subdivision(
            data=update_subdivision_dto
        )

        return JSONResponse(
            content=jsonable_encoder(subdivision_dto),
            status_code=status.HTTP_200_OK,
        )

    async def delete_subdivision(self, subdivision_id: int):
        """
        Update subdivision
        """
        await self.services.delete_subdivision(subdivision_id=subdivision_id)

        return Response(status_code=status.HTTP_204_NO_CONTENT)


class ProjectEndpoints:
    def __init__(
        self,
        services: ProjectService,
        base_url: str,
    ):
        self.services = services
        self.base_url = base_url

    def _generate_urls(self, subdivision_id: int, project_id: int):
        project_url = generate_url(
            base_url=self.base_url,
            urls=["subdivisions", subdivision_id, "projects", project_id],
        )
        subdivision_url = generate_url(
            base_url=self.base_url,
            urls=["subdivisions", subdivision_id],
        )
        return {
            "subdivision_url": subdivision_url,
            "project_url": project_url,
        }

    async def list_projects(
        self,
        subdivision_id: int,
        names: str | None = Query(
            default=None,
            description='string of names splitted by "|"',
            example="name|name",
        ),
        completed: bool | None = Query(default=None),
        limit: int | None = Query(default=20),
        offset: int | None = Query(default=0),
    ):
        """
        Get list of project and
        generates links to projects
        """

        if names:
            names = names.split("|")

        projects_list_dto = await self.services.list_projects(
            subdivision_id=subdivision_id,
            names=names,
            completed=completed,
            limit=limit,
            offset=offset,
        )
        projects_list_response = []
        for project in projects_list_dto:
            urls = self._generate_urls(
                subdivision_id=subdivision_id,
                project_id=project.project_id,
            )
            projects_list_response.append({**project.model_dump(), "urls": urls})
        return JSONResponse(
            content=jsonable_encoder(projects_list_response),
            status_code=status.HTTP_200_OK,
        )

    async def get_project(
        self,
        subdivision_id: int,
        project_id: int,
    ):
        """
        Get concrete project
        and generates links
        """
        project_dto = await self.services.get_project(project_id=project_id)
        urls = self._generate_urls(
            subdivision_id=subdivision_id,
            project_id=project_dto.project_id,
        )
        return JSONResponse(
            content=jsonable_encoder({**project_dto.model_dump(), "urls": urls}),
            status_code=status.HTTP_200_OK,
        )

    async def create_project(
        self,
        data: BaseProjectSchema,
        subdivision_id: int,
    ):
        """
        Creates project and generates
        project's link
        """
        proejct_dto = await self.services.create_project(
            subdivision_id=subdivision_id,
            data=data,
        )

        urls = self._generate_urls(
            subdivision_id=subdivision_id,
            project_id=proejct_dto.project_id,
        )
        return JSONResponse(
            content=jsonable_encoder({**proejct_dto.model_dump(), "urls": urls}),
            status_code=status.HTTP_201_CREATED,
        )

    async def update_project(
        self,
        subdivision_id: int,
        project_id: int,
        data: BaseProjectSchema,
    ):
        """
        Update project
        """
        project_dto = await self.services.update_project(
            project_id=project_id,
            data=data,
        )
        return JSONResponse(
            content=jsonable_encoder(project_dto),
            status_code=status.HTTP_200_OK,
        )

    async def delete_project(
        self,
        subdivision_id: int,
        project_id: int,
    ):
        """
        Update project
        """
        await self.services.delete_project(project_id=project_id)
        return Response(status_code=status.HTTP_205_RESET_CONTENT)


employee_endpoints = EmployeeEndpoints(services=employee_service)
subdivision_endpoints = SubdivisionEndpoints(
    services=subdivision_service,
    base_url=settings.BASE_URL,
)
project_endpoints = ProjectEndpoints(
    services=project_service,
    base_url=settings.BASE_URL,
)
