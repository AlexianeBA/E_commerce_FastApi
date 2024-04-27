from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CartRequest(BaseModel):
    product_id: int
    quantity: int
    promotional_code: Optional[str]


class CartResponse(BaseModel):
    id: int
    buyer_id: int
    items: list[CartRequest]
    total: int
    created_at: datetime
    promotional_code: Optional[str]


class CartItemResponse(BaseModel):
    product_id: int
    quantity: int
    promotional_code: Optional[str]
