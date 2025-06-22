from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import load_only, defer
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from config import async_session

from files.apps.user.models import User
from files.apps.user.schemas import UserSchema
from files.exceptions import DoesNotExistError, ValidationError


class UserDbRequests:
    def __init__(self, async_session: async_sessionmaker[AsyncSession]):
        self.async_session = async_session

    async def get_user(
        self, user_id: int = None, email: str = None, load_password: bool = False
    ) -> UserSchema:
        async with self.async_session() as session:

            if user_id is not None and email is not None:
                raise

            load_list = [
                User.user_id,
                User.email,
                User.name,
                User.phone_number,
                User.avatar,
                User.about,
                User.is_staff,
                User.is_active,
                User.is_superuser,
            ]
            if load_password:
                load_list.append(User.password)
            try:
                query = select(User).options(
                    load_only(
                        *load_list,
                        raiseload=True,
                    )
                )
                if user_id is not None:
                    query = query.where(user_id == user_id)
                if email is not None:
                    query = query.where(email == email)

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

                if load_password:
                    user_dto.password = user.password

                return user_dto

            except NoResultFound as error:
                DoesNotExistError(
                    message="Required user doesn't exits",
                    class_name=self.__class__.__name__,
                    method_name=self.get_user.__name__,
                    error_text=str(error),
                )
            except MultipleResultsFound as error:
                pass

    async def get_users(
        self,
        filter: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ):
        async with self.async_session() as session:
            query = select(
                User.user_id,
                User.email,
                User.name,
                User.is_staff,
                User.is_active,
                User.is_superuser,
            )
            if filter:
                # !!!!!!!!!!!!!!!!!!!!!!!!
                query = query.where(filter)
            if limit:
                query = query.limit(limit=limit)
            if offset:
                query = query.offset(offset=offset)

            query_rows = await session.execute(statement=query)
            query_rows_result = query_rows.scalars().all()

            users_dto = [
                UserSchema(
                    user_id=user.user_id,
                    email=user.email,
                    name=user.name,
                    is_staff=user.is_staff,
                    is_active=user.is_active,
                    is_superuser=user.is_superuser,
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

    async def update_user(self, data: UserSchema) -> None:
        async with async_session() as session:
            stmt = (
                update(User)
                .where(User.user_id == data.user_id)
                .values(
                    **data.model_dump(
                        exclude_defaults=True,
                        exclude={"user_id"},
                    )
                )
            ).returning(User.user_id)
            stmt_result = await session.execute(statement=stmt)
            stmt_result.scalar_one()

            await session.commit()

    async def update_user_password(
        self,
        user_id: int,
        new_password: str,
    ) -> None:
        async with async_session() as session:
            stmt_password = (
                update(User)
                .values(password=new_password)
                .where(User.user_id == user_id)
            )

            stmt_password_result = await session.execute(stmt_password)
            stmt_password_result.scalar_one()
            await session.commit()

    async def get_user_password(self, user_id: str) -> bytes:
        async with async_session() as session:
            stmt = select(User.password).where(User.user_id == user_id)
            stmt_result = await session.execute(stmt)
            user_password = stmt_result.scalar_one()

            return user_password

    async def delete_user(self, user_id: int) -> None:
        async with self.async_session() as session:
            stmt = delete(User).where(user_id == user_id)
            await session.execute(stmt)


class UserAuthDbRequests:
    def __init__(self, async_session: async_sessionmaker[AsyncSession]):
        self.async_session = async_session

    async def get_user_id_and_status(self, email: str) -> "UserSchema":
        async with self.async_session() as session:
            try:

                query = select(
                    User.user_id,
                    User.is_active,
                    User.is_staff,
                ).where(User.email == email)
                query_result = await session.execute(statement=query)
                query_result_row: User = query_result.one_or_none()

                return UserSchema(
                    email=email,
                    user_id=query_result_row.user_id,
                    is_active=query_result_row.is_active,
                    is_admin=query_result_row.is_staff,
                )
            except NoResultFound as error:
                DoesNotExistError(
                    message="Required user doesn't exits",
                    class_name=self.__class__.__name__,
                    method_name=self.get_user_id_and_status.__name__,
                    error_text=str(error),
                )


user_auth_db_requests = UserAuthDbRequests(async_session=async_session)
user_db_requests = UserDbRequests(async_session=async_session)
