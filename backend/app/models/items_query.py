from pydantic import BaseModel

from ..models.item_public import ItemPublic


class ItemsQuery(BaseModel):
    items: list[ItemPublic]
    total_price: float
