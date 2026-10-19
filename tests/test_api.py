from fastapi.testclient import TestClient
from app.main import app

def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

def test_create_and_redirect_and_stats():
    with TestClient(app) as client:
        created = client.post("/api/urls", json={"url": "https://example.com/path"})
        assert created.status_code == 201
        body = created.json()
        code = body["code"]

        redirect = client.get(f"/{code}", follow_redirects=False)
        assert redirect.status_code == 307
        assert redirect.headers["location"] == "https://example.com/path"

        stats = client.get(f"/api/urls/{code}")
        assert stats.status_code == 200
        assert stats.json()["click_count"] == 1

def test_custom_alias_conflict():
    with TestClient(app) as client:
        first = client.post("/api/urls", json={"url": "https://example.com", "custom_alias": "my-link"})
        assert first.status_code == 201
        second = client.post("/api/urls", json={"url": "https://example.org", "custom_alias": "my-link"})
        assert second.status_code == 409

def test_invalid_url():
    with TestClient(app) as client:
        response = client.post("/api/urls", json={"url": "not-a-url"})
        assert response.status_code == 422
