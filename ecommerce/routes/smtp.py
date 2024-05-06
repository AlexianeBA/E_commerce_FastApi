import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import APIRouter, HTTPException, status

from dto.dto_smtp import EmailRequest

router = APIRouter()

email = "MS_0t7ir0@trial-3zxk54vn9jxljy6v.mlsender.net"
password = "uHUmWHV9uiUdgrVA"


@router.post("/send_email")
async def send_email(email, password, email_request: EmailRequest):
    try:
        msg = MIMEMultipart()
        msg["From"] = email
        msg["To"] = email_request.receiver_email
        msg["Subject"] = email_request.subject
        msg.attach(MIMEText(email_request.body, "plain"))
        server = smtplib.SMTP("smtp.mailersend.net", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email_request.receiver_email, msg.as_string())
        server.quit()
        return "Email sent successfully"
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
