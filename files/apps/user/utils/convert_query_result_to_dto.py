from typing import List, Any, TypeVar, Type

from pydantic import BaseModel

T = TypeVar("T")
U = TypeVar("U")


def convert_query_result_to_dto[T, U](
    result: Type[List[U] | U], schema: Type[T]
) -> T | List[T]:
    """
    Converts query result to pydantic model

    :param result: result of db query
    :param schema: pydantic model schema

    :return:  pydantic model
    """

    if isinstance(result, list):
        return [schema.model_validate(model, from_attributes=True) for model in result]

    return schema.model_validate(result, from_attributes=True)
