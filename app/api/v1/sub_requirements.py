"""
Sub-requirements API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.requirement_service import RequirementService
from app.schemas.requirement import SubRequirementCreate, SubRequirementUpdate, SubRequirementResponse

router = APIRouter()


@router.post("/{requirement_id}/sub-requirements", response_model=SubRequirementResponse, status_code=status.HTTP_201_CREATED)
def create_sub_requirement(
    requirement_id: int,
    sub_requirement: SubRequirementCreate,
    db: Session = Depends(get_db)
):
    """Create a new sub-requirement."""
    result = RequirementService.create_sub_requirement(db, requirement_id, sub_requirement)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parent requirement not found"
        )
    return result


@router.get("/{requirement_id}/sub-requirements", response_model=List[SubRequirementResponse])
def get_sub_requirements(
    requirement_id: int,
    db: Session = Depends(get_db)
):
    """Get all sub-requirements for a requirement."""
    return RequirementService.get_sub_requirements(db, requirement_id)


@router.get("/sub-requirements/{sub_requirement_id}", response_model=SubRequirementResponse)
def get_sub_requirement(
    sub_requirement_id: int,
    db: Session = Depends(get_db)
):
    """Get a sub-requirement by ID."""
    from app.repositories.requirement_repository import SubRequirementRepository
    sub_req = SubRequirementRepository.get(db, sub_requirement_id)
    if not sub_req:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sub-requirement not found"
        )
    return sub_req


@router.put("/sub-requirements/{sub_requirement_id}", response_model=SubRequirementResponse)
def update_sub_requirement(
    sub_requirement_id: int,
    sub_requirement_update: SubRequirementUpdate,
    db: Session = Depends(get_db)
):
    """Update a sub-requirement."""
    result = RequirementService.update_sub_requirement(
        db, sub_requirement_id, sub_requirement_update.dict(exclude_unset=True)
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sub-requirement not found"
        )
    return result


@router.delete("/sub-requirements/{sub_requirement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sub_requirement(
    sub_requirement_id: int,
    db: Session = Depends(get_db)
):
    """Delete a sub-requirement."""
    success = RequirementService.delete_sub_requirement(db, sub_requirement_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sub-requirement not found"
        )


