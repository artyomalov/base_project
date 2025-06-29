from sqlalchemy import select, insert, update, delete, and_
from sqlalchemy.orm import load_only, defer, joinedload, selectinload
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from config import async_session

from files.exceptions.does_not_exist_exception import DoesNotExistError

from files.apps.subdivision.models import Subdivision, Project, Employee
from files.apps.subdivision.schemas import (
    BaseProjectSchema,
    BaseSubdivisionSchema,
    EmployeeSchema,
    SubdivisionSchema,
    ProjectSchema,
)


class EmployeeRepository:
    def __init__(self, async_session: async_sessionmaker[AsyncSession]):
        self.async_session = async_session

    async def list_employees(self, project_id: int):
        async with self.async_session() as session:
            stmt = select(Employee).options(
                joinedload(Employee.employee).load_only(
                    "username",
                    "email",
                    "name",
                    "phone_number",
                    "avatar",
                    "about",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                )
            )
            stmt_result = await session.execute(statement=stmt)
            employees = stmt_result.scalars.all()

            print(employees, ">>>>>>>>>>>>>>>>>>>>>>>>>")

    async def create_employee(self, data: EmployeeSchema) -> None:
        async with self.async_session() as session:
            try:
                stmt = insert(Employee).values(
                    user=data.user,
                    subdivision=data.subdivision,
                )
                await session.execute(statement=stmt)
                await session.commit()
            except:
                pass

    async def delete_employee(self, data: EmployeeSchema) -> None:
        async with self.async_session() as session:
            try:
                stmt = delete(Employee).where(
                    and_(
                        Employee.user == data.user,
                        Employee.subdivision == data.subdivision,
                    )
                )
                await session.execute(stmt)
                await session.commit()
            except:
                pass


class SubdivisionRepository:
    def __init__(self, async_session: async_sessionmaker[AsyncSession]):
        self.async_session = async_session

    async def list_subdivisions(
        self,
        filter: list[str],
        offset: int,
        limit: int,
    ) -> list[SubdivisionSchema]:
        async with self.async_session() as session:
            query = (
                select(Subdivision)
                .options(
                    load_only(
                        Subdivision.subdivision_id,
                        Subdivision.name,
                        Subdivision.description,
                        Subdivision.creation_time,
                        Subdivision.department,
                        raiseload=True,
                    ).selectinload(Subdivision.employees)
                )
                .where()
                .offset(offset)
                .limit(limit)
            )
            query_result = await session.execute(query)
            subdivisions = query_result.scalars().all()

            subdivisions_list_dto = []

            for subdivision in subdivisions:
                subdivision_dto = SubdivisionSchema(
                    subdivision_id=subdivision.subdivision_id,
                    name=subdivision.name,
                    description=subdivision.description,
                    creation_time=subdivision.creation_time,
                    department=subdivision.department,
                    employees=subdivision.employees,
                )

                subdivisions_list_dto.append(subdivision_dto)

            return subdivisions_list_dto

    async def get_subdivision(self, subdivision_id: int) -> SubdivisionSchema:
        async with self.async_session() as session:
            query = (
                select(Subdivision)
                .options(
                    load_only(
                        Subdivision.name,
                        Subdivision.description,
                        Subdivision.creation_time,
                        Subdivision.department,
                        Subdivision.employees,
                    ).selectinload(Subdivision.employees)
                )
                .where(Subdivision.subdivision_id == subdivision_id)
            )

            query_result = await session.execute(statement=query)
            subdivision: Subdivision = query_result.scalar_one()

            subdivision_dto = SubdivisionSchema(
                subdivision_id=subdivision_id,
                name=subdivision.name,
                description=subdivision.description,
                creation_time=subdivision.creation_time,
                department=subdivision.department,
                employees=subdivision.employees,
            )

            return subdivision_dto

    async def create_subdivision(
        self, data: BaseSubdivisionSchema
    ) -> SubdivisionSchema:
        async with self.async_session() as session:
            stmt = (
                insert(Subdivision)
                .values(**data.model_dump())
                .returning(
                    Subdivision.subdivision_id,
                    Subdivision.name,
                    Subdivision.description,
                    Subdivision.creation_time,
                    Subdivision.department,
                )
            )

            stmt_result = await session.execute(statement=stmt)

            subdivision: Subdivision = stmt_result.one()

            subdivision_dto = SubdivisionSchema(
                subdivision_id=subdivision.subdivision_id,
                name=subdivision.name,
                description=subdivision.description,
                creation_time=subdivision.creation_time,
                department=subdivision.department,
            )

            await session.commit()

            return subdivision_dto

    async def update_subdivision(self, data: SubdivisionSchema) -> SubdivisionSchema:
        async with self.async_session() as session:
            update_dict = {}

            if data.name is not None:
                update_dict["name"] = data.name
            if data.description is not None:
                update_dict["description"] = data.description
            if data.department is not None:
                update_dict["department"] = data.department

            stmt = (
                update(Subdivision)
                .values(**update_dict)
                .where(Subdivision.subdivision_id == data.subdivision_id)
                .returning(Subdivision)
                .options(
                    load_only(
                        Subdivision.subdivision_id,
                        Subdivision.name,
                        Subdivision.description,
                        Subdivision.creation_time,
                        Subdivision.department,
                    )
                )
            )

            stmt_result = await session.execute(statement=stmt)
            subdivision: Subdivision = stmt_result.scalar_one()

            subdivision_dto = SubdivisionSchema(
                subdivision_id=subdivision.subdivision_id,
                name=subdivision.name,
                description=subdivision.description,
                creation_time=subdivision.creation_time,
                department=subdivision.department,
            )

            await session.commit()

            return subdivision_dto

    async def delete_subdivision(self, subdivision_id: int) -> None:
        async with self.async_session() as session:
            stmt = (
                delete(Subdivision)
                .where(Subdivision.subdivision_id == subdivision_id)
                .returning(
                    Subdivision.subdivision_id,
                    Subdivision.name,
                    Subdivision.description,
                    Subdivision.creation_time,
                    Subdivision.department,
                )
            )
            stmt_result = await session.execute(statement=stmt)
            subdivision: Subdivision = stmt_result.one()

            subdivision_dto = SubdivisionSchema(
                subdivision_id=subdivision.subdivision_id,
                name=subdivision.name,
                description=subdivision.description,
                creation_time=subdivision.creation_time,
                department=subdivision.department,
            )

            await session.commit()

            return subdivision_dto


class ProjectRepository:
    def __init__(self, async_session: async_sessionmaker[AsyncSession]):
        self.async_session = async_session

    async def list_projects(
        self,
        subdivision_id: int | None = None,
        filter: dict = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[ProjectSchema]:
        async with self.async_session() as session:
            query = (
                select(Project)
                .options(
                    load_only(
                        Project.project_id,
                        Project.name,
                        Project.completed,
                        Project.start_time,
                        Project.complete_time,
                        Project.description,
                        Project.subdivision_id,
                        raiseload=True,
                    )
                )
                .where(subdivision_id == subdivision_id)
                .limit(limit)
                .offset(offset)
            )

            query_result = await session.execute(query)
            projects = query_result.scalars().all()

            projects_dto = [
                ProjectSchema(
                    project_id=project.project_id,
                    name=project.name,
                    completed=project.completed,
                    start_time=project.start_time,
                    complete_time=project.complete_time,
                    description=project.description,
                    subdivision_id=project.subdivision_id,
                )
                for project in projects
            ]

            return projects_dto

    async def get_project(self, project_id) -> ProjectSchema:
        try:
            async with self.async_session() as session:
                query = (
                    select(Project)
                    .options(
                        load_only(
                            Project.project_id,
                            Project.name,
                            Project.completed,
                            Project.start_time,
                            Project.complete_time,
                            Project.description,
                            Project.subdivision_id,
                            raiseload=True,
                        )
                    )
                    .where(Project.project_id == project_id)
                )

                query_result = await session.execute(query)
                project = query_result.scalar_one()

                project_dto = ProjectSchema(
                    project_id=project.project_id,
                    name=project.name,
                    completed=project.completed,
                    start_time=project.start_time,
                    complete_time=project.complete_time,
                    description=project.description,
                    subdivision_id=project.subdivision_id,
                )

                return project_dto
        except NoResultFound as error:
            DoesNotExistError(
                message="Required user doesn't exits",
                class_name=self.__class__.__name__,
                method_name=self.get_project.__name__,
                error_text=str(error),
            )
        except MultipleResultsFound as error:
            pass

    async def create_project(self, subdivision_id: int, data: BaseProjectSchema):
        async with self.async_session() as session:
            print(data, ">>>>>>>>>>>>>>>>>>>>>>>>>")
            stmt = (
                insert(Project)
                .values(
                    **data.model_dump(exclude_none=True),
                    subdivision_id=subdivision_id,
                )
                .returning(
                    Project.project_id,
                    Project.name,
                    Project.completed,
                    Project.start_time,
                    Project.complete_time,
                    Project.description,
                    Project.subdivision_id,
                )
            )

            stmt_result = await session.execute(stmt)
            project: Project = stmt_result.one()

            project_dto = ProjectSchema(
                project_id=project.project_id,
                name=project.name,
                completed=project.completed,
                start_time=project.start_time,
                complete_time=project.complete_time,
                description=project.description,
                subdivision_id=project.subdivision_id,
            )
            await session.commit()

            return project_dto

    async def update_project(self, project_id: int, data: BaseProjectSchema):
        async with self.async_session() as session:

            stmt = (
                update(Project)
                .values(**data.model_dump())
                .where(Project.project_id == project_id)
                .returning(
                    Project.project_id,
                    Project.name,
                    Project.completed,
                    Project.start_time,
                    Project.complete_time,
                    Project.description,
                    Project.subdivision_id,
                )
            )

            stmt_result = await session.execute(statement=stmt)
            project = stmt_result.one()

            project_dto = ProjectSchema(
                project_id=project.project_id,
                name=project.name,
                completed=project.completed,
                start_time=project.start_time,
                complete_time=project.complete_time,
                description=project.description,
                subdivision_id=project.subdivision_id,
            )
            await session.commit()

            return project_dto

    async def delete_project(self, project_id: int) -> None:
        async with self.async_session() as session:
            stmt = delete(Project).where(Project.project_id == project_id)
            await session.execute(stmt)
            await session.commit()


employee_repository = EmployeeRepository(async_session=async_session)
subdivision_repository = SubdivisionRepository(async_session=async_session)
project_repository = ProjectRepository(async_session=async_session)
