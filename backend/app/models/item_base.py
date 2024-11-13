from decimal import Decimal

from sqlmodel import Field, SQLModel

from ..enums.category import Category


class ItemBase(SQLModel):
    name: str = Field(min_length=1, index=True)
    category: Category = Field(index=True)
    price: Decimal = Field(ge=0.0, decimal_places=2, index=True)
