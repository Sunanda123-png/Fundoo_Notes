from fastapi import APIRouter, Depends, Request, Response, status, HTTPException, BackgroundTasks
from core.db import get_db
from .schemas import UserValidator, LoginUser
from sqlalchemy.orm import Session
from .models import User, pwd_context
from settings import logger,settings
from .utils import create_access_token, decode_access_token, send_mail
from fastapi_mail import MessageSchema
from tasks import send_notification
router = APIRouter()


@router.post("/register_user", status_code=status.HTTP_201_CREATED)
def register_user(response: Response, data: UserValidator, db: Session = Depends(get_db)):
    """
    This function is created for registering the user
    :param response: For getting response with status code
    :param data: validated user data from schemas
    :param db: session will create for adding the data in db
    :return: user metadata
    """
    try:
        user = User(**data.model_dump())
        user.set_password(user.password)
        db.add(user)
        db.commit()
        db.refresh(user)
        token = f"{settings.BASE_URL}/verify?token={create_access_token({'user': user.id})}"
        send_notification.delay(user.email, token, "user registration")
        return {"message": "Registration successful. Welcome message send", "status": 201, "data": user}
    except Exception as e:
        logger.exception(str(e))
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}


@router.post("/login_user", status_code=status.HTTP_200_OK)
def login_user(response: Response, login: LoginUser, db: Session = Depends(get_db)):
    """
    This function is created for loging the user
    :param response: For getting response with status code
    :param login: it contain the username and password
    :param db: for session creation for checking data is present in db or not
    :return: message and generated token
    """
    try:
        user = db.query(User).filter(User.username == login.username).first()
        if not user and not pwd_context.verify(login.password, user.password) and user.is_verified:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
        token = create_access_token(data={"user": user.id})
        return {"message": "Login successful", "token": token, "status": 200}
    except Exception as e:
        logger.exception(str(e))
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}


@router.get("/verify")
def verify(response: Response, token: str, payload: dict = Depends(decode_access_token),
           db: Session = Depends(get_db)):
    try:
        user_id = payload.get('user')
        if not user_id:
            raise Exception("Invalid user")
        user_details = db.query(User).filter_by(id=user_id).first()
        user_details.is_verified = True
        db.commit()
        return {"message":"User verification is successful", "status": 200}
    except Exception as e:
        logger.exception(str(e))
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}




