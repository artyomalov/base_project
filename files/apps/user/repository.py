from sqlalchemy import select, insert, update, delete, or_
from sqlalchemy.orm import load_only, defer
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from config import async_session

from files.apps.user.models import User
from files.apps.user.schemas import UserSchema
from files.exceptions import DoesNotExistError, ValidationError


class UserRepository:
    def __init__(self, async_session: async_sessionmaker[AsyncSession]):
        self.async_session = async_session

    async def get_user(
        self, username: str = None, email: str = None, load_password: bool = False
    ) -> UserSchema:
        async with self.async_session() as session:
            load_list = [
                User.username,
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

                if username is not None or (username is not None and email is not None):
                    query = query.where(User.username == username)
                if email is not None:
                    query = query.where(User.email == email)

                query_result = await session.execute(statement=query)
                user: User = query_result.scalar_one()

                user_dto = UserSchema(
                    username=user.username,
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

    async def list_users(
        self,
        usernames: list[str] | None = None,
        names: list[str] | None = None,
        emails: list[str] | None = None,
        is_superuser: bool = None,
        is_staff: bool = None,
        is_active: bool = None,
        limit: int | None = None,
        offset: int | None = None,
    ):
        async with self.async_session() as session:
            query = select(
                User.username,
                User.email,
                User.name,
                User.is_staff,
                User.is_active,
                User.is_superuser,
            )

            conditions = []
            if usernames is not None and len(usernames) > 0:
                conditions.append(User.username.in_(usernames))
            if names is not None and len(names) > 0:
                conditions.append(User.name.in_(names))
            if emails is not None and len(emails) > 0:
                conditions.append(User.email.in_(emails))
            if is_superuser is not None:
                conditions.append(User.is_superuser == is_superuser)
            if is_staff is not None:
                conditions.append(User.is_staff == is_staff)
            if is_active is not None:
                conditions.append(User.is_active == is_active)
            if len(conditions) > 0:
                query = query.where(*conditions)

            if limit is not None:
                query = query.limit(limit=limit)
            if offset is not None:
                query = query.offset(offset=offset)

            query_rows = await session.execute(statement=query)
            query_rows_result = query_rows.all()

            users_dto = [
                UserSchema(
                    username=user.username,
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
            stmt = (
                insert(User)
                .values(
                    username=data.username,
                    password=data.password,
                    # data.model_dump(
                    #     exclude_none=True,
                    #     exclude_unset=True,
                    # )
                )
                .returning(
                    User.username,
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
            user: User = stmt_result.one()

            user_dto = UserSchema(
                username=user.username,
                email=user.email,
                name=user.name,
                phone_number=user.phone_number,
                avatar=user.avatar,
                about=user.about,
                is_staff=user.is_staff,
                is_active=user.is_active,
                is_superuser=user.is_superuser,
            )

            await session.commit()

            return user_dto

    async def update_user(self, data: UserSchema) -> None:
        async with async_session() as session:
            try:
                stmt = (
                    update(User)
                    .where(User.username == data.username)
                    .values(
                        **data.model_dump(
                            exclude_defaults=True,
                            exclude={"username"},
                        )
                    )
                    .returning(
                        User.username,
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
                user: User = stmt_result.one_or_none()

                if user is not None:
                    return None

                user_dto = UserSchema(
                    username=user.username,
                    email=user.email,
                    name=user.name,
                    phone_number=user.phone_number,
                    avatar=user.avatar,
                    about=user.about,
                    is_staff=user.is_staff,
                    is_active=user.is_active,
                    is_superuser=user.is_superuser,
                )

                await session.commit()

                return user_dto
            except NoResultFound as error:
                DoesNotExistError(
                    message="Required user doesn't exits",
                    class_name=self.__class__.__name__,
                    method_name=self.update_user.__name__,
                    error_text=str(error),
                )

    async def update_user_password(
        self,
        username: str,
        new_password: str,
    ) -> None:
        async with async_session() as session:
            try:
                stmt_password = (
                    update(User)
                    .values(password=new_password)
                    .where(User.username == username)
                )

                await session.execute(stmt_password)
                await session.commit()
            except NoResultFound as error:
                DoesNotExistError(
                    message="Required user doesn't exits",
                    class_name=self.__class__.__name__,
                    method_name=self.update_user_password.__name__,
                    error_text=str(error),
                )

    async def get_user_password(self, username: str) -> bytes:
        async with async_session() as session:
            try:
                stmt = select(User.password).where(User.username == username)
                stmt_result = await session.execute(stmt)
                user_password = stmt_result.scalar_one()

                return user_password
            except NoResultFound as error:
                DoesNotExistError(
                    message="Required user doesn't exits",
                    class_name=self.__class__.__name__,
                    method_name=self.get_user_password.__name__,
                    error_text=str(error),
                )

    async def delete_user(self, username: str) -> None:
        async with self.async_session() as session:
            if not username:
                raise ValidationError()

            stmt = delete(User).where(User.username == username)

            await session.execute(stmt)
            await session.commit()

    async def check_user_exists(self, username: str) -> None:
        async with self.async_session() as session:
            query = select(User).where(User.username == username).exists()

            exists = await session.execute(statement=query)

            return exists


class UserAuthRepository:
    def __init__(self, async_session: async_sessionmaker[AsyncSession]):
        self.async_session = async_session

    async def get_user_id_and_status(self, username: str) -> "UserSchema":
        async with self.async_session() as session:
            try:
                query = select(
                    User.is_active,
                    User.is_staff,
                ).where(User.username == username)
                query_result = await session.execute(statement=query)
                query_result_row: User = query_result.one_or_none()

                return UserSchema(
                    username=query_result_row.username,
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


user_auth_repository = UserAuthRepository(async_session=async_session)
user_repository = UserRepository(async_session=async_session)
