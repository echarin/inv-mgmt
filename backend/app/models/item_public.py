from decimal import Decimal

from ..models.item_base import ItemBase

# test
class ItemPublic(ItemBase):
    id: int

    # ensures that Decimal is serialised to float
    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }