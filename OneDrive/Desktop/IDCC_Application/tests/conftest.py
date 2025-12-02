"""
Pytest configuration and fixtures.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.core.database import Base, get_db
from app.main import app
from app.models.requirement import Priority
from app.schemas.requirement import RequirementCreate


# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a test database session."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client."""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_requirement_data():
    """Sample requirement data for testing."""
    return {
        "project_name": "Test Project",
        "business_owner": "John Doe",
        "business_unit": "Engineering",
        "title": "Test Requirement",
        "description": "This is a test requirement description that is long enough to pass validation.",
        "priority": Priority.MEDIUM,
        "expected_outcome": "Successful implementation",
        "success_criteria": "All tests pass",
        "constraints": "Budget: $10,000",
        "dependencies": "None",
        "category": "testing"
    }


