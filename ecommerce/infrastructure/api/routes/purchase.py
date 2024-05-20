from fastapi import APIRouter

from domain.ecommerce.use_case.purchase import get_buyers_info_logic


router = APIRouter()


@router.get("/seller/{seller_id}/buyers")
async def get_buyers_info(seller_id: int):
    return await get_buyers_info_logic(seller_id)
