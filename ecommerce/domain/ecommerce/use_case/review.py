from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from infrastructure.api.dto.dto_review import ReviewModel
from infrastructure.api.routes.auth import (
    get_current_active_buyer_logic,
    get_current_user_logic,
)
from models import Product, Review


async def add_review_logic(
    review: ReviewModel, current_user=Depends(get_current_user_logic)
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


async def get_reviews_by_user_id_logic(user_id: int):
    reviews = await Review.objects().where(Review.user_id == user_id).run()
    return JSONResponse(content=[review.to_dict() for review in reviews])


async def get_reviews_by_product_id_logic(product_id: int):
    reviews = await Review.objects().where(Review.product_id == product_id).run()
    return JSONResponse(content=[review.to_dict() for review in reviews])


async def get_review_by_id_logic(review_id: int):
    review = await Review.objects().where(Review.id == review_id).first().run()
    if review:
        return JSONResponse(content=review.to_dict())
    else:
        return JSONResponse(content={"message": "Review not found"}, status_code=404)
