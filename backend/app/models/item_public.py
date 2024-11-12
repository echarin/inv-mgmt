from decimal import Decimal

from pydantic import field_serializer

from ..models.item_base import ItemBase


class ItemPublic(ItemBase):
    id: int

    @field_serializer("price")
    def serialize_price(self, price: Decimal) -> float:
        return float(price)
