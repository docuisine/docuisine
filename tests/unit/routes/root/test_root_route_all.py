from fastapi import status
from fastapi.testclient import TestClient
import pytest


class TestGET:
    @pytest.mark.parametrize(
        "client_name, expected_status",
        [
            ("public", status.HTTP_200_OK),
            ("user", status.HTTP_200_OK),
            ("admin", status.HTTP_200_OK),
        ],
    )
    def test_root_route(
        self, client_name: str, expected_status: int, clients: dict[str, TestClient]
    ):
        """Test the public root route returns status 200 and correct message."""
        response = clients[client_name].get("/")
        assert response.status_code == expected_status, response.text
        assert response.json() == "Hello, from Docuisine!"
