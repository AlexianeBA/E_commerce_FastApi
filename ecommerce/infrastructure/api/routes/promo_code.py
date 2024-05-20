from fastapi import APIRouter
from fastapi.responses import JSONResponse
from domain.ecommerce.exceptions.exceptions import PromoCodeCreationException
from domain.ecommerce.use_case.promo_code import create_promo_code_logic
from infrastructure.api.dto.dto_promo_code import PromoCodeRequest

router = APIRouter()


@router.post("/promo_code/")
async def create_promo_code(promo_code: PromoCodeRequest):
    try:
        return await create_promo_code_logic(promo_code)
    except PromoCodeCreationException as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
