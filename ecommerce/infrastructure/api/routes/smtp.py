from fastapi import APIRouter
from domain.ecommerce.use_case.smtp import send_email_logic
from infrastructure.api.dto.dto_smtp import EmailRequest

router = APIRouter()


@router.post("/send_email")
async def send_email(email_request: EmailRequest):
    return await send_email_logic(email_request)
