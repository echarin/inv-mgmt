from .filter_params import FilterParams


class FilterParamsV2(FilterParams):
    name_contains: str | None = None
    price_range: tuple[int, int] | None = None
