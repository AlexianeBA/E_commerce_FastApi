from pydantic import BaseModel
from datetime import datetime


class PromoCodeRequest(BaseModel):
    code: str
    discount: int
    start_date: datetime
    end_date: datetime
