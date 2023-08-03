from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
from core.db import get_db
from .schemas import UserValidator, LoginUser
from sqlalchemy.orm import Session
from .models import User, pwd_context
from settings import logger

router = APIRouter()


@router.post("/register_user", status_code=status.HTTP_201_CREATED)
def register_user(response: Response, data: UserValidator, db: Session = Depends(get_db)):
    try:
        user = User(**data.model_dump())
        user.set_password(user.password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        logger.exception(str(e))
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}


@router.post("/login_user", status_code=status.HTTP_200_OK)
def login_user(login: LoginUser, db: Session = Depends(get_db)):
    user_in_db = db.query(User).filter(User.username == login.username).first()
    if not user_in_db or not pwd_context.verify(login.password, user_in_db.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    return {"message": "Login successful"}
