import logging
from typing import Tuple, TypeVar, List, Dict, Any, Type, Optional, cast

try:
    from pydantic import BaseModel
except ModuleNotFoundError:
    logging.exception("missing pydantic, please install using msql[pydantic]")

T = TypeVar("T", bound=BaseModel)


def to_pydantic_model(schema: Type[T], data: Optional[Tuple]) -> Optional[T]:
    if not data:
        return None
    ret: Dict[str, Any] = {}
    for index, key in enumerate(schema.__fields__):
        ret[key] = data[index]
    return schema(**ret)


def to_pydantic_list(schema: Type[T], data: List[Tuple]) -> List[T]:
    return [cast(T, to_pydantic_model(schema, x)) for x in data]
