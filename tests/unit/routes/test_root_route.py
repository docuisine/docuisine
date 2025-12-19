from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from docuisine.dependencies.services import get_user_service
from docuisine.main import app


def test_read_root(client):
    ## Setup
    def mock_user_service():
        mock = MagicMock()
        return mock

    app.dependency_overrides[get_user_service] = lambda: mock_user_service
    client = TestClient(app)

    ## Test
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello, from Docuisine!"
