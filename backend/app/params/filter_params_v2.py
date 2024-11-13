from typing import Self

from pydantic import field_validator, model_validator

from .filter_params import FilterParams


class FilterParamsV2(FilterParams):
    name_contains: str | None = None
    price_range: tuple[int, int] | None = None

    @field_validator("name_contains", mode="before")
    @classmethod
    def empty_string_to_none(cls, value):
        if value == "":
            return None
        return value

    @model_validator(mode="after")
    def validate_price_range(self) -> Self:
        if self.price_range:
            min_price, max_price = self.price_range
            if max_price < min_price:
                raise ValueError("Max price must be greater than or equal to min price")
        return self
