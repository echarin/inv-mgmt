from sqlmodel import select

from ..dependencies import SessionDep
from ..models.item_create import ItemCreate
from ..schemas.item_db import ItemDb
from ..utils import decimal_price_to_string, local_time


class ItemsCrud:
    def save_item(self, session: SessionDep, item: ItemDb):
        session.add(item)
        session.commit()
        session.refresh(item)

    def read_items(self, session: SessionDep):
        items_db = session.exec(select(ItemDb)).all()
        print(f"Items in db found: {items_db}")
        return items_db
    
    def get_names(self, session: SessionDep):
        return session.exec(select(ItemDb.name).distinct()).all()

    def create_item(self, session: SessionDep, item: ItemCreate):
        # check if name already exists
        if item.name in self.get_names(session):
            print("Item already exists, proceeding to update")
            return self.update_item_by_name(session, item)

        item_db = ItemDb(
            **item.model_dump(),
            last_updated_dt=local_time()
        )

        item_db.price = decimal_price_to_string(item.price)

        self.save_item(session, item_db)

        print(f"Item saved: {item_db.model_dump}")

        return item_db
    
    def update_item_by_name(self, session: SessionDep, item: ItemCreate):
        item_db = session.exec(select(ItemDb).where(ItemDb.name == item.name)).first()
        if item_db:
            item_data = item.model_dump() # no need exclude_unset=True since all fields are filled
            item_db.sqlmodel_update(item_data)
            item_db.price = decimal_price_to_string(item.price)
            item_db.last_updated_dt = local_time()

            self.save_item(session, item_db)

            return item_db
        else:
            raise Exception("Item not found")
    
items_crud = ItemsCrud()