from datetime import datetime
from typing import Self

from pydantic import field_validator, model_validator

from ..enums.category import Category
from .params import Params


class FilterParams(Params):
    dt_from: datetime | None = None
    dt_to: datetime | None = None
    category: Category | None = None

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")
        }

    # allows frontend to send empty strings for fields
    @field_validator('dt_from', 'dt_to', 'category', mode='before')
    @classmethod
    def empty_string_to_none(cls, value):
        if value == '':
            return None
        return value
    
    @model_validator(mode="after")
    def validate_date_range(self) -> Self:
        dt_to = self.dt_to
        dt_from = self.dt_from
        if dt_to and dt_from and dt_to < dt_from:
            raise ValueError('dt_to must be greater than or equal to dt_from')
        return self