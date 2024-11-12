from datetime import timedelta
from decimal import Decimal

import pytest
from app.crud.items_crud import ItemsCrud
from app.enums.category import Category
from app.enums.item_status import ItemStatus
from app.models.item_create import ItemCreate
from app.params.filter_params import FilterParams
from app.utils import current_local_time, decimal_price_to_string
from sqlmodel import Session, SQLModel, create_engine


@pytest.fixture(scope="function")
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="module")
def items_crud():
    return ItemsCrud()


@pytest.fixture
def item1():
    return ItemCreate(
        name="Item 1", category=Category.stationery.value, price=Decimal("5.50")
    )


@pytest.fixture
def item2():
    return ItemCreate(
        name="Item 2", category=Category.books.value, price=Decimal("15.00")
    )


def add_items(session, items_crud, *items):
    for item in items:
        items_crud.create_or_update_item(session, item)


def test_read_items_no_filters(session, items_crud, item1, item2):
    add_items(session, items_crud, item1, item2)

    filter_params = FilterParams()
    result = items_crud.read_items(session, filter_params)

    assert len(result["items"]) == 2
    assert result["total_price"] == float(item1.price + item2.price)

    item_names = [item.name for item in result["items"]]
    assert "Item 1" in item_names
    assert "Item 2" in item_names


def test_read_items_filter_by_category(session, items_crud, item1, item2):
    add_items(session, items_crud, item1, item2)

    filter_params = FilterParams(category=Category.stationery.value)
    result = items_crud.read_items(session, filter_params)

    assert len(result["items"]) == 1
    assert result["total_price"] == float(item1.price)
    item = result["items"][0]
    assert item.name == item1.name
    assert item.category == item1.category
    assert item.price == float(item1.price)


def test_read_items_filter_by_date_range(session, items_crud, item1, item2):
    add_items(session, items_crud, item1, item2)

    past_date = current_local_time() - timedelta(days=365)
    future_date = current_local_time() + timedelta(days=365)
    filter_params = FilterParams(dt_from=past_date, dt_to=future_date)
    result = items_crud.read_items(session, filter_params)

    assert len(result["items"]) == 2


def test_read_items_filter_no_results(session, items_crud, item1, item2):
    add_items(session, items_crud, item1, item2)

    # We did not save anything under "furniture"
    filter_params = FilterParams(category=Category.furniture)
    result = items_crud.read_items(session, filter_params)

    assert len(result["items"]) == 0
    assert result["total_price"] == 0


def test_create_item(session, items_crud, item1):
    created_item, status = items_crud.create_or_update_item(session, item1)

    assert status == ItemStatus.CREATED
    assert created_item.name == item1.name
    assert created_item.category == item1.category
    assert created_item.price == decimal_price_to_string(item1.price)


def test_update_item(session, items_crud, item1):
    items_crud.create_or_update_item(session, item1)
    updated_item = ItemCreate(
        name=item1.name, category=Category.electronics.value, price=Decimal("10.00")
    )

    created_item, status = items_crud.create_or_update_item(session, updated_item)

    assert status == ItemStatus.UPDATED
    assert created_item.name == updated_item.name
    assert created_item.category == updated_item.category
    assert created_item.price == decimal_price_to_string(updated_item.price)
