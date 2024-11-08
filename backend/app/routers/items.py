from fastapi import APIRouter

from ..models.item_create import ItemCreate
from ..models.item_public import ItemPublic


router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
async def read_items():
    return [{"name": "Item Foo"}, {"name": "item Bar"}]

@router.post("/create", response_model=ItemPublic)
async def create_item(item: ItemCreate):
    return item
