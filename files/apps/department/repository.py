from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import load_only, defer
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from config import async_session

from files.apps.department.models import Subdivision, Project
from files.apps.department.schemas import SubdivisionSchema, ProjectSchema


class SubdivisionRepository:
    def __init__(self, async_session: async_sessionmaker[AsyncSession]):
        self.async_session = async_session

    async def list_subdivisions(
        self,
        filter: str,
        offset: int,
        limit: int,
    ) -> list[SubdivisionSchema]:
        async with self.async_session() as session:
            query = (
                select(
                    Subdivision.subdivision_id,
                    Subdivision.name,
                    Subdivision.description,
                    Subdivision.creation_time,
                    Subdivision.department,
                )
                .where()
                .offset(offset)
                .limit(limit)
            )
            query_result = await session.execute(statement=query)
            subdivisions = query_result.all()

            subdivisions_list_dto = [
                SubdivisionSchema(
                    subdivision.subdivision_id,
                    subdivision.name,
                    subdivision.description,
                    subdivision.creation_time,
                    subdivision.department,
                )
                for subdivision in subdivisions
            ]

            return subdivisions_list_dto

    async def get_subdivision(self, subdivision_id) -> SubdivisionSchema:
        async with self.async_session() as session:
            query = select(
                Subdivision.subdivision_id,
                Subdivision.name,
                Subdivision.description,
                Subdivision.creation_time,
                Subdivision.department,
            ).where(Subdivision.subdivision_id == subdivision_id)

            query_result = await session.execute(statement=query)
            subdivision: Subdivision = query_result.all()

            subdivision_dto = SubdivisionSchema(
                subdivision.subdivision_id,
                subdivision.name,
                subdivision.description,
                subdivision.creation_time,
                subdivision.department,
            )

            return subdivision_dto

    async def create_subdivision(self):
        async with self.async_session() as session:
            pass

    async def update_subdivision(self):
        async with self.async_session() as session:
            pass

    async def delete_subdivision(self, subdivision_id: int):
        async with self.async_session() as session:
            stmt = delete(Subdivision).where(
                Subdivision.subdivision_id == subdivision_id
            )

            await session.execute(stmt)

            await session.commit()


class SubdivisionRepository:
    def __init__(self, async_session: async_sessionmaker[AsyncSession]):
        self.async_session = async_session

    async def list_projects(self):
        async with self.async_session() as session:
            pass

    async def get_project(self):
        async with self.async_session() as session:
            pass

    async def create_project(self):
        async with self.async_session() as session:
            pass

    async def update_project(self):
        async with self.async_session() as session:
            pass

    async def delete_project(self):
        async with self.async_session() as session:
            pass


subdivision_repository = SubdivisionRepository(async_session=async_session)
