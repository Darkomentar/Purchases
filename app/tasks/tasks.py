import smtplib
from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings
from app.tasks.celery import celery


@celery.task
def process_mailing(mails: list[EmailStr], message: str):
    email = EmailMessage()
    email["Subject"] = "Новая цена актива"
    email["From"] = settings.SMTP_USER
    # mails =  ", ".join(mails)
    email["To"] = mails
    # email["To"] = settings.SMTP_USER
    email.set_content(message)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(email)
