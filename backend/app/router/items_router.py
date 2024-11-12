from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from ..crud.items_crud import items_crud
from ..dependencies import SessionDep
from ..enums.category import Category
from ..enums.item_status import ItemStatus
from ..models.item_create import ItemCreate
from ..params.filter_params import FilterParams

router = APIRouter(
    prefix="/items", tags=["items"], responses={404: {"description": "Not found"}}
)

STATUS_CODE_MAPPING = {
    ItemStatus.CREATED: status.HTTP_201_CREATED,
    ItemStatus.UPDATED: status.HTTP_200_OK,
}


@router.post("/")
async def read_items(session: SessionDep, filter_params: FilterParams):
    return items_crud.read_items(session, filter_params)


@router.get("/categories")
async def read_categories():
    return Category.values()


@router.post("/create")
async def create_item(session: SessionDep, item: ItemCreate):
    item_created, status = items_crud.create_or_update_item(session, item)
    return JSONResponse(
        status_code=STATUS_CODE_MAPPING[status], 
        content={
            "id": item_created.id,
            "status": status.value
        }
    )
