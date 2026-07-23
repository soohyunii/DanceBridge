from tests.conftest import auth_header


def test_create_student_profile(client, student_token):
    resp = client.post(
        "/students", json={"name": "Student A"}, headers=auth_header(student_token)
    )
    assert resp.status_code == 201
    assert resp.json()["name"] == "Student A"


def test_cannot_create_duplicate_student_profile(client, student_token):
    client.post("/students", json={"name": "Student A"}, headers=auth_header(student_token))
    resp = client.post("/students", json={"name": "Student B"}, headers=auth_header(student_token))
    assert resp.status_code == 409


def test_dancer_role_cannot_create_student_profile(client, dancer_token):
    resp = client.post("/students", json={"name": "x"}, headers=auth_header(dancer_token))
    assert resp.status_code == 403


def test_get_nonexistent_student_returns_404(client):
    resp = client.get("/students/9999")
    assert resp.status_code == 404
