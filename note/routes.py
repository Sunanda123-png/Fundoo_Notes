from core.db import get_db
from .models import Note
from .schemas import NoteValidator
from settings import logger
from fastapi import APIRouter, Response, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from user.models import User
from .utils import get_token

note_router = APIRouter(dependencies=[Depends(get_token)])


@note_router.post("/create_note")
def create_note(request: Request, response: Response, data: NoteValidator, db: Session = Depends(get_db)):
    try:

        note = Note(**data.model_dump(), user_id=request.state.user.id)
        db.add(note)
        db.commit()
        db.refresh(note)
        return {"message": "successfully added note", "status": 201, "data": note}
    except Exception as e:
        logger.exception(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}


# @note_router.get("/notes")
# def read_notes(response: Response, db: Session = Depends(get_db)):
#     try:
#         notes = db.query(Note).all()
#         return {"message": "successfully get the all notes", "status": 200, "data": notes}
#     except Exception as e:
#         logger.exception(e)
#         response.status_code = status.HTTP_400_BAD_REQUEST
#         return {"message": str(e)}


@note_router.get("/note")
def read_note(request: Request, response: Response, db: Session = Depends(get_db)):
    try:
        note = db.query(Note).filter_by(user_id=request.state.user.id).all()
        notes = [x.to_dict() for x in note]
        return {"message": "successfully getting note", "status": 200, "data": notes}
    except Exception as e:
        logger.exception(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}


@note_router.put("/update_note/{note_id}")
def update_note(response: Response, updated_note: NoteValidator, note_id: int, user: User = Depends(get_token),
                db: Session = Depends(get_db)):
    try:
        note = db.query(Note).filter_by(id=note_id, user_id=user.id).first()
        if note is None:
            raise HTTPException(status_code=404, detail=" Note not found")
        [setattr(note, key, val) for key, val in updated_note.model_dump().items()]
        db.commit()
        db.refresh(note)
        return {"message": "successfully updated note", "status": 201, "data": note}
    except Exception as e:
        logger.exception(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}


@note_router.delete("/delete_note/{note_id}")
def delete_note(response: Response, note_id: int, user: User = Depends(get_token), db: Session = Depends(get_db)):
    try:
        note = db.query(Note).filter_by(id=note_id, user_id=user.id).first()
        if note is None:
            raise HTTPException(status_code=404, detail=" Note not found")
        db.delete(note)
        db.commit()
        return {"message": "successfully deleted note", "status": 200, "data": note}
    except Exception as e:
        logger.exception(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}
