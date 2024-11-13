from .filter_params_v2 import FilterParamsV2
from .pagination_params import PaginationParams
from .params import Params
from .sorting_params import SortingParams


class OverallParams(Params):
    filters: FilterParamsV2 | None
    pagination: PaginationParams | None
    sort: SortingParams | None
