from sqlmodel import Field, SQLModel

from backend.models.category import Category


class ItemBase(SQLModel):
    name: str = Field(min_length=1, index=True)
    category: Category = Field(index=True)
    price: float = Field(default=0.0, ge=0.0, index=True)