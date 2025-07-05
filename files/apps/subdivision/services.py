from files.apps.subdivision.enums import DepartmentEnum
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
    BaseProjectSchema,
    EmployeeSchema,
    ProjectSchema,
    SubdivisionSchema,
)

from files.apps.user import UserRepositoryAdapter, user_repository_adapter
from files.exceptions import DoesNotExistError


class EmployeeService:
    def __init__(
        self,
        repository: EmployeeRepository,
        subdivision_repository: SubdivisionRepository,
        user_repository_adapter: UserRepositoryAdapter,
    ):
        self.repository = repository
        self.subdivision_repository = subdivision_repository
        self.user_repository_adapter = user_repository_adapter

    async def list_employees(self, subdivision_id: int) -> EmployeeSchema:
        result = await self.repository.list_employees(subdivision_id=subdivision_id)
        return result

    async def create_employee(
        self,
        subdivision: int,
        user: str,
    ) -> None:

        subdivision_exists = self.subdivision_repository.check_subdivision_exist(subdivision_id=subdivision)
        user_exists = self.user_repository_adapter.check_user_exists(username=user)

        if not subdivision_exists:
            raise DoesNotExistError(
                message=f"Subdivision with id: {subdivision} does not exist",
                class_name=self.__class__.__name__,
                method_name=self.get_user.__name__,
                error_text=f"Subdivision with id: {subdivision} does not exist",
            )
        if not user_exists:
            raise DoesNotExistError(
                message=f"User with username: {user} does not exist",
                class_name=self.__class__.__name__,
                method_name=self.get_user.__name__,
                error_text=f"User with username: {user} does not exist",
            )

        await self.repository.create_employee(
            subdivision=subdivision,
            user=user,
        )

    async def delete_employee(
        self,
        subdivision: int,
        user: str,
    ) -> None:
        await self.repository.delete_employee(
            subdivision=subdivision,
            user=user,
        )


class SubdivisionService:
    def __init__(self, repository: SubdivisionRepository):
        self.repository = repository

    async def list_subdivisions(
        self,
        names: list[str] | None,
        departments: list[DepartmentEnum] | None,
        limit: int | None = 20,
        offset: int | None = 0,
    ) -> list[SubdivisionSchema]:
        """
        Get subdivisions list with pagination
        add link for every subdivision
        """
        subdivisions_dto = await self.repository.list_subdivisions(
            names=names,
            departments=departments,
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

    # async def list_employees(self, subdivision_id: int) -> UserSchema:
    #     """
    #     Lists all subdivisions's employees
    #     """

    #     employees_dto = await self.repository.list_employees(
    #         subdivision_id=subdivision_id
    #     )
    #     return employees_dto


class ProjectService:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    async def list_projects(
        self,
        subdivision_id: int,
        names: list[str] | None = None,
        completed: bool | None = None,
        limit: int | None = 20,
        offset: int | None = 0,
    ) -> list[ProjectSchema]:
        """
        Get projects list with pagination
        add link for every project
        """
        projects_dto = await self.repository.list_projects(
            subdivision_id=subdivision_id,
            names=names,
            completed=completed,
            limit=limit,
            offset=offset,
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


employee_service = EmployeeService(
    repository=employee_repository,
    subdivision_repository=subdivision_repository,
    user_repository_adapter=user_repository_adapter,
)
subdivision_service = SubdivisionService(repository=subdivision_repository)
project_service = ProjectService(repository=project_repository)
