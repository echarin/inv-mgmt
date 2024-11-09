from fastapi import APIRouter

from ..crud.items_crud import items_crud
from ..dependencies import SessionDep
from ..enums.category import Category
from ..models.item_create import ItemCreate
from ..models.item_public import ItemPublic

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=list[ItemPublic])
async def read_items(session: SessionDep):
    return items_crud.read_items(session)

@router.get("/categories")
async def read_categories():
    return Category.values()

@router.post("/create")
async def create_item(session: SessionDep, item: ItemCreate):
    item_created = items_crud.create_item(session, item)
    return { "id": item_created.id }
