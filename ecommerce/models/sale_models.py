from pydantic import BaseModel
from datetime import datetime


class SaleIn(BaseModel):
    category: str
    discount: float
    start_date: datetime
    end_date: datetime
