from fastapi import APIRouter, HTTPException, status, Depends

from models.review_models import ReviewModel
from routes.auth import get_current_active_buyer, get_current_user
from tables import Product, Review

router = APIRouter()


@router.post("/reviews")
async def add_review(
    review: ReviewModel, current_user=Depends(get_current_user)
) -> dict:
    user_id = current_user.id
    product = (
        await Product.objects().where(Product.id == review.product_id).first().run()
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    new_review = await Review.objects().create(
        user_id=user_id,
        product_id=review.product_id,
        rating=review.rating,
        comment=review.comment,
    )

    return new_review.to_dict()
