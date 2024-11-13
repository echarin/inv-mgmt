from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from ..crud.items_crud import items_crud
from ..dependencies import SessionDep
from ..enums.category import Category
from ..enums.item_status import ItemStatus
from ..models.item_create import ItemCreate
from ..params.filter_params import FilterParams

router = APIRouter(
    prefix="/items/v2", tags=["items-v2"], responses={404: {"description": "Not found"}}
)

STATUS_CODE_MAPPING = {
    ItemStatus.CREATED: status.HTTP_201_CREATED,
    ItemStatus.UPDATED: status.HTTP_200_OK,
}


@router.post("/")
async def read_items_additional_params(session: SessionDep, filter_params: FilterParams):
    return items_crud.read_items(session, filter_params)