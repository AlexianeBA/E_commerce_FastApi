from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from domain.ecommerce.exceptions.exceptions import EmailSendingException
from domain.ecommerce.use_case.smtp import send_email_logic
from infrastructure.api.dto.dto_smtp import EmailRequest

router = APIRouter()


@router.post("/send_email")
async def send_email(email_request: EmailRequest):
    try:
        return await send_email_logic(email_request)
    except EmailSendingException as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )
