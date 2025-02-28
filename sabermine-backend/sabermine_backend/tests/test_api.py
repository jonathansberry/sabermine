from fastapi.testclient import TestClient
from sabermine_backend.api import app
from io import BytesIO

client = TestClient(app)


class TestAPI():

    def test_cors_blocked_origin(self):
        response = client.get("/api/", headers={
            "Origin": "http://blocked.com",
        })
        assert response.status_code == 200
        assert not response.headers.get("access-control-allow-origin")

    def test_cors_allowed_origin(self):
        response = client.get("/api/", headers={
            "Origin": "http://localhost:3000"
        })
        assert response.status_code == 200
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


class TestReady():

    def test_ready(self):
        response = client.get("/api/")
        assert response.status_code == 200
        assert response.json() == {"message": "Sabermine api ready"}


class TestShortenURL():

    def test_shorten_url(self, dynamodb_mock):
        response = client.post("/api/shorten_url", json={"url": "https://example.com"})
        assert response.status_code == 200
        assert "short_url" in response.json()

    def test_shorten_url_invalid(self, dynamodb_mock):
        response = client.post("/api/shorten_url", json={"url": "invalid-url"})
        assert response.status_code == 422  # Unprocessable Entity


class TestRedirect():

    def test_redirect(self, dynamodb_mock):
        item = {"short_code": "abc123", "original_url": "https://example.com"}
        dynamodb_mock.put_item(Item=item)
        response = client.get(f"/{item["short_code"]}", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == item["original_url"]

    def test_redirect_not_found(self, dynamodb_mock):
        response = client.get("/nonexistent")
        assert response.status_code == 404
        assert response.json() == {"detail": "Short code not found"}


class TestUpload():

    def test_upload_file(self, dynamodb_mock, s3_mock):
        file_data = BytesIO(b"Hello, this is a test file!")
        response = client.post(
            "/api/upload",
            files={"file": ("test.txt", file_data, "text/plain")}
        )
        assert response.status_code == 200
        assert "short_url" in response.json()
