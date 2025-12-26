from fastapi import status
from fastapi.applications import AppType
from fastapi.testclient import TestClient


class TestGET:
    def test_health_route_admin(self, app_admin: AppType):
        """Test the public health route with admin user authentication returns status 200 and correct message."""
        client = TestClient(app_admin)
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK, response.text
        data = response.json()
        assert data["status"] == "healthy"
        assert "commit_hash" in data
        assert "version" in data
