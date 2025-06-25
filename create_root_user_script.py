from logging import getLogger
from os import getenv

from asyncio import run

from sqlalchemy import insert, select

from config import async_session

from files import User, PasswordHandlingUtil


logger = getLogger("logger")


async def create_root_user():
    username = input("username (default 'root'): ")
    if not username:
        username = "root"

    password = input("password (default 'root'): ")
    if not password:
        password = "root"

    hashed_password = PasswordHandlingUtil.hash_password(password=password)
    async with async_session() as session:
        query_get_user = select(User.username).where(User.username == username)
        result = await session.execute(query_get_user)
        user_username = result.scalar_one_or_none()
        if user_username is not None:
            logger.debug("User already exists")
            return

        stmt_insert_user = insert(User).values(
            username=username,
            password=hashed_password,
            is_active=True,
            is_superuser=True,
        )

        await session.execute(stmt_insert_user)
        await session.commit()

        logger.debug("User has been created successfully")


run(create_root_user())
