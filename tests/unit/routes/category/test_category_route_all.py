from unittest.mock import MagicMock

from fastapi.testclient import TestClient
import pytest

from docuisine.db.models import Category
from docuisine.dependencies.auth import get_client_user
from docuisine.dependencies.services import get_category_service
from docuisine.main import app
from docuisine.utils import errors

from . import params as p


@pytest.mark.parametrize(
    "scenario, client_name, expected_status, expected_response", p.GET_PARAMETERS
)
class TestGET:
    def test_get_categories(
        self,
        scenario: str,
        client_name: str,
        expected_status: int,
        expected_response: dict,
        clients: dict[str, TestClient],
    ):
        """Test getting categories."""

        def mock_category_service():
            mock = MagicMock()
            match scenario:
                case "get_all":
                    mock.get_all_categories.return_value = [
                        Category(**cat) for cat in p.GET_ALL_CATEGORIES_RESPONSE
                    ]
                case "get_by_id":
                    mock.get_category.return_value = Category(**p.GET_BY_ID_RESPONSE)
                case "get_not_found":
                    mock.get_category.side_effect = errors.CategoryNotFoundError(category_id=999)
            return mock

        client = clients[client_name]
        client.app.dependency_overrides[get_category_service] = mock_category_service  # type: ignore

        match scenario:
            case "get_all":
                response = client.get("/categories/")
            case "get_by_id":
                response = client.get("/categories/1")
            case "get_not_found":
                response = client.get("/categories/999")
        assert response.status_code == expected_status, response.text
        assert response.json() == expected_response


@pytest.mark.parametrize(
    "scenario, client_name, expected_status, expected_response", p.POST_PARAMETERS
)
class TestPOST:
    def test_create_category(
        self,
        scenario: str,
        client_name: str,
        expected_status: int,
        expected_response: dict,
        admin_user,
        public_user,
        regular_user,
    ):
        """Test creating a category (success or conflict)."""

        ## Setup
        mock_service = MagicMock()

        def mock_category_service():
            match scenario:
                case "success" | "success_no_description":
                    mock_service.create_category.return_value = Category(**expected_response)
                case "conflict":
                    mock_service.create_category.side_effect = errors.CategoryExistsError(
                        name="Dessert"
                    )
                case _:
                    pass
            return mock_service

        match client_name:
            case "admin":
                app.dependency_overrides[get_client_user] = lambda: admin_user
                client = TestClient(app)
            case "user":
                app.dependency_overrides[get_client_user] = lambda: regular_user
                client = TestClient(app)
            case "public":
                app.dependency_overrides[get_client_user] = lambda: public_user
                client = TestClient(app)
        client.app.dependency_overrides[get_category_service] = mock_category_service  # type: ignore

        ## Test
        match scenario:
            case "success":
                response = client.post(
                    "/categories/",
                    data={"name": "Mexican", "description": "Mexican cuisine"},
                )
            case "success_no_description":
                response = client.post("/categories/", data={"name": "Vegan"})
            case "conflict":
                response = client.post(
                    "/categories/",
                    data={"name": "Dessert", "description": "Sweet dishes"},
                )
            case "unauthorized":
                ## NOTE: This is a temp fix, This validation error should not happen.
                ## The mock service is leaking past the identity access check.
                response = client.post(
                    "/categories/",
                    data={"name": "Unauthorized", "description": "Should not work"},
                )
                assert mock_service.create_category.call_count == 0
        assert response.status_code == expected_status, response.text
        assert response.json() == expected_response
