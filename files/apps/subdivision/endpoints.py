from fastapi import Response, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from config import settings

from common import Paginator, generate_url

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
    EmployeeSchema,
    BaseProjectSchema,
    SubdivisionSchema,
)

from files.apps.subdivision.enums import DepartmentEnum


class EmployeeEndpoints:
    def __init__(self, services: EmployeeService):
        self.services = services

    async def create_employee(self, data: EmployeeSchema):
        await self.services.create_employee(data=data)
        return JSONResponse(
            content=jsonable_encoder(data),
            status_code=status.HTTP_201_CREATED,
        )

    async def list_employees(self, project_id: int):
        pass

    async def delete_employee(self, data: EmployeeSchema):
        await self.services.delete_employee(data=data)
        return Response(status_code=status.HTTP_204_NO_CONTENT)


class SubdivisionEndpoints:
    def __init__(
        self,
        services: SubdivisionService,
        base_url: str,
        PaginatorClass: Paginator | None = None,
    ):
        self.PaginatorClass = PaginatorClass
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
        filter: str = "",
        offset: int = 0,
        limit: int = 20,
    ):
        """
        Get list of subdivisions and generates
        links to projects and employees
        """
        subdivisions_list_dto = await self.services.list_subdivisions(
            filter=filter,
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
        PaginatorClass: Paginator | None = None,
    ):
        self.PaginatorClass = PaginatorClass
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
        filter: str = "",
        offset: int = 0,
        limit: int = 20,
    ):
        """
        Get list of project and
        generates links to projects
        """
        projects_list_dto = await self.services.list_projects(
            subdivision_id=subdivision_id,
            filter=filter,
            offset=offset,
            limit=limit,
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
