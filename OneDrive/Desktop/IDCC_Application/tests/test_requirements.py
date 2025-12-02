"""
Tests for requirements API.
"""
import pytest
from app.services.requirement_service import RequirementService
from app.schemas.requirement import RequirementCreate, RequirementUpdate
from app.models.requirement import Priority


def test_create_requirement(db, sample_requirement_data):
    """Test creating a requirement."""
    requirement_create = RequirementCreate(**sample_requirement_data)
    requirement = RequirementService.create_requirement(db, requirement_create)
    
    assert requirement.id is not None
    assert requirement.title == sample_requirement_data["title"]
    assert requirement.project_name == sample_requirement_data["project_name"]
    assert requirement.business_owner == sample_requirement_data["business_owner"]


def test_get_requirement(db, sample_requirement_data):
    """Test getting a requirement by ID."""
    requirement_create = RequirementCreate(**sample_requirement_data)
    created = RequirementService.create_requirement(db, requirement_create)
    
    retrieved = RequirementService.get_requirement(db, created.id)
    assert retrieved is not None
    assert retrieved.id == created.id
    assert retrieved.title == sample_requirement_data["title"]


def test_update_requirement(db, sample_requirement_data):
    """Test updating a requirement."""
    requirement_create = RequirementCreate(**sample_requirement_data)
    created = RequirementService.create_requirement(db, requirement_create)
    
    update_data = RequirementUpdate(title="Updated Title")
    updated = RequirementService.update_requirement(db, created.id, update_data)
    
    assert updated.title == "Updated Title"
    assert updated.id == created.id


def test_delete_requirement(db, sample_requirement_data):
    """Test deleting a requirement."""
    requirement_create = RequirementCreate(**sample_requirement_data)
    created = RequirementService.create_requirement(db, requirement_create)
    
    success = RequirementService.delete_requirement(db, created.id)
    assert success is True
    
    retrieved = RequirementService.get_requirement(db, created.id)
    assert retrieved is None


def test_create_sub_requirement(db, sample_requirement_data):
    """Test creating a sub-requirement."""
    requirement_create = RequirementCreate(**sample_requirement_data)
    parent = RequirementService.create_requirement(db, requirement_create)
    
    from app.schemas.requirement import SubRequirementCreate
    sub_req_data = SubRequirementCreate(
        title="Sub-requirement 1",
        description="Test sub-requirement",
        priority=Priority.HIGH
    )
    
    sub_req = RequirementService.create_sub_requirement(db, parent.id, sub_req_data)
    assert sub_req.id is not None
    assert sub_req.requirement_id == parent.id
    assert sub_req.title == "Sub-requirement 1"


def test_requirements_api(client, sample_requirement_data):
    """Test requirements API endpoints."""
    # Create requirement via API
    response = client.post("/api/v1/requirements/", json=sample_requirement_data)
    assert response.status_code == 201
    requirement_id = response.json()["id"]
    
    # Get requirement
    response = client.get(f"/api/v1/requirements/{requirement_id}")
    assert response.status_code == 200
    assert response.json()["title"] == sample_requirement_data["title"]
    
    # Update requirement
    update_data = {"title": "Updated via API"}
    response = client.put(f"/api/v1/requirements/{requirement_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated via API"
    
    # Delete requirement
    response = client.delete(f"/api/v1/requirements/{requirement_id}")
    assert response.status_code == 204
    
    # Verify deleted
    response = client.get(f"/api/v1/requirements/{requirement_id}")
    assert response.status_code == 404


