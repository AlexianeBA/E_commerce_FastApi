from pydantic import BaseModel


class ReviewModel(BaseModel):
    product_id: int
    rating: int
    comment: str
