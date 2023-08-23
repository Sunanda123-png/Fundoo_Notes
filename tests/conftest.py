import json

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from core.db import Base, get_db
from settings import settings
from main import app

engine = create_engine(settings.TEST_DATABASE_URL)
testing_session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base.metadata.create_all(bind=engine)


@pytest.fixture()
def override_get_db():
    Base.metadata.create_all(bind=engine)
    db = testing_session()
    try:
        yield db
    finally:
        Base.metadata.drop_all(bind=engine)
        db.close()


@pytest.fixture()
def client(override_get_db):
    def override_db():
        try:
            yield override_get_db
        finally:
            override_get_db.close()

    app.dependency_overrides[get_db] = override_db
    yield TestClient(app)

@pytest.fixture()
def register_and_login_user(client):
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
    login_data = {
        "username": "goy",
        "password": "stringii"
    }
    response = client.post('/login_user', json=login_data)
    return json.loads(response.content)


