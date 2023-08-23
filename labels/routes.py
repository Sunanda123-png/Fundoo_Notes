from fastapi import APIRouter, Depends, Request, Response
from .schemas import LabelsValidator
from note.utils import get_token
from core.db import get_db
from sqlalchemy.orm import Session
from psycopg2 import connect

connection = connect('dbname=fundoo_notes user=postgres')
cursor = connection.cursor()
label_router = APIRouter(dependencies=[Depends(get_token)])


@label_router.post("/create_labels")
def create_labels(request: Request, data: LabelsValidator):
    """
    This function is created for creating label
    :param request: request parameter taken for use global variable and get_token which from their we will get user id
    :param data: inputted data in fields for creating label
    :return: message,status and label data
    """
    query = "INSERT INTO labels (name, colour_field, user_id) VALUES (%s, %s, %s)"
    query_lst = [data.name, data.colour_field, request.state.user.id]
    cursor.execute(query, query_lst)
    connection.commit()

    # fetch the data from data base
    select_query = "SELECT * FROM labels ORDER BY id DESC fetch first row only"
    cursor.execute(select_query)
    columns = [row[0] for row in cursor.description]
    labels = dict(zip(columns, cursor.fetchone()))
    return {"message": "Successfully created labels", "status": 201, "data": labels}


@label_router.get("/get_label")
def fetching_labels(request: Request):
    """
    This function is created for fetching label
    :param request: request parameter taken for use global variable and get_token which from their we will get user id
    :return: message,status and label data
    """
    cursor.execute('SELECT * FROM Labels WHERE user_id=%s', [request.state.user.id])
    columns = [row[0] for row in cursor.description]
    labels = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return {"message": "Successfully fetched labels", "status": 200, "data": labels}


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

    query = "UPDATE labels SET name = %s, colour_field = %s, user_id = %s WHERE id = %s"
    query_params = [updated_label.name, updated_label.colour_field, request.state.user.id, label_id]
    cursor.execute(query, query_params)
    connection.commit()

    # fetch the updated value
    select_query = "SELECT * FROM labels WHERE id=%s"
    cursor.execute(select_query, [label_id])
    columns = [row[0] for row in cursor.description]
    labels = dict(zip(columns, cursor.fetchone()))
    return {"message": "successfully updated label", "status": 201, "data": labels}


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
    query = "DELETE FROM labels  WHERE id = %s AND user_id = %s"
    query_params = [label_id, request.state.user.id]
    cursor.execute(query, query_params)
    connection.commit()
    return {"message": "successfully deleted label", "status": 200}
