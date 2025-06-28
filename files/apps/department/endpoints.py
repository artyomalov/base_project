from fastapi import Response, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from common import Paginator, generate_url

from files.apps.department.services import (
    EmployeeService,
    ProjectService,
    SubdivisionService,
)
from files.apps.department.schemas import (
    EmployeeSchema,
    ProjectSchema,
    SubdivisionSchema,
)


class EmployeeEndpoints:
    def __init__(self, service: EmployeeService):
        self.service = service

    async def create_employee(self, data: EmployeeSchema):
        result = await self.service.create_employee(data=data)

        if not result:
            return JSONResponse(
                jsonable_encoder({"error": "Operation failed"}),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return JSONResponse(
            content=jsonable_encoder(data),
            status_code=status.HTTP_201_CREATED,
        )

    async def delete_employee(self, data: EmployeeSchema):
        result = await self.service.delete_employee(data=data)

        if not result:
            return JSONResponse(
                jsonable_encoder({"error": "Operation failed"}),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(status_code=status.HTTP_204_NO_CONTENT)


class SubdivisionEndpoints:
    def __init__(
        self,
        services: SubdivisionService,
        PaginatorClass: Paginator,
        base_url: str,
    ):
        self.PaginatorClass = PaginatorClass

        self.services = services

        self.base_url = base_url

    def _generate_urls(self, subdivision_id: int):
        subdivision_url_get = generate_url(
            base_url=self.base_url,
            urls=["subdivisions", "get", subdivision_id],
        )
        subdivision_url_patch = generate_url(
            base_url=self.base_url,
            urls=["subdivisions", "patch", subdivision_id],
        )
        subdivision_url_delete = generate_url(
            base_url=self.base_url,
            urls=["subdivisions", "delete", subdivision_id],
        )
        projects_url_get = generate_url(
            base_url=self.base_url,
            urls=["subdivisions", subdivision_id, "projects"],
        )
        projects_url_post = generate_url(
            base_url=self.base_url,
            urls=["subdivisions", subdivision_id, "projects"],
        )

        employees_url_get = generate_url(
            base_url=self.base_url,
            urls=["subdivisions", subdivision_id, "employees"],
        )
        employees_url_post = generate_url(
            base_url=self.base_url,
            urls=["subdivisions", subdivision_id, "employees"],
        )
        employees_url_delete = generate_url(
            base_url=self.base_url,
            urls=["subdivisions", subdivision_id, "employees"],
        )

        return {
            "subdivision_url_get": subdivision_url_get,
            "subdivision_url_patch": subdivision_url_patch,
            "subdivision_url_delete": subdivision_url_delete,
            "projects_url_get": projects_url_get,
            "projects_url_post": projects_url_post,
            "employees_url_get": employees_url_get,
            "employees_url_post": employees_url_post,
            "employees_url_delete": employees_url_delete,
        }

    async def list_subdivisions(
        self,
        filter: str,
        offset: int,
        limit: int,
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

    async def create_subdivision(self, data: SubdivisionSchema):
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

    async def update_subdivision(self, data: SubdivisionSchema):
        """
        Update subdivision
        """
        subdivision_dto = await self.services.get_subdivision(data=data)

        return JSONResponse(
            content=jsonable_encoder(
                subdivision_dto,
                status_code=status.HTTP_200_OK,
            )
        )

    async def delete_subdivision(self, subdivision_id: int):
        """
        Update subdivision
        """
        subdivision_dto = await self.services.delete_subdivision(
            subdivision_id=subdivision_id
        )

        return Response(
            content=jsonable_encoder(
                subdivision_dto,
                status_code=status.HTTP_200_OK,
            )
        )


class ProjectEndpoints:
    def __init__(
        self,
        services: ProjectService,
        PaginatorClass: Paginator,
        base_url: str,
    ):
        self.PaginatorClass = PaginatorClass
        self.services = services
        self.base_url = base_url

    def _generate_urls(self, project_id: int):
        project_url_get = generate_url(
            base_url=self.base_url,
            urls=["subdivisions", "projects", "get", project_id],
        )
        project_url_patch = generate_url(
            base_url=self.base_url,
            urls=["subdivisions", "projects", "patch", project_id],
        )
        project_url_delete = generate_url(
            base_url=self.base_url,
            urls=["subdivisions", "projects", "delete", project_id],
        )
        return {
            "project_url_get": project_url_get,
            "project_url_patch": project_url_patch,
            "project_url_delete": project_url_delete,
        }

    async def list_projects(
        self,
        subdivision_id: int,
        filter: str,
        offset: int,
        limit: int,
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
            urls = self._generate_urls(project_id=project.project_id)
            projects_list_response.append({**project.model_dump(), "urls": urls})
        return JSONResponse(
            content=jsonable_encoder(projects_list_response),
            status_code=status.HTTP_200_OK,
        )

    async def get_project(
        self,
        project_id: int,
    ):
        """
        Get concrete project
        and generates links
        """
        project_dto = await self.services.get_project(project_id=project_id)
        urls = self._generate_urls(project_id=project_dto.project_id)
        return JSONResponse(
            content=jsonable_encoder({**project_dto.model_dump(), "urls": urls}),
            status_code=status.HTTP_200_OK,
        )

    async def create_project(self, data: ProjectSchema):
        """
        Creates project and generates
        project's link
        """
        proejct_dto = await self.services.create_project(data=data)
        urls = self._generate_urls(project_id=proejct_dto.project_id)
        return JSONResponse(
            content=jsonable_encoder({**proejct_dto.model_dump(), "urls": urls}),
            status_code=status.HTTP_201_CREATED,
        )

    async def update_project(self, data: ProjectSchema):
        """
        Update project
        """
        project_dto = await self.services.update_project(data=data)
        return JSONResponse(
            content=jsonable_encoder(project_dto, status_code=status.HTTP_200_OK)
        )

    async def delete_project(self, project_data: int):
        """
        Update project
        """
        project_dto = await self.services.delete_project(project_data=project_data)
        return JSONResponse(
            content=jsonable_encoder(project_dto, status_code=status.HTTP_200_OK)
        )
