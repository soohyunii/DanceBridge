from tests.conftest import auth_header, signup_and_login

VALID_URL = "https://www.instagram.com/reel/Cabc123XYZ/"


def test_create_video_requires_dancer_profile_first(client, dancer_token):
    resp = client.post(
        "/videos", json={"instagram_url": VALID_URL}, headers=auth_header(dancer_token)
    )
    assert resp.status_code == 400


def test_dancer_can_register_own_video(client, dancer_token, dancer_profile):
    resp = client.post(
        "/videos", json={"instagram_url": VALID_URL}, headers=auth_header(dancer_token)
    )
    assert resp.status_code == 201
    assert resp.json()["dancer_id"] == dancer_profile["id"]


def test_invalid_url_rejected(client, dancer_token, dancer_profile):
    resp = client.post(
        "/videos",
        json={"instagram_url": "https://youtube.com/watch?v=abc"},
        headers=auth_header(dancer_token),
    )
    assert resp.status_code == 422


def test_student_cannot_register_video(client, student_token, student_profile):
    resp = client.post(
        "/videos", json={"instagram_url": VALID_URL}, headers=auth_header(student_token)
    )
    assert resp.status_code == 403


def test_unauthenticated_cannot_register_video(client):
    resp = client.post("/videos", json={"instagram_url": VALID_URL})
    assert resp.status_code == 401


def test_dancer_cannot_delete_another_dancers_video(client, dancer_token, dancer_profile):
    created = client.post(
        "/videos", json={"instagram_url": VALID_URL}, headers=auth_header(dancer_token)
    ).json()

    other_token = signup_and_login(client, "other-dancer@test.com", "pass1234", "dancer")
    client.post("/dancers", json={"name": "Other Dancer"}, headers=auth_header(other_token))

    resp = client.delete(f"/videos/{created['id']}", headers=auth_header(other_token))
    assert resp.status_code == 403


def test_delete_own_video_succeeds(client, dancer_token, dancer_profile):
    created = client.post(
        "/videos", json={"instagram_url": VALID_URL}, headers=auth_header(dancer_token)
    ).json()
    resp = client.delete(f"/videos/{created['id']}", headers=auth_header(dancer_token))
    assert resp.status_code == 204
