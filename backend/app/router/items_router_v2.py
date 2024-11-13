from fastapi import APIRouter

from ..crud.items_crud_v2 import items_crud_v2
from ..dependencies import SessionDep
from ..params.overall_params import OverallParams

router = APIRouter(
    prefix="/items/v2", tags=["items-v2"], responses={404: {"description": "Not found"}}
)


@router.post("/")
async def read_items_additional_params(
    session: SessionDep, overall_params: OverallParams
):
    return items_crud_v2.read_items_v2(session, overall_params)
