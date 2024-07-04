import logging
import smtplib
from email.message import EmailMessage

from pydantic import EmailStr

from app.config import config

logger = logging.getLogger(__name__)


def send_email(email: EmailStr, subject: str, content: str):
    logger.debug(f"Sending email to {email}.")
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = f"tomasemilio<{config.ADMIN_EMAIL}>"
        msg["To"] = email
        msg.set_content(content)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(config.ADMIN_EMAIL, config.ADMIN_EMAIL_TOKEN)
            smtp.send_message(msg)
        logger.info(f"Email sent to {email}.")
    except Exception as e:
        logger.error(f"Email not sent to {email}. {e}")
