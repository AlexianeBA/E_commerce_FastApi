from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    stock: int
    description: str
    created_at: datetime
    seller_id: Optional[int]


class ProductRequest(BaseModel):
    name: str
    price: int
    stock: int
    category: str
    rating: int
    on_sale: bool
    is_new: bool
    in_stock: bool
    description: str
    image_url: str
    discount: Optional[int] = None
    discount_end_date: Optional[datetime] = None
