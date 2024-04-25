from pydantic import BaseModel


class Sale(BaseModel):
    id: int
    buyer_username: str
    age_buyer: int
    sexe_buyer: str
    location_buyer: str
