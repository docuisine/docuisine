from unittest.mock import MagicMock

from fastapi.testclient import TestClient
import pytest

from docuisine.dependencies.services import get_user_service
from docuisine.main import app


@pytest.fixture(scope="module")
def mock_user_service():
    mock = MagicMock()
    return mock


@pytest.fixture(scope="module")
def client(mock_user_service):
    app.dependency_overrides[get_user_service] = lambda: mock_user_service
    yield TestClient(app)
    app.dependency_overrides.clear()
