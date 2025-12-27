from unittest.mock import MagicMock

from fastapi.applications import AppType
from fastapi.testclient import TestClient
import pytest

from docuisine.db.models import User
from docuisine.dependencies.auth import get_client_user
from docuisine.main import app as fastapi_app
from docuisine.schemas.enums import Role


@pytest.fixture(scope="function")
def app():
    """
    Provide the FastAPI app for testing.
    Used in units test for routes by mocking the services with a test client.
    """
    yield fastapi_app
    fastapi_app.dependency_overrides.clear()


@pytest.fixture(scope="module")
def mock_user_service():
    """
    Provide a mock UserService.
    Used in units test for routes by mocking the services.
    """
    mock = MagicMock()
    return mock


@pytest.fixture
def db_session():
    """
    Provide a mock database session for testing.
    Used in unit tests for services by mocking the database session.
    """
    session = MagicMock()
    session.query.return_value = session
    session.filter_by.return_value = session
    session.delete.return_value = session
    session.commit.return_value = session
    session.add.return_value = session
    session.rollback.return_value = session
    return session


@pytest.fixture
def regular_user():
    """
    Provide a regular user instance for testing.
    Used in unit tests for services and routes that require a regular user.

    NOTES
    -----
    Do not use mock user with MagicMock. 
    This will break identity access checks in routes
    """
    return User(
        id=1,
        username="dev-user",
        password="hashed::DevPassword1P!",
        email="dev-user@docuisine.org",
        role=Role.USER,
    )


@pytest.fixture
def app_regular_user(app: AppType, regular_user: User):
    """
    Provide a FastAPI app with a regular authenticated user.
    Used in unit tests for routes that require an authenticated regular user.
    """
    app.dependency_overrides[get_client_user] = lambda: regular_user
    return app


@pytest.fixture
def admin_user():
    """
    Provide an admin user instance for testing.
    Used in unit tests for services and routes that require an admin user.

    NOTES
    -----
    Do not use mock user with MagicMock. 
    This will break identity access checks in routes
    """
    return User(
        id=2,
        username="dev-admin",
        password="hashed::DevPassword2P!",
        email="dev-admin@docuisine.org",
        role=Role.ADMIN,
    )


@pytest.fixture
def app_admin(app: AppType, admin_user: User):
    """
    Provide a FastAPI app with an admin authenticated user.
    Used in unit tests for routes that require an authenticated admin user.
    """
    app.dependency_overrides[get_client_user] = lambda: admin_user
    return app


@pytest.fixture
def public_client(app: AppType):
    """
    Provide a TestClient without any authenticated user.
    Used in unit tests for public routes that do not require authentication.
    """
    app.dependency_overrides[get_client_user] = lambda: None
    return TestClient(app)


@pytest.fixture
def admin_client(app_admin: AppType):
    """
    Provide a TestClient with an admin authenticated user.
    Used in unit tests for routes that require an authenticated admin user.
    """
    return TestClient(app_admin)


@pytest.fixture
def user_client(app_regular_user: AppType):
    """
    Provide a TestClient with a regular authenticated user.
    Used in unit tests for routes that require an authenticated regular user.
    """
    return TestClient(app_regular_user)


@pytest.fixture
def clients(
    public_client: TestClient,
    user_client: TestClient,
    admin_client: TestClient,
) -> dict[str, TestClient]:
    """
    Provide a dictionary of TestClients for different user roles.
    Used in unit tests for routes that require different levels of authentication.
    """
    return {
        "public": public_client,
        "user": user_client,
        "admin": admin_client,
    }
