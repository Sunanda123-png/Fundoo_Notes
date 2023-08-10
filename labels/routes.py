from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
from .models import Labels
from .schemas import LabelsValidator
from note.utils import get_token
from core.db import get_db
from sqlalchemy.orm import Session
from settings import logger

label_router = APIRouter(dependencies=[Depends(get_token)])


@label_router.post("/create_labels")
def create_labels(request: Request, response: Response, data: LabelsValidator, db: Session = Depends(get_db)):
    """
    This function is created for creating label
    :param request: request parameter taken for use global variable and get_token which from their we will get user id
    :param response: for getting the response
    :param data: inputted data in fields for creating label
    :param db: for creating session with database
    :return: message,status and label data
    """
    try:
        label = Labels(**data.model_dump(), user_id=request.state.user.id)
        db.add(label)
        db.commit()
        db.refresh(label)
        return {"message": "Successfully created labels", "status": 201, "data": label}
    except Exception as e:
        logger.exception(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}


@label_router.get("/get_label")
def fetching_labels(request: Request, response: Response, db: Session = Depends(get_db)):
    """
    This function is created for fetching label
    :param request: request parameter taken for use global variable and get_token which from their we will get user id
    :param response: for getting the response
    :param db: for creating session with database
    :return: message,status and label data
    """
    try:
        label = db.query(Labels).filter_by(user_id=request.state.user.id).all()
        labels = [x.to_dict() for x in label]
        return {"message": "Successfully fetched labels", "status": 200, "data": labels}
    except Exception as e:
        logger.exception(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}


@label_router.put("/update_label/{label_id}")
def update_label(request: Request, response: Response, label_id: int, updated_label: LabelsValidator,
                 db: Session = Depends(get_db)):
    """
    This function is created for update the label
    :param request: request parameter taken for use global variable and get_token which from their we will get user id
    :param response: for getting the response
    :param label_id: which label need to update
    :param updated_label: inputted updated data in fields for update label
    :param db: for creating session with database
    :return: message,status and updated label data
    """
    try:
        label = db.query(Labels).filter_by(id=label_id, user_id=request.state.user.id).first()
        if label is None:
            raise HTTPException(status_code=404, detail=" label not found")
        [setattr(label, key, val) for key, val in updated_label.model_dump().items()]
        db.commit()
        db.refresh(label)
        return {"message": "successfully updated label", "status": 201, "data": label}
    except Exception as e:
        logger.exception(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}


@label_router.delete("/delete_label/{label_id}")
def delete_label(request: Request, response: Response, label_id: int, db: Session = Depends(get_db)):
    """
    this function is created for delete the label
    :param request: request parameter taken for use global variable and get_token which from their we will get user id
    :param response: for getting the response
    :param label_id: which label need to be deleted
    :param db: for creating session with database
    :return: message,status and data
    """
    try:
        label = db.query(Labels).filter_by(id=label_id, user_id=request.state.user.id).first()
        db.delete(label)
        db.commit()
        return {"message": "successfully deleted label", "status": 200, "data": label}
    except Exception as e:
        logger.exception(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}
