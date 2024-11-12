from unittest.mock import patch

from app.enums.category import Category
from app.enums.item_status import ItemStatus
from app.main import app
from app.schemas.item import Item
from fastapi.testclient import TestClient

client = TestClient(app)

# Mock objects
mock_item = Item(
    id=1,
    name="Test Item",
    category="stationery",
    price="10.00",
    last_updated_dt="2024-11-12T00:00:00",
)

# Mock responses
mock_items_response = {"items": [], "total_price": 0}


@patch("app.crud.items_crud.ItemsCrud.read_items")
def test_read_items_with_default_filter_params_returns_status_200(mock_read_items):
    mock_read_items.return_value = mock_items_response

    response = client.post("/items/", json={})

    assert response.status_code == 200
    assert response.json() == mock_items_response


@patch("app.crud.items_crud.ItemsCrud.read_items")
def test_read_items_with_empty_filter_params_returns_status_200(mock_read_items):
    mock_read_items.return_value = mock_items_response

    response = client.post(
        "/items/",
        json={
            "dt_from": "",
            "dt_to": "",
            "category": "",
        },
    )

    assert response.status_code == 200
    assert response.json() == mock_items_response


@patch("app.crud.items_crud.ItemsCrud.read_items")
def test_read_items_with_valid_filter_params_returns_status_200(mock_read_items):
    mock_read_items.return_value = mock_items_response

    response = client.post(
        "/items/",
        json={
            "dt_from": "2024-11-03 00:00:00",
            "dt_to": "2024-11-14 00:00:00",
            "category": "stationery",
        },
    )

    assert response.status_code == 200
    assert response.json() == mock_items_response


@patch("app.crud.items_crud.ItemsCrud.read_items")
def test_read_items_with_invalid_date_returns_status_422(mock_read_items):
    mock_read_items.return_value = mock_items_response

    response = client.post(
        "/items/",
        json={
            "dt_from": "weirddate",
        },
    )

    assert response.status_code == 422


@patch("app.crud.items_crud.ItemsCrud.read_items")
def test_read_items_with_invalid_date_range_returns_status_422(mock_read_items):
    mock_read_items.return_value = mock_items_response

    response = client.post(
        "/items/",
        json={
            # dt_from is before dt_to
            "dt_from": "2024-11-15 00:00:00",
            "dt_to": "2024-11-13 00:00:00",
            "category": "stationery",
        },
    )

    assert response.status_code == 422


@patch("app.crud.items_crud.ItemsCrud.read_items")
def test_read_items_with_invalid_category_returns_status_422(mock_read_items):
    mock_read_items.return_value = mock_items_response

    response = client.post(
        "/items/",
        json={
            "dt_from": "2024-11-01 00:00:00",
            "dt_to": "2024-11-10 00:00:00",
            "category": "nosuchcategory",
        },
    )

    assert response.status_code == 422


def test_read_categories_returns_status_200():
    response = client.get("/items/categories")

    assert response.status_code == 200
    assert response.json() == Category.values()


@patch("app.crud.items_crud.ItemsCrud.create_or_update_item")
def test_create_item_with_valid_item_returns_status_201_and_created(
    mock_create_or_update_item,
):
    mock_create_or_update_item.return_value = (mock_item, ItemStatus.CREATED)

    response = client.post(
        "/items/create",
        json={
            "name": "Test Item", 
            "category": "stationery", 
            "price": "10.00"
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": mock_item.id, 
        "status": ItemStatus.CREATED.value
    }

@patch("app.crud.items_crud.ItemsCrud.create_or_update_item")
def test_create_item_with_existing_item_returns_status_201_and_created(
    mock_create_or_update_item,
):
    mock_create_or_update_item.return_value = (mock_item, ItemStatus.UPDATED)

    response = client.post(
        "/items/create",
        json={
            "name": "Test Item", 
            "category": "stationery", 
            "price": "10.00"
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": mock_item.id, 
        "status": ItemStatus.UPDATED.value
    }

def test_create_item_with_invalid_request_bodies_returns_status_422():
    '''
    Three scenarios to test
    1. Name below minimum length of 1
    2. Category does not exist
    3. Price exceeds 2 decimal places
    4. Price is below 0
    '''
    
    response = client.post(
        "/items/create",
        json={
            "name": "", 
            "category": "stationery", 
            "price": "10.00"
        },
    )

    assert response.status_code == 422

    response = client.post(
        "/items/create",
        json={
            "name": "Test Item", 
            "category": "nosuchcategory", 
            "price": "10.00"
        },
    )

    assert response.status_code == 422

    response = client.post(
        "/items/create",
        json={
            "name": "Test Item", 
            "category": "stationery", 
            "price": "5.555555"
        },
    )

    assert response.status_code == 422

    response = client.post(
        "/items/create",
        json={
            "name": "Test Item", 
            "category": "stationery", 
            "price": "-1.0"
        },
    )

    assert response.status_code == 422
