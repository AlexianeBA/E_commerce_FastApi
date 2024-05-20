import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import APIRouter, HTTPException, status

from domain.ecommerce.exceptions.exceptions import EmailSendingException
from infrastructure.api.dto.dto_smtp import EmailRequest

email = "MS_0t7ir0@trial-3zxk54vn9jxljy6v.mlsender.net"
password = "uHUmWHV9uiUdgrVA"


async def send_email_logic(email_request: EmailRequest):
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
    except:
        raise EmailSendingException("Email not sent")
