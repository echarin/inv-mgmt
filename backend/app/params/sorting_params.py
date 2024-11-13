from typing import Literal

from pydantic import Field

from .params import Params


class SortingParams(Params):
    field: Literal["id", "name", "price", "category"] = Field(None)
    order: Literal["asc", "desc"] = Field(None)
