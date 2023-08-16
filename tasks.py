from email.message import EmailMessage
import smtplib, ssl
from celery import Celery
from settings import settings

celery = Celery(
    __name__,
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    broker_connection_retry_on_startup=True,
    redbeat_redis_url=settings.CELERY_BROKER_URL,
    redbeat_lock_key=None,
    enable_utc=False,
    beat_max_loop_interval=5,
    beat_scheduler='redbeat.schedulers.RedBeatScheduler'
)


@celery.task
def send_notification(email, mail_content, subject):
    message = EmailMessage()
    message["From"] = settings.EMAIL
    message["To"] = email
    message["Subject"] = subject
    message.set_content(mail_content)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(user=settings.EMAIL, password=settings.PASSWORD)
        smtp.sendmail(settings.EMAIL, email, message.as_string())
        smtp.quit()
    return f'{email}send'
