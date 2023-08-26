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


def test_create_note(client, register_and_login_user):
    note_data = {
        "title": "india",
        "description": "Delhi is a beautifull country",
        "reminder": "2023-08-12T14:46:08Z"
    }
    response = client.post("/create_note", json=note_data, headers={"token": register_and_login_user.get('token'),
                                                                    'content_type': 'application/json'})
    assert response.status_code == 201


def test_get_note(client, register_and_login_user):
    note_data = {
        "title": "india",
        "description": "Delhi is a beautifull country",
        "reminder": "2023-08-12T14:46:08Z"
    }
    response = client.post("/create_note", json=note_data, headers={"token": register_and_login_user.get('token'),
                                                                    'content_type': 'application/json'})
    assert response.status_code == 201

    get_response = client.get("/note", headers={"token": register_and_login_user.get('token'),
                                                'content_type': 'application/json'})
    assert get_response.status_code == 200


def test_update_note(client, register_and_login_user):
    note_data = {
        "title": "india",
        "description": "Delhi is a beautifull country",
        "reminder": "2023-08-12T14:46:08Z"
    }
    response = client.post("/create_note", json=note_data, headers={"token": register_and_login_user.get('token'),
                                                                    'content_type': 'application/json'})
    assert response.status_code == 201
    note_id = response.json().get('data', {}).get('id')

    updated_note_data = {
        "title": "india",
        "description": "isro mission",
        "reminder": "2023-08-12T14:46:08Z"
    }
    update_response = client.put(f"/update_note/{note_id}", json=updated_note_data, headers={
        "token": register_and_login_user.get('token'),
        'content_type': 'application/json'})

    assert update_response.status_code == 201


def test_delete_note(client, register_and_login_user):
    note_data = {
        "title": "india",
        "description": "Delhi is a beautifull country",
        "reminder": "2023-08-12T14:46:08Z"
    }
    response = client.post("/create_note", json=note_data, headers={"token": register_and_login_user.get('token'),
                                                                    'content_type': 'application/json'})
    assert response.status_code == 201
    note_id = response.json().get('data', {}).get('id')

    delete_data = client.delete(f"/delete_note/{note_id}", headers={"token": register_and_login_user.get('token'),
                                                                    'content_type': 'application/json'})
    assert delete_data.status_code == 200


def test_create_label(client, register_and_login_user):
    label_data = {
        "name": "jerry",
        "colour_field": "brown"
    }
    response = client.post("/create_labels", json=label_data, headers={"token": register_and_login_user.get('token'),
                                                                       'content_type': 'application/json'})
    assert response.status_code == 201


def test_get_label(client, register_and_login_user):
    label_data = {
        "name": "jerry",
        "colour_field": "brown"
    }
    response = client.post("/create_labels", json=label_data, headers={"token": register_and_login_user.get('token'),
                                                                       'content_type': 'application/json'})
    assert response.status_code == 201

    get_notes = client.get("/get_label", headers={"token": register_and_login_user.get('token'),
                                                  'content_type': 'application/json'})
    assert get_notes.status_code == 200


def test_update_label(client, register_and_login_user):
    label_data = {
        "name": "jerry",
        "colour_field": "brown"
    }
    response = client.post("/create_labels", json=label_data, headers={"token": register_and_login_user.get('token'),
                                                                       'content_type': 'application/json'})
    assert response.status_code == 201

    update_label_data = {
        "name": "Tom",
        "colour_field": "brown"
    }

    label_id = response.json().get('data', {}).get('id')
    update_response = client.put(f"/update_label/{label_id}", json=update_label_data, headers=
    {"token": register_and_login_user.get('token'),
     'content_type': 'application/json'})

    assert update_response.status_code == 201


def test_delete_label(client, register_and_login_user):
    label_data = {
        "name": "jerry",
        "colour_field": "brown"
    }
    response = client.post("/create_labels", json=label_data, headers={"token": register_and_login_user.get('token'),
                                                                       'content_type': 'application/json'})
    assert response.status_code == 201

    label_id = response.json().get('data', {}).get('id')
    delete_response = client.delete(f"/delete_label/{label_id}", headers={"token": register_and_login_user.get('token'),
                                                                          'content_type': 'application/json'})

    assert delete_response.status_code == 200
