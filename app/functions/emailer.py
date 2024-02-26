import logging
import smtplib
from email.message import EmailMessage

from pydantic import EmailStr

from app.config import config

logger = logging.getLogger(__name__)


def send_confirmation_email(email: EmailStr, url: str):
    msg = EmailMessage()
    msg["Subject"] = "Confirm your email"
    msg["From"] = f"FastAPI Boilerplate<{config.EMAIL_USERNAME}>"
    msg["To"] = email
    msg.set_content(
        f"""
        Click the link below to confirm your email:
        {url}
        """
    )
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(config.EMAIL_USERNAME, config.EMAIL_TOKEN)
        smtp.send_message(msg)
    logger.debug(f"Confirmation email sent to {email}.")
