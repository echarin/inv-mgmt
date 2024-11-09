from decimal import Decimal

from sqlmodel import select

from ..dependencies import SessionDep
from ..models.item_create import ItemCreate
from ..models.item_public import ItemPublic
from ..params.filter_params import FilterParams
from ..schemas.item import Item
from ..utils import current_local_time, decimal_price_to_string


class ItemsCrud:
    def create_item_query(self, filter_params: FilterParams):
        query = select(Item)
        if filter_params.dt_from:
            query = query.where(Item.last_updated_dt >= filter_params.dt_from)
        
        if filter_params.dt_to:
            query = query.where(Item.last_updated_dt <= filter_params.dt_to)

        if filter_params.category:
            query = query.where(Item.category == filter_params.category)

        return query

    def read_items(self, session: SessionDep, filter_params: FilterParams) -> dict:
        query = self.create_item_query(filter_params)
        items_db = session.exec(query).all()

        items_public: list[ItemPublic] = []
        total_price: Decimal = Decimal(0)
        for item in items_db:
            item_public = ItemPublic.model_validate(item)
            items_public.append(item_public)
            total_price += item_public.price

        return { 
            "items": list(items_public),
            "total_price": float(total_price)
        }
    
    def get_item_by_name(self, session: SessionDep, name: str) -> Item | None:
        return session.exec(select(Item).where(Item.name == name)).first()

    def create_or_update_item(self, session: SessionDep, item: ItemCreate) -> Item:
        item_db = Item(
            **item.model_dump(),
            last_updated_dt=current_local_time()
        )
        item_db.price = decimal_price_to_string(item.price)

        existing_item = self.get_item_by_name(session, item_db.name)

        if existing_item:
            print("Item already exists, proceeding to update")
            existing_item.sqlmodel_update(item.model_dump(exclude_unset=True))
            existing_item.price = decimal_price_to_string(item.price)
            existing_item.last_updated_dt = current_local_time()
            item_db = existing_item
        else:
            print("Item does not exist, proceeding to create")
        
        session.add(item_db)
        session.commit()
        session.refresh(item_db)

        print(f"Item saved: {item_db.model_dump}")

        return item_db
    
items_crud = ItemsCrud()