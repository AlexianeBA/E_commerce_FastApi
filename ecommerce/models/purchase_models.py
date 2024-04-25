from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PurchaseModel(BaseModel):
    id: int
    buyer_id: int
    product_id: int
    quantity: int
    total: int
    purchase_date: Optional[datetime]
