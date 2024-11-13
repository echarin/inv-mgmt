from pydantic import Field

from .params import Params

DEFAULT_PAGE: int = 1
DEFAULT_LIMIT: int = 10


class PaginationParams(Params):
    page: int | None = Field(default=DEFAULT_PAGE, gt=0)
    limit: int | None = Field(default=DEFAULT_LIMIT, gt=0, le=100)
