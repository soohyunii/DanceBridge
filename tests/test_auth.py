def test_signup_creates_user(client):
    resp = client.post("/auth/signup", json={"email": "a@test.com", "password": "pass1234"})
    assert resp.status_code == 201
    assert resp.json()["email"] == "a@test.com"


def test_signup_duplicate_email_fails(client):
    client.post("/auth/signup", json={"email": "a@test.com", "password": "pass1234"})
    resp = client.post("/auth/signup", json={"email": "a@test.com", "password": "pass1234"})
    assert resp.status_code == 409


def test_login_wrong_password_fails(client):
    client.post("/auth/signup", json={"email": "a@test.com", "password": "pass1234"})
    resp = client.post(
        "/auth/login", json={"email": "a@test.com", "password": "wrong", "role": "dancer"}
    )
    assert resp.status_code == 401


def test_login_unknown_email_fails(client):
    resp = client.post(
        "/auth/login", json={"email": "nobody@test.com", "password": "pass1234", "role": "dancer"}
    )
    assert resp.status_code == 401


def test_same_account_can_login_with_either_role(client):
    client.post("/auth/signup", json={"email": "a@test.com", "password": "pass1234"})

    as_dancer = client.post(
        "/auth/login", json={"email": "a@test.com", "password": "pass1234", "role": "dancer"}
    )
    as_student = client.post(
        "/auth/login", json={"email": "a@test.com", "password": "pass1234", "role": "student"}
    )

    assert as_dancer.json()["role"] == "dancer"
    assert as_student.json()["role"] == "student"
