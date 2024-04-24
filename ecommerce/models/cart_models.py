from datetime import datetime

from pydantic import BaseModel


class CartItem(BaseModel):
    product_id: int
    quantity: int


class Cart(BaseModel):
    id: int
    buyer_id: int
    items: list[CartItem]
    total: int
    created_at: datetime
