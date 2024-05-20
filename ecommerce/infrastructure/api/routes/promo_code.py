from fastapi import APIRouter
from domain.ecommerce.use_case.promo_code import create_promo_code_logic
from infrastructure.api.dto.dto_promo_code import PromoCodeRequest

router = APIRouter()


@router.post("/promo_code/")
async def create_promo_code(promo_code: PromoCodeRequest):
    return await create_promo_code_logic(promo_code)
