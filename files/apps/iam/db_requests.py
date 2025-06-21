from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import load_only, defer
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from config import async_session

from files.apps.iam.models import User
from files.apps.iam.schemas import UserSchema
from files.exceptions import DoesNotExistError


class UserDbRequests:
    def __init__(self, async_session: async_sessionmaker[AsyncSession]):
        self.async_session = async_session

    async def get_user(self, user_id: int) -> UserSchema:
        async with self.async_session() as session:
            try:
                query = (
                    select(User)
                    .options(
                        load_only(
                            User.user_id,
                            User.email,
                            User.name,
                            User.phone_number,
                            User.avatar,
                            User.about,
                            User.is_staff,
                            User.is_active,
                            User.is_superuser,
                            raiseload=True,
                        )
                    )
                    .where(user_id == user_id)
                )
                query_result = await session.execute(statement=query)
                user: User = query_result.scalar_one()

                user_dto = UserSchema(
                    user_id=user.user_id,
                    email=user.email,
                    name=user.name,
                    phone_number=user.phone_number,
                    avatar=user.avatar,
                    about=user.about,
                    is_staff=user.is_staff,
                    is_active=user.is_active,
                    is_superuser=user.is_superuser,
                )

                return user_dto

            except NoResultFound as error:
                DoesNotExistError("Required user doesn't exits")
            except MultipleResultsFound as error:
                pass

    async def get_users(self, filter: str, limit: int, offset: int):
        async with self.async_session() as session:
            query = (
                select(User)
                .options(
                    load_only(
                        User.user_id,
                        User.email,
                        User.name,
                        User.is_staff,
                        User.is_active,
                        User.is_superuser,
                        raiseload=True,
                    )
                )
                # !!!!!!!!!!!!!!!!!!!!!!!!
                .where()
                # !!!!!!!!!!!!!!!!!!!!!!!!
                .limit(limit=limit)
                .offset(offset=offset)
            )
            query_rows = await session.execute(statement=query)
            query_rows_result = query_rows.scalars().all()

            users_dto = [
                UserSchema(
                    user.user_id,
                    user.email,
                    user.name,
                    user.is_staff,
                    user.is_active,
                    user.is_superuser,
                )
                for user in query_rows_result
            ]

            return users_dto

    async def create_user(self, data: UserSchema):
        async with self.async_session() as session:
            try:
                stmt = (
                    insert(User)
                    .values(
                        data.model_dump(
                            exclude_none=True,
                            exclude_unset=True,
                        )
                    )
                    .returning(
                        User.user_id,
                        User.email,
                        User.name,
                        User.phone_number,
                        User.avatar,
                        User.about,
                        User.is_staff,
                        User.is_active,
                        User.is_superuser,
                    )
                )

                stmt_result = await session.execute(statement=stmt)
                user: User = stmt_result.scalar_one()

                user_dto = UserSchema(
                    user_id=user.user_id,
                    email=user.email,
                    name=user.name,
                    phone_number=user.phone_number,
                    avatar=user.avatar,
                    about=user.about,
                    is_staff=user.is_staff,
                    is_active=user.is_active,
                    is_superuser=user.is_superuser,
                )

                return user_dto
            except:
                pass

    async def delete_user(self, user_id: int) -> None:
        async with self.async_session() as session:
            stmt = delete(User).where(user_id == user_id)
            await session.execute(stmt)


user_db_requests = UserDbRequests(async_session=async_session)
