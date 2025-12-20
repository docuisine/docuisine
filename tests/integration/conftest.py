from fastapi.testclient import TestClient
import pytest
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from docuisine.db.models.base import Base
from docuisine.dependencies.db import get_db_session
from docuisine.main import app

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db_session] = get_test_db


@pytest.fixture()
def setup_and_teardown():
    """Setup and teardown the database for tests."""
    # NOTE: A faster way to setup and teardown the database
    # for tests is by using rollbacks, without committing changes.
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client():
    return TestClient(app)
