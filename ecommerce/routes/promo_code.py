from dto.dto_promo_code import PromoCodeRequest
from models import PromotionalCode
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/promo_code/")
async def create_promo_code(promo_code: PromoCodeRequest):
    new_promo_code = PromotionalCode(
        code=promo_code.code,
        discount=promo_code.discount,
        start_date=promo_code.start_date,
        end_date=promo_code.end_date,
    )
    await new_promo_code.save()
    return {
        "message": f"Promo code {promo_code.code} created with discount {promo_code.discount}% from {promo_code.start_date} to {promo_code.end_date}"
    }
