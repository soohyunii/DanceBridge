import pytest

from tests.conftest import auth_header


@pytest.fixture
def dance_class(client, dancer_profile):
    resp = client.post(
        "/classes", json={"dancer_id": dancer_profile["id"], "title": "Hiphop Basics"}
    )
    return resp.json()


def test_student_can_apply_to_class(client, student_token, student_profile, dance_class):
    resp = client.post(
        "/enrollments", json={"class_id": dance_class["id"]}, headers=auth_header(student_token)
    )
    assert resp.status_code == 201
    assert resp.json()["status"] == "pending"


def test_duplicate_application_rejected(client, student_token, student_profile, dance_class):
    headers = auth_header(student_token)
    client.post("/enrollments", json={"class_id": dance_class["id"]}, headers=headers)
    resp = client.post("/enrollments", json={"class_id": dance_class["id"]}, headers=headers)
    assert resp.status_code == 409


def test_apply_to_nonexistent_class_fails(client, student_token, student_profile):
    resp = client.post(
        "/enrollments", json={"class_id": 9999}, headers=auth_header(student_token)
    )
    assert resp.status_code == 404


def test_student_sees_only_own_enrollments(client, student_token, student_profile, dance_class):
    client.post(
        "/enrollments", json={"class_id": dance_class["id"]}, headers=auth_header(student_token)
    )
    resp = client.get("/enrollments", headers=auth_header(student_token))
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    assert resp.json()[0]["student_id"] == student_profile["id"]


def test_dancer_sees_applications_to_own_classes(
    client, dancer_token, student_token, student_profile, dance_class
):
    client.post(
        "/enrollments", json={"class_id": dance_class["id"]}, headers=auth_header(student_token)
    )
    resp = client.get("/enrollments", headers=auth_header(dancer_token))
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_student_cannot_approve_own_enrollment(
    client, student_token, student_profile, dance_class
):
    created = client.post(
        "/enrollments", json={"class_id": dance_class["id"]}, headers=auth_header(student_token)
    ).json()
    resp = client.patch(
        f"/enrollments/{created['id']}",
        json={"status": "approved"},
        headers=auth_header(student_token),
    )
    assert resp.status_code == 403


def test_dancer_can_approve_application_to_own_class(
    client, dancer_token, student_token, student_profile, dance_class
):
    created = client.post(
        "/enrollments", json={"class_id": dance_class["id"]}, headers=auth_header(student_token)
    ).json()
    resp = client.patch(
        f"/enrollments/{created['id']}",
        json={"status": "approved"},
        headers=auth_header(dancer_token),
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "approved"


def test_student_can_cancel_own_enrollment(
    client, student_token, student_profile, dance_class
):
    created = client.post(
        "/enrollments", json={"class_id": dance_class["id"]}, headers=auth_header(student_token)
    ).json()
    resp = client.patch(
        f"/enrollments/{created['id']}",
        json={"status": "cancelled"},
        headers=auth_header(student_token),
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "cancelled"
