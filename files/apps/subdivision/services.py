from files.apps.subdivision.repository import (
    EmployeeRepository,
    ProjectRepository,
    SubdivisionRepository,
    employee_repository,
    subdivision_repository,
    project_repository,
)
from files.apps.subdivision.schemas import (
    BaseSubdivisionSchema,
    EmployeeSchema,
    BaseProjectSchema,
    ProjectSchema,
    SubdivisionSchema,
)


class EmployeeService:
    def __init__(self, repository: EmployeeRepository):
        self.repository = repository

    async def create_employee(self, data: EmployeeSchema) -> bool:
        result = await self.repository.create_employee(data=data)
        return result

    async def delete_employee(self, data: EmployeeSchema) -> bool:
        result = await self.repository.delete_employee(data=data)
        return result


class SubdivisionService:
    def __init__(self, repository: SubdivisionRepository):
        self.repository = repository

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

    async def get_subdivision(self, subdivision_id: int) -> SubdivisionSchema:
        """
        get subdivision data from db
        generate link to projects
        generate links for subdivision actions
        """
        subdivision_dto = await self.repository.get_subdivision(
            subdivision_id=subdivision_id
        )

        return subdivision_dto

    async def create_subdivision(
        self, data: BaseSubdivisionSchema
    ) -> SubdivisionSchema:
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

    async def create_project(
        self, subdivision_id: int, data: BaseProjectSchema
    ) -> ProjectSchema:
        """
        Creates project and
        returns created result
        """
        project_dto = await self.repository.create_project(
            subdivision_id=subdivision_id,
            data=data,
        )

        return project_dto

    async def update_project(
        self,
        project_id: int,
        data: BaseProjectSchema,
    ) -> ProjectSchema:
        """
        Updates selected project
        and returns updated result
        """
        project_dto = await self.repository.update_project(
            project_id=project_id,
            data=data,
        )

        return project_dto

    async def delete_project(self, project_id: int) -> None:
        """
        Deletes project by id
        """
        await self.repository.delete_project(project_id=project_id)


employee_service = EmployeeService(repository=employee_repository)
subdivision_service = SubdivisionService(repository=subdivision_repository)
project_service = ProjectService(repository=project_repository)
