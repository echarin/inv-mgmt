from sqlmodel import select

from ..dependencies import SessionDep
from ..models.item_create import ItemCreate
from ..schemas.item import Item
from ..utils import decimal_price_to_string, local_time


class ItemsCrud:
    def read_items(self, session: SessionDep) -> list[Item]:
        items_db = session.exec(select(Item)).all()
        return list(items_db)
    
    def get_item_by_name(self, session: SessionDep, name: str) -> Item | None:
        return session.exec(select(Item).where(Item.name == name)).first()

    def create_or_update_item(self, session: SessionDep, item: ItemCreate) -> Item:
        item_db = Item(
            **item.model_dump(),
            last_updated_dt=local_time()
        )
        item_db.price = decimal_price_to_string(item.price)

        existing_item = self.get_item_by_name(session, item_db.name)

        if existing_item:
            # Update existing item
            print("Item already exists, proceeding to update")
            existing_item.sqlmodel_update(item.model_dump(exclude_unset=True))
            existing_item.price = decimal_price_to_string(item.price)
            existing_item.last_updated_dt = local_time()
            item_db = existing_item
        else:
            print("Item does not exist, proceeding to create")
        
        session.add(item_db)
        session.commit()
        session.refresh(item_db)

        print(f"Item saved: {item_db.model_dump}")

        return item_db
    
items_crud = ItemsCrud()