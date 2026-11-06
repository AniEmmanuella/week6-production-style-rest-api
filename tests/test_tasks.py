def create_sample(client, headers, **overrides):
    payload = {
        "title": "Prepare project report",
        "description": "Write the Week 6 project report",
        "status": "pending",
        "priority": "high",
    }
    payload.update(overrides)
    return client.post("/api/v1/tasks/", json=payload, headers=headers)


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_read_task(client, auth_headers):
    created = create_sample(client, auth_headers)
    assert created.status_code == 201
    task_id = created.json()["id"]

    fetched = client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert fetched.status_code == 200
    assert fetched.json()["title"] == "Prepare project report"


def test_validation_rejects_invalid_priority(client, auth_headers):
    response = create_sample(client, auth_headers, priority="urgent")
    assert response.status_code == 422


def test_authentication_is_required(client):
    response = client.get("/api/v1/tasks/")
    assert response.status_code == 401


def test_invalid_token_is_rejected(client):
    response = client.get("/api/v1/tasks/", headers={"Authorization": "Bearer wrong"})
    assert response.status_code == 401


def test_update_task(client, auth_headers):
    created = create_sample(client, auth_headers)
    task_id = created.json()["id"]
    response = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"status": "completed"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_delete_task(client, auth_headers):
    created = create_sample(client, auth_headers)
    task_id = created.json()["id"]
    deleted = client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert deleted.status_code == 204
    missing = client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert missing.status_code == 404


def test_pagination_and_filtering(client, auth_headers):
    create_sample(client, auth_headers, title="Buy groceries", priority="low")
    create_sample(client, auth_headers, title="Finish API", priority="high")
    create_sample(client, auth_headers, title="Review notes", priority="high")

    page = client.get("/api/v1/tasks/?limit=1&offset=0", headers=auth_headers)
    assert page.status_code == 200
    assert len(page.json()["items"]) == 1
    assert page.json()["total"] == 3

    filtered = client.get(
        "/api/v1/tasks/?priority=high&search=API",
        headers=auth_headers,
    )
    assert filtered.status_code == 200
    assert filtered.json()["total"] == 1
    assert filtered.json()["items"][0]["title"] == "Finish API"


def test_missing_task_returns_404(client, auth_headers):
    response = client.get("/api/v1/tasks/9999", headers=auth_headers)
    assert response.status_code == 404
