from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse

from dto.dto_review import ReviewModel
from routes.auth import get_current_active_buyer, get_current_user
from models import Product, Review

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


@router.get("/reviews/{user_id}")
async def get_reviews_by_user_id(user_id: int):
    reviews = await Review.objects().where(Review.user_id == user_id).run()
    return JSONResponse(content=[review.to_dict() for review in reviews])


@router.get("/reviews/{product_id}")
async def get_reviews_by_product_id(product_id: int):
    reviews = await Review.objects().where(Review.product_id == product_id).run()
    return JSONResponse(content=[review.to_dict() for review in reviews])


@router.get("/reviews/{review_id}")
async def get_review_by_id(review_id: int):
    review = await Review.objects().where(Review.id == review_id).first().run()
    if review:
        return JSONResponse(content=review.to_dict())
    else:
        return JSONResponse(content={"message": "Review not found"}, status_code=404)
