from user.utils import decode_access_token
from fastapi import HTTPException, Request, Depends
from sqlalchemy.orm import Session
from core.db import get_db
from user.models import User


def get_token(request: Request, db: Session = Depends(get_db)):
    try:
        token = request.headers.get('token')
        if not token:
            raise HTTPException(status_code=404, detail="Token not found")
        payload = decode_access_token(token)
        user = db.query(User).filter_by(id=payload.get('user')).first()
        if user is None:
            raise HTTPException(status_code=404, detail="user is not in db")
        # return user
        request.state.user = user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
