from sqlmodel import Field
from backend.models.item_base import ItemBase


class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # price: str = Field(index=True)
    # last_updated_dt: str = Field(default=None, index=True)