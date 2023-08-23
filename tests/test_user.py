import pytest
from sqlalchemy import false


def test_register_user_successfully(client):
    user_data = {
        "username": "goy",
        "firstname": "string",
        "lastname": "string",
        "password": "stringii",
        "email": "ssunanda02@gmail.com",
        "phone": 0,
        "location": "string"
    }
    response = client.post('/register_user', json=user_data)
    print(response.content)
    assert response.status_code == 201


def test_login(client):
    user_data = {
        "username": "goy",
        "firstname": "string",
        "lastname": "string",
        "password": "stringii",
        "email": "ssunanda02@gmail.com",
        "phone": 0,
        "location": "string"
    }
    response = client.post('/register_user', json=user_data)
    assert response.status_code == 201
    login_data = {
        "username": "goy",
        "password": "stringii"
    }
    response = client.post('/login_user', json=login_data)
    assert response.status_code == 200



@pytest.mark.abc
def test_create_note(client, register_and_login_user):

    note_data = {
        "title": "india",
        "description": "Delhi is a beautifull country",
        "is_archive": false,
        "is_trash": false,
        "reminder": "2023-08-12T14:46:08Z"
    }
    response = client.post("/create_note", json=note_data, headers={"token": register_and_login_user.get('token')})
    assert response.status_code == 201
