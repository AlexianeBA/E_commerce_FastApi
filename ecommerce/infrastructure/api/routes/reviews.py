from fastapi import APIRouter, Depends
from domain.ecommerce.use_case.auth import get_current_user_logic
from domain.ecommerce.use_case.review import (
    add_review_logic,
    get_reviews_by_user_id_logic,
    get_reviews_by_product_id_logic,
    get_review_by_id_logic,
)
from infrastructure.api.dto.dto_review import ReviewModel

router = APIRouter()


@router.post("/reviews")
async def add_review(
    review: ReviewModel, current_user=Depends(get_current_user_logic)
) -> dict:
    return await add_review_logic(review, current_user)


@router.get("/reviews/{user_id}")
async def get_reviews_by_user_id(user_id: int):
    return await get_reviews_by_user_id_logic(user_id)


@router.get("/reviews/{product_id}")
async def get_reviews_by_product_id(product_id: int):
    return await get_reviews_by_product_id_logic(product_id)


@router.get("/reviews/{review_id}")
async def get_review_by_id(review_id: int):
    return await get_review_by_id_logic(review_id)
