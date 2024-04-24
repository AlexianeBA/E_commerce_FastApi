from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ProductModel(BaseModel):
    id: int
    name: str
    price: int
    stock: int
    description: str


class ProductIn(BaseModel):
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
