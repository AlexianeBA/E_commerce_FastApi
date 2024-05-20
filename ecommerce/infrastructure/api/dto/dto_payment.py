from pydantic import BaseModel


class PaymentRequest(BaseModel):
    card_number: str
    card_expiry: str
    card_cvv: str
    amount: float


class PaymentResponse(BaseModel):
    message: str
