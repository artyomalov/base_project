from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import load_only, defer
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from config import async_session

from files.apps.department.models import Subdivision, Project


class SubdivisionRepository:
    def __init__(self, async_session: async_sessionmaker[AsyncSession]):
        self.async_session = async_session

    async def list_subdivisions(self):
        async with self.async_session() as session:
            pass

    async def get_subdivision(self):
        async with self.async_session() as session:
            pass

    async def create_subdivision(self):
        async with self.async_session() as session:
            pass

    async def update_subdivision(self):
        async with self.async_session() as session:
            pass

    async def delete_subdivision(self):
        async with self.async_session() as session:
            pass


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
