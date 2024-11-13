from typing import Literal
from .params import Params

class SortingParams(Params):
    field: Literal["id", "name", "price", "category"] | None
    order: Literal["asc", "desc"] = "asc"
