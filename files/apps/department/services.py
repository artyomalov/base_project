from config import settings
from files.apps.department.repository import (
    EmployeeRepository,
    ProjectRepository,
    SubdivisionRepository,
)
from files.apps.department.schemas import (
    EmployeeSchema,
    ProjectSchema,
    SubdivisionSchema,
)


class EmployeeService:
    def __init__(self, service: EmployeeRepository):
        self.service = service

    async def create_employee(self, data: EmployeeSchema) -> bool:
        result = await self.service.create_employee(data=data)
        return result

    async def delete_employee(self, data: EmployeeSchema) -> bool:
        result = await self.service.delete_employee(data=data)
        return result


class SubdivisionService:
    def __init__(self, subdivision_repository: SubdivisionRepository):
        self.repository = subdivision_repository

    async def list_subdivisions(
        self,
        filter: str,
        offset: int,
        limit: int,
    ) -> list[SubdivisionSchema]:
        """
        Get subdivisions list with pagination
        add link for every subdivision
        """
        subdivisions_dto = await self.repository.list_subdivisions(
            filter=filter,
            offset=offset,
            limit=limit,
        )

        return subdivisions_dto

    async def get_subdivision(self, subdivision_id: int):
        """
        get subdivision data from db
        generate link to projects
        generate links for subdivision actions
        """
        subdivision_dto = await self.repository.get_subdivision(
            subdivision_id=subdivision_id
        )

        return subdivision_dto

    async def create_subdivision(self, data: SubdivisionSchema) -> SubdivisionSchema:
        """
        Creates subdivision and returns
        created subdivision
        """
        subdivision_dto = await self.repository.create_subdivision(data=data)

        return subdivision_dto

    async def update_subdivision(self, data: SubdivisionSchema) -> SubdivisionSchema:
        """
        Updates selected subdivision and
        returns updated result
        """
        subdivision_dto = await self.repository.update_subdivision(data=data)

        return subdivision_dto

    async def delete_subdivision(self, subdivision_id: int) -> None:
        """
        Deletes selected subdivision
        """
        await self.repository.delete_subdivision(subdivision_id=subdivision_id)


class ProjectService:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    async def list_projects(
        self,
        subdivision_id: int,
        filter: str,
        offset: int,
        limit: int,
    ) -> list[ProjectSchema]:
        """
        Get projects list with pagination
        add link for every project
        """
        projects_dto = await self.repository.list_projects(
            subdivision_id=subdivision_id,
            filter=filter,
            offset=offset,
            limit=limit,
        )

        return projects_dto

    async def get_project(self, project_id: int) -> ProjectSchema:
        """
        Get project data from db
        """
        project_dto = await self.repository.get_project(project_id=project_id)

        return project_dto

    async def create_project(self, data: ProjectSchema) -> ProjectSchema:
        """
        Creates project and
        returns created result
        """
        project_dto = await self.repository.create_project(data=data)

        return project_dto

    async def update_project(self, data: ProjectSchema) -> ProjectSchema:
        """
        Updates selected project
        and returns updated result
        """
        project_dto = await self.repository.update_project(data=data)

        return project_dto

    async def delete_project(self, project_id) -> None:
        """
        Deletes project by id
        """
        project_dto = await self.repository.delete_project(project_id=project_id)

        return project_dto
