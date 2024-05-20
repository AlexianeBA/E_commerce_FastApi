from fastapi import Depends
from fastapi.responses import JSONResponse
from domain.ecommerce.exceptions.exceptions import (
    ProductNotFoundException,
    ReviewNotFoundException,
)
from infrastructure.api.dto.dto_review import ReviewModel
from infrastructure.api.routes.users import (
    get_current_user_logic,
)
from models.product_models import Product
from models.review_models import Review


async def add_review_logic(
    review: ReviewModel, current_user=Depends(get_current_user_logic)
) -> dict:
    user_id = current_user.id
    product = (
        await Product.objects().where(Product.id == review.product_id).first().run()
    )
    if not product:
        raise ProductNotFoundException("Product not found")

    new_review = await Review.objects().create(
        user_id=user_id,
        product_id=review.product_id,
        rating=review.rating,
        comment=review.comment,
    )

    return new_review.to_dict()


async def get_reviews_by_user_id_logic(user_id: int):
    reviews = await Review.objects().where(Review.user_id == user_id).run()
    if not reviews:
        raise ReviewNotFoundException("No reviews found for this user")
    return JSONResponse(content=[review.to_dict() for review in reviews])


async def get_reviews_by_product_id_logic(product_id: int):
    reviews = await Review.objects().where(Review.product_id == product_id).run()
    if not reviews:
        raise ReviewNotFoundException("No reviews found for this product")
    return JSONResponse(content=[review.to_dict() for review in reviews])


async def get_review_by_id_logic(review_id: int):
    review = await Review.objects().where(Review.id == review_id).first().run()
    if not review:
        raise ReviewNotFoundException("Review not found")
    return JSONResponse(content=review.to_dict())
