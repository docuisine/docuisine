from typing import Callable
from unittest.mock import MagicMock

from fastapi import status
from fastapi.testclient import TestClient
import pytest

from docuisine.db.models import User
from docuisine.dependencies.services import get_user_service
from docuisine.schemas.enums import Role
from docuisine.utils import errors


class TestGET:
    @pytest.mark.parametrize(
        "scenario, client_name, expected_status, expected_response",
        [
            ("existing_root_user", "public", status.HTTP_200_OK, True),
            ("no_existing_root_user", "user", status.HTTP_200_OK, False),
            ("no_existing_root_user", "admin", status.HTTP_200_OK, False),
        ],
    )
    def test_root_route(
        self,
        scenario: str,
        client_name: str,
        expected_status: int,
        expected_response: bool,
        create_client: Callable[[str], TestClient],
    ):
        """Test the public root route returns status 200 and correct message."""

        def mock_user_service():
            mock = MagicMock()
            if scenario == "existing_root_user":
                mock.get_user.return_value = User(
                    id=1, username="root", email="root@root.com", role=Role.ADMIN
                )
            elif scenario == "no_existing_root_user":
                mock.get_user.side_effect = errors.UserNotFoundError()
            return mock

        client = create_client(client_name)
        client.app.dependency_overrides[get_user_service] = mock_user_service  # type: ignore

        response = client.get("/init/existing-root-user")
        assert response.status_code == expected_status, response.text
        assert response.json() is expected_response


class TestPOST:

    @pytest.mark.parametrize(
        "scenario, client_name, expected_status",
        [
            ("create_first_user_success", "public", status.HTTP_200_OK),
            ("create_first_user_already_exists", "public", status.HTTP_403_FORBIDDEN),
            ("create_first_user_already_exists", "user", status.HTTP_403_FORBIDDEN),
            ("create_first_user_already_exists", "admin", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_create_first_user(self, scenario: str, client_name: str, expected_status: int, create_client: Callable[[str], TestClient]):
        """Test creating the first user returns status 200 and correct response."""
        client = create_client(client_name)

        # Mock the user service to simulate no existing root user
        def mock_user_service():
            mock = MagicMock()
            if scenario == "create_first_user_already_exists":
                mock.get_user.return_value = User(
                    id=1, username="root", email="root@root.com", role=Role.ADMIN
                )
            else:
                mock.get_user.side_effect = errors.UserNotFoundError(user_id=1)
                mock.create_user.return_value = User(
                    id=1, username="root", email="root@root.com", role=Role.ADMIN
                )
            return mock

        client.app.dependency_overrides[get_user_service] = mock_user_service  # type: ignore

        response = client.post(
            "/init/create-first-user",
            json={
                "username": "root",
                "password": "!Password1",
                "email": "root@root.com",
            },
        )
        assert response.status_code == expected_status, response.text
        if expected_status == status.HTTP_200_OK:
            data = response.json()
            assert data["username"] == "root"
            assert data["email"] == "root@root.com"