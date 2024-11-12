from decimal import Decimal
from typing import Tuple

from sqlmodel import select

from ..dependencies import SessionDep
from ..enums.item_status import ItemStatus
from ..models.item_create import ItemCreate
from ..models.item_public import ItemPublic
from ..params.filter_params import FilterParams
from ..schemas.item import Item
from ..utils import current_local_time, decimal_price_to_string


class ItemsCrud:
    def save_item(self, session: SessionDep, item: Item) -> None:
        session.add(item)
        session.commit()
        session.refresh(item)

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

        return {"items": list(items_public), "total_price": float(total_price)}

    def get_item_by_name(self, session: SessionDep, name: str) -> Item | None:
        return session.exec(select(Item).where(Item.name == name)).first()

    def create_or_update_item(
        self, session: SessionDep, item: ItemCreate
    ) -> Tuple[Item, ItemStatus]:
        item_data = item.model_dump()
        existing_item = self.get_item_by_name(session, item.name)
        current_time = current_local_time()

        if existing_item:
            print("Item already exists, proceeding to update")
            existing_item.sqlmodel_update(item_data)
            existing_item.price = decimal_price_to_string(item.price)
            existing_item.last_updated_dt = current_local_time()
            self.save_item(session, existing_item)
            print(f"Item updated: {existing_item}")
            return existing_item, ItemStatus.UPDATED
        else:
            print("Item does not exist, proceeding to create")
            new_item = Item(**item_data, last_updated_dt=current_time)
            new_item.price = decimal_price_to_string(item.price)
            self.save_item(session, new_item)
            print(f"Item created: {new_item}")
            return new_item, ItemStatus.CREATED


items_crud = ItemsCrud()
