from core.db import get_db
from .models import Note
from .schemas import NoteValidator
from settings import logger
from fastapi import APIRouter, Response, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from user.models import User
from .utils import get_token, Cache, add_reminder


note_router = APIRouter(dependencies=[Depends(get_token)])


@note_router.post("/create_note")
def create_note(request: Request, response: Response, data: NoteValidator, db: Session = Depends(get_db)):
    """
    This function is created for create the Note
    :param request: request parameter taken for use global variable and get_token which
    is dependency like request.state.user.id for getting user_id
    :param response: for getting the response
    :param data: inputted data in fields
    :param db: for creating session with database
    :return: message,status and created note data
    """
    try:
        note = Note(**data.model_dump(), user_id=request.state.user.id)

        db.add(note)
        db.commit()
        db.refresh(note)
        Cache.save(request.state.user.id, note.to_dict())
        add_reminder(note)
        return {"message": "successfully added note", "status": 201, "data": note.to_dict()}
    except Exception as e:
        logger.exception(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}


@note_router.get("/note")
def read_note(request: Request, response: Response, db: Session = Depends(get_db)):
    """
    This function is created for fetching the note
    :param request: request parameter taken for use global variable and get_token which
    is dependency like request.state.user.id for getting user_id
    :param response: for getting the response
    :param db: for creating session with database
    :return: message,status and fetched note data
    """
    try:
        cached_notes = Cache.get_notes(request.state.user.id)
        if cached_notes:
            return {"message": "successfully getting note from cached", "status": 200, "data": cached_notes}
        note = db.query(Note).filter_by(user_id=request.state.user.id, is_archive=False, is_trash=False).all()
        notes = [x.to_dict() for x in note]
        return {"message": "successfully getting note", "status": 200, "data": notes}
    except Exception as e:
        logger.exception(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}


@note_router.put("/update_note/{note_id}")
def update_note(request: Request, response: Response, updated_note: NoteValidator, note_id: int,
                user: User = Depends(get_token), db: Session = Depends(get_db)):
    """
    This function is created for update the note
    :param request: request parameter taken for use global variable and get_token which
    is dependency like request.state.user.id for getting user_id
    :param response: for getting the response
    :param updated_note: inputted  updated data in fields
    :param note_id: which note need to be updated
    :param user: instead use global variable it's another method for getting user_id from token
    :param db: for creating session with database
    :return: message,status and updated note data
    """
    try:
        note = db.query(Note).filter_by(id=note_id, user_id=user.id).first()
        if note is None:
            raise HTTPException(status_code=404, detail=" Note not found")
        [setattr(note, key, val) for key, val in updated_note.model_dump().items()]
        db.commit()
        db.refresh(note)
        Cache.save(request.state.user.id, note.to_dict())
        return {"message": "successfully updated note", "status": 201, "data": note}
    except Exception as e:
        logger.exception(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}


@note_router.delete("/delete_note/{note_id}")
def delete_note(request: Request,response: Response, note_id: int, user: User = Depends(get_token), db: Session = Depends(get_db)):
    """
    This function is created for delete the note
    :param request: request parameter taken for use global variable and get_token which
    is dependency like request.state.user.id for getting user_id
    :param response: for getting the response
    :param note_id: which note need to delete
    :param user: instead use global variable it's another method for getting user_id from token
    :param db: for creating session with database
    :return: message,status and deleted note data
    """
    try:
        Cache.delete_note(request.state.user.id, note_id)
        note = db.query(Note).filter_by(id=note_id, user_id=request.state.user.id).first()
        if note is None:
            raise HTTPException(status_code=404, detail=" Note not found")
        db.delete(note)
        db.commit()
        return {"message": "successfully deleted note", "status": 200, "data": note}
    except Exception as e:
        logger.exception(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}


@note_router.post("/archive/{note_id}")
def archive(request: Request, response: Response, note_id: int, db: Session = Depends(get_db)):
    """
    This function is created for archiving note with just making condition True and False
    :param request:  request parameter taken for use global variable and get_token which from their we will get user id
    :param response: for getting the response
    :param note_id: which note need to be archived
    :param db: for creating session with database
    :return: message,status and archived note data
    """
    try:
        note = db.query(Note).filter_by(id=note_id, user_id=request.state.user.id).first()
        note.is_archive = False if note.is_archive else True
        db.commit()
        db.refresh(note)
        Cache.save(request.state.user.id, note.to_dict())
        return {"message": "note is archieved", "status": 200, "data": note}
    except Exception as e:
        logger.exception(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}


@note_router.get("/get_archive")
def get_archive(request: Request, response: Response, db: Session = Depends(get_db)):
    try:
        note = db.query(Note).filter_by(user_id=request.state.user.id, is_archive=True)
        notes = [x.to_dict() for x in note]
        return {"message": "get the archive note", "status": 200, "data": notes}
    except Exception as e:
        logger.exception(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}


@note_router.post("/trash/{note_id}")
def trash(request: Request, response: Response, note_id: int, db: Session = Depends(get_db)):
    try:
        note = db.query(Note).filter_by(id=note_id, user_id=request.state.user.id).first()
        note.is_trash = False if note.is_trash else True
        db.commit()
        db.refresh(note)
        Cache.save(request.state.user.id, note.to_dict())
        return {"message": "note is trashed", "status": 200, "data": note}
    except Exception as e:
        logger.exception(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}


@note_router.get("/get_trash")
def get_trash(request: Request, response: Response, db: Session = Depends(get_db)):
    try:
        note = db.query(Note).filter_by(user_id=request.state.user.id, is_trash=True)
        notes = [x.to_dict() for x in note]
        return {"message": "get trashed note", "status": 200, "data": notes}
    except Exception as e:
        logger.exception(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}
