from pydantic import BaseModel
from files.apps.user.models import User
from .repository import UserRepository, user_repository


class UserModelsAdapter:
    """
    Provides user's models for outer apps
    """

    def __init__(self, models: list[BaseModel]):
        for model in models:
            class_name = model.__name__
            setattr(self, class_name, model)

    def get_attributes(self):
        return vars(self)


class UserSchemasAdapter:
    """
    Provides user's schemas for outer apps
    """

    def __init__(self, schemas: list[BaseModel]):
        for schema in schemas:
            class_name = schema.__name__
            setattr(self, class_name, schema)

    def get_schemas(self):
        return vars(self)


class UserRepositoryAdapter:
    """
    Provides user's repository requests for outer apps
    """

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def list_users(
        self,
        filter: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ):
        users_dto = await self.repository.get_users(
            filter=filter,
            limit=limit,
            offset=offset,
        )

        return users_dto

    async def check_user_exists(self, username: str) -> bool:
        exists = self.repository.check_user_exists(username)

        return exists


user_models_adapter = UserModelsAdapter(models=[User])
# user_schemas_adapter = UserSchemasAdapter(schemas=[UserSchema])
user_repository_adapter = UserRepositoryAdapter(repository=user_repository)
