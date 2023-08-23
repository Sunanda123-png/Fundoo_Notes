from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
from core.db import get_db
from .schemas import UserValidator, LoginUser, ForgetPassword, ResetPassword
from sqlalchemy.orm import Session
from .models import User, pwd_context
from settings import logger, settings
from .utils import create_access_token, decode_access_token
from tasks import send_notification
from note.utils import CustomException

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
    user = db.query(User).filter(User.username == login.username).first()
    if not user:
        raise CustomException(message="Invalid Credential", status_code=400)
    if not pwd_context.verify(login.password, user.password) and user.is_verified:
        raise CustomException(message="Invalid Credential", status_code=400)
    token = create_access_token(data={"user": user.id})
    return {"message": "Login successful", "token": token, "status": 200}


@router.get("/verify")
def verify(response: Response, token: str, payload: dict = Depends(decode_access_token),
           db: Session = Depends(get_db)):
    user_id = payload.get('user')
    if not user_id:
        raise CustomException(message="Invalid user", status_code=404)
    user_details = db.query(User).filter_by(id=user_id).first()
    user_details.is_verified = True
    db.commit()
    return {"message": "User verification is successful", "status": 200}


@router.post("/forget_password")
def forget_password(data: ForgetPassword, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=data.username, email=data.email).first()
    if not user:
        raise CustomException(message="User not found", status_code=404)
    token = f"{settings.BASE_URL}/reset_password?token={create_access_token({'user': user.id})}"
    send_notification.delay(user.email, token, "reset password")
    return {"message": "Reset link sent to mail", "status": 200}


@router.post("/reset_password")
def reset_password(token: str, data: ResetPassword, payload: dict = Depends(decode_access_token),
                   db: Session = Depends(get_db)):
    if data.password != data.confirm_password:
        raise CustomException(message="Password mismatched", status_code=400)
    user = db.query(User).filter_by(id=payload.get('user')).first()
    if not user:
        raise CustomException(message="User not found", status_code=404)
    user.password = user.set_password(data.password)
    db.commit()
    return {"message": "Password set successfully", "status": 200}
