from tests.conftest import auth_header


def test_create_dancer_profile(client, dancer_token):
    resp = client.post(
        "/dancers", json={"name": "Dancer A", "bio": "hi"}, headers=auth_header(dancer_token)
    )
    assert resp.status_code == 201
    assert resp.json()["name"] == "Dancer A"


def test_cannot_create_duplicate_dancer_profile(client, dancer_token):
    client.post("/dancers", json={"name": "Dancer A"}, headers=auth_header(dancer_token))
    resp = client.post("/dancers", json={"name": "Dancer B"}, headers=auth_header(dancer_token))
    assert resp.status_code == 409


def test_student_role_cannot_create_dancer_profile(client, student_token):
    resp = client.post("/dancers", json={"name": "x"}, headers=auth_header(student_token))
    assert resp.status_code == 403


def test_create_dancer_requires_auth(client):
    resp = client.post("/dancers", json={"name": "x"})
    assert resp.status_code == 401


def test_get_nonexistent_dancer_returns_404(client):
    resp = client.get("/dancers/9999")
    assert resp.status_code == 404
