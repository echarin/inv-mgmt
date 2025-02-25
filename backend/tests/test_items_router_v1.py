from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from backend.app.enums.category import Category
from backend.app.enums.item_status import ItemStatus
from backend.app.main import app
from backend.app.schemas.item import Item

client = TestClient(app)


@pytest.fixture
def mock_item():
    return Item(
        id=1,
        name="Test Item",
        category="stationery",
        price="10.00",
        last_updated_dt="2024-11-12T00:00:00",
    )


@pytest.fixture
def mock_items_response():
    return {"items": [], "total_price": 0}


# needed to update the module and class names
@patch("backend.app.crud.items_crud_v1.ItemsCrudV1.read_items")
def test_read_items_with_default_filter_params(mock_read_items, mock_items_response):
    mock_read_items.return_value = mock_items_response

    response = client.post("/items/", json={})

    assert response.status_code == 200
    assert response.json() == mock_items_response


@patch("backend.app.crud.items_crud_v1.ItemsCrudV1.read_items")
def test_read_items_with_empty_filter_params(mock_read_items, mock_items_response):
    mock_read_items.return_value = mock_items_response

    response = client.post(
        "/items/",
        json={"dt_from": "", "dt_to": "", "category": ""},
    )

    assert response.status_code == 200
    assert response.json() == mock_items_response


@patch("backend.app.crud.items_crud_v1.ItemsCrudV1.read_items")
def test_read_items_with_valid_filter_params(mock_read_items, mock_items_response):
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


@patch("backend.app.crud.items_crud_v1.ItemsCrudV1.read_items")
def test_read_items_with_invalid_date(mock_read_items, mock_items_response):
    mock_read_items.return_value = mock_items_response

    response = client.post(
        "/items/",
        json={"dt_from": "weirddate"},
    )

    assert response.status_code == 422


@patch("backend.app.crud.items_crud_v1.ItemsCrudV1.read_items")
def test_read_items_with_invalid_date_range(mock_read_items, mock_items_response):
    mock_read_items.return_value = mock_items_response

    response = client.post(
        "/items/",
        json={
            "dt_from": "2024-11-15 00:00:00",
            "dt_to": "2024-11-13 00:00:00",
            "category": "stationery",
        },
    )

    assert response.status_code == 422


@patch("backend.app.crud.items_crud_v1.ItemsCrudV1.read_items")
def test_read_items_with_invalid_category(mock_read_items, mock_items_response):
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


@patch("backend.app.crud.items_crud_v1.ItemsCrudV1.create_or_update_item")
def test_create_item_with_valid_item_returns_status_201(
    mock_create_or_update_item, mock_item
):
    mock_create_or_update_item.return_value = (mock_item, ItemStatus.CREATED)

    response = client.post(
        "/items/create",
        json={"name": "Test Item", "category": "stationery", "price": "10.00"},
    )

    assert response.status_code == 201
    assert response.json() == {"id": mock_item.id, "status": ItemStatus.CREATED.value}


@patch("backend.app.crud.items_crud_v1.ItemsCrudV1.create_or_update_item")
def test_create_item_with_existing_item_returns_status_200(
    mock_create_or_update_item, mock_item
):
    mock_create_or_update_item.return_value = (mock_item, ItemStatus.UPDATED)

    response = client.post(
        "/items/create",
        json={"name": "Test Item", "category": "stationery", "price": "10.00"},
    )

    assert response.status_code == 200
    assert response.json() == {"id": mock_item.id, "status": ItemStatus.UPDATED.value}


# Parameterized test for invalid create item request bodies
@pytest.mark.parametrize(
    "invalid_body",
    [
        # Name below min length
        {"name": "", "category": "stationery", "price": "10.00"},
        # Invalid category
        {"name": "Test Item", "category": "nosuchcategory", "price": "10.00"},
        # Price with excessive decimals
        {"name": "Test Item", "category": "stationery", "price": "5.555555"},
        # Negative price
        {"name": "Test Item", "category": "stationery", "price": "-1.0"},
    ],
)
def test_create_item_with_invalid_request_bodies(invalid_body):
    response = client.post(
        "/items/create",
        json=invalid_body,
    )

    assert response.status_code == 422
