def test_create_class_for_existing_dancer(client, dancer_profile):
    resp = client.post(
        "/classes",
        json={"dancer_id": dancer_profile["id"], "title": "Waacking Basics", "genre": "waacking"},
    )
    assert resp.status_code == 201
    assert resp.json()["dancer_id"] == dancer_profile["id"]


def test_create_class_for_nonexistent_dancer_fails(client):
    resp = client.post("/classes", json={"dancer_id": 9999, "title": "Ghost Class"})
    assert resp.status_code == 404


def test_list_classes_filtered_by_genre(client, dancer_profile):
    dancer_id = dancer_profile["id"]
    client.post("/classes", json={"dancer_id": dancer_id, "title": "A", "genre": "waacking"})
    client.post("/classes", json={"dancer_id": dancer_id, "title": "B", "genre": "hiphop"})

    resp = client.get("/classes", params={"genre": "waacking"})
    assert resp.status_code == 200
    results = resp.json()
    assert len(results) == 1
    assert results[0]["genre"] == "waacking"


def test_get_nonexistent_class_returns_404(client):
    resp = client.get("/classes/9999")
    assert resp.status_code == 404
