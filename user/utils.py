import datetime
import jwt
from datetime import datetime, timedelta
from settings import settings
from os import environ
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema
from dotenv import load_dotenv
import smtplib,ssl
from email.message import EmailMessage

load_dotenv()


def create_access_token(data: dict,
                        expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    """
    This function is created for encoding
    :param data: the user info or metadata
    :param expires_delta: after this time the token will expire
    :return: encoded jwt
    """
    now = datetime.utcnow()
    data.update({"exp": now + expires_delta, "iat": now})

    encoded_jwt = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    This function is created for decode the token
    :param token: generated token
    :return: payload which is metadata
    """
    try:
        payload = jwt.decode(token, environ.get("SECRET_KEY"), algorithms=[environ.get("ALGORITHM")])
        return payload
    except jwt.PyJWTError as e:
        raise e


def send_mail(email, token):
    message = EmailMessage()
    message["From"] = settings.EMAIL
    message["To"] = email
    message["Subject"] = "User registration"
    message.set_content(token)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(user=settings.EMAIL, password=settings.PASSWORD)
        smtp.sendmail(settings.EMAIL, email, message.as_string())
        smtp.quit()

    # conf = ConnectionConfig(
    #     MAIL_USERNAME="sunanda shil",
    #     MAIL_PASSWORD=settings.PASSWORD,
    #     MAIL_FROM=settings.EMAIL,
    #     MAIL_PORT=587,
    #     MAIL_SERVER="smtp.gmail.com",
    #     MAIL_STARTTLS=False,
    #     MAIL_SSL_TLS=True,
    #     USE_CREDENTIALS=True,
    #     VALIDATE_CERTS=True
    # )
    # message = MessageSchema(
    #     subject="Welcome to our website!",
    #     recipients=[email],
    #     body=f"Thank you for registering on our website. We are excited to have you!\n{token}",
    #     subtype="html"
    # )
    # fm = FastMail(conf)
    # await fm.send_message(message)

