from pydantic import BaseModel


class EmailRequest(BaseModel):
    receiver_email: str
    subject: str
    body: str
