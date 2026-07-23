import os

os.environ["DANCEBRIDGE_DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app


@pytest.fixture(autouse=True)
def _fresh_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


def auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def signup_and_login(client, email: str, password: str, role: str) -> str:
    client.post("/auth/signup", json={"email": email, "password": password})
    resp = client.post("/auth/login", json={"email": email, "password": password, "role": role})
    return resp.json()["access_token"]


@pytest.fixture
def dancer_token(client):
    return signup_and_login(client, "dancer@test.com", "pass1234", "dancer")


@pytest.fixture
def student_token(client):
    return signup_and_login(client, "student@test.com", "pass1234", "student")


@pytest.fixture
def dancer_profile(client, dancer_token):
    resp = client.post(
        "/dancers", json={"name": "Test Dancer"}, headers=auth_header(dancer_token)
    )
    return resp.json()


@pytest.fixture
def student_profile(client, student_token):
    resp = client.post(
        "/students", json={"name": "Test Student"}, headers=auth_header(student_token)
    )
    return resp.json()
