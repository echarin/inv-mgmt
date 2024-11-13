from datetime import datetime

from sqlmodel import Field

from ..models.item_base import ItemBase
from ..utils import current_local_time


class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    price: str = Field(index=True)
    last_updated_dt: datetime = Field(default_factory=current_local_time, index=True)
