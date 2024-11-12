from fastapi import APIRouter

from ..crud.items_crud import items_crud
from ..dependencies import SessionDep
from ..enums.category import Category
from ..models.item_create import ItemCreate
from ..params.filter_params import FilterParams

router = APIRouter(
    prefix="/items", tags=["items"], responses={404: {"description": "Not found"}}
)


@router.post("/")
async def read_items(session: SessionDep, filter_params: FilterParams):
    return items_crud.read_items(session, filter_params)


@router.get("/categories")
async def read_categories():
    return Category.values()


@router.post("/create")
async def create_item(session: SessionDep, item: ItemCreate):
    item_created, status = items_crud.create_or_update_item(session, item)
    return {"id": item_created.id, "status": status.value}
