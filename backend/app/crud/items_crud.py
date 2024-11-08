from sqlmodel import select

from ..dependencies import SessionDep
from ..models.item_create import ItemCreate
from ..schemas.item import Item
from ..utils import float_price_to_string, local_time


class ItemsCrud:
    def read_items(self, session: SessionDep):
        items = session.exec(select(Item)).all()
        return items

    def create_item(self, session: SessionDep, item: ItemCreate):
        item_db = Item(
            **item.model_dump(),
            last_updated_dt=local_time()
        )

        item_db.price = float_price_to_string(item.price)
        print(item_db.model_dump)

        session.add(item_db)
        session.commit()
        session.refresh(item_db)
        return item_db
    
items_crud = ItemsCrud()