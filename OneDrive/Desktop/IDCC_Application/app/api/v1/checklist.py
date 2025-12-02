"""
Checklist API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.services.requirement_service import RequirementService
from app.schemas.requirement import ChecklistItemCreate, ChecklistItemUpdate, ChecklistItemResponse

router = APIRouter()


@router.post("/{requirement_id}/checklist", response_model=ChecklistItemResponse, status_code=status.HTTP_201_CREATED)
def create_checklist_item(
    requirement_id: int,
    checklist_item: ChecklistItemCreate,
    db: Session = Depends(get_db)
):
    """Create a new checklist item for a requirement."""
    result = RequirementService.create_checklist_item(db, requirement_id, checklist_item)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )
    return result


@router.post("/sub-requirements/{sub_requirement_id}/checklist", response_model=ChecklistItemResponse, status_code=status.HTTP_201_CREATED)
def create_checklist_item_for_sub_requirement(
    sub_requirement_id: int,
    checklist_item: ChecklistItemCreate,
    db: Session = Depends(get_db)
):
    """Create a new checklist item for a sub-requirement."""
    result = RequirementService.create_checklist_item(db, None, checklist_item, sub_requirement_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sub-requirement not found"
        )
    return result


@router.get("/{requirement_id}/checklist", response_model=List[ChecklistItemResponse])
def get_checklist_items(
    requirement_id: int,
    db: Session = Depends(get_db)
):
    """Get all checklist items for a requirement."""
    return RequirementService.get_checklist_items(db, requirement_id=requirement_id)


@router.get("/sub-requirements/{sub_requirement_id}/checklist", response_model=List[ChecklistItemResponse])
def get_checklist_items_for_sub_requirement(
    sub_requirement_id: int,
    db: Session = Depends(get_db)
):
    """Get all checklist items for a sub-requirement."""
    return RequirementService.get_checklist_items(db, sub_requirement_id=sub_requirement_id)


@router.put("/checklist/{checklist_item_id}", response_model=ChecklistItemResponse)
def update_checklist_item(
    checklist_item_id: int,
    checklist_item_update: ChecklistItemUpdate,
    db: Session = Depends(get_db)
):
    """Update a checklist item."""
    result = RequirementService.update_checklist_item(
        db, checklist_item_id, checklist_item_update.dict(exclude_unset=True)
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Checklist item not found"
        )
    return result


@router.delete("/checklist/{checklist_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_checklist_item(
    checklist_item_id: int,
    db: Session = Depends(get_db)
):
    """Delete a checklist item."""
    success = RequirementService.delete_checklist_item(db, checklist_item_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Checklist item not found"
        )


