from typing import List
from pydantic import BaseModel


class OrderItemModel(BaseModel):
    product_id: int
    quantity: int


class OrderModel(BaseModel):
    id: int
    buyer_id: int
    items: List[OrderItemModel]
