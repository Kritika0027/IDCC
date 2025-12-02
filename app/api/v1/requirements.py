"""
Requirements API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.requirement_service import RequirementService
from app.schemas.requirement import RequirementCreate, RequirementUpdate, RequirementResponse

router = APIRouter()


@router.post("/", response_model=RequirementResponse, status_code=status.HTTP_201_CREATED)
def create_requirement(
    requirement: RequirementCreate,
    db: Session = Depends(get_db)
):
    """Create a new requirement."""
    return RequirementService.create_requirement(db, requirement)


@router.get("/", response_model=List[RequirementResponse])
def get_requirements(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all requirements."""
    return RequirementService.get_all_requirements(db, skip, limit)


@router.get("/{requirement_id}", response_model=RequirementResponse)
def get_requirement(
    requirement_id: int,
    db: Session = Depends(get_db)
):
    """Get a requirement by ID."""
    requirement = RequirementService.get_requirement(db, requirement_id)
    if not requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )
    return requirement


@router.put("/{requirement_id}", response_model=RequirementResponse)
def update_requirement(
    requirement_id: int,
    requirement_update: RequirementUpdate,
    db: Session = Depends(get_db)
):
    """Update a requirement."""
    requirement = RequirementService.update_requirement(db, requirement_id, requirement_update)
    if not requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )
    return requirement


@router.delete("/{requirement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_requirement(
    requirement_id: int,
    db: Session = Depends(get_db)
):
    """Delete a requirement."""
    success = RequirementService.delete_requirement(db, requirement_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )


