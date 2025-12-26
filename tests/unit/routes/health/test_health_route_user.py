from fastapi import status
from fastapi.applications import AppType
from fastapi.testclient import TestClient


class TestGET:
    def test_health_route_user(self, app_regular_user: AppType):
        """Test the public health route with regular user authentication returns status 200 and correct message."""
        client = TestClient(app_regular_user)
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK, response.text
        data = response.json()
        assert data["status"] == "healthy"
        assert "commit_hash" in data
        assert "version" in data
