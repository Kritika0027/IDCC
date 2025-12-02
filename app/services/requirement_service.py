"""
Service layer for requirement business logic.
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app.repositories.requirement_repository import (
    RequirementRepository,
    SubRequirementRepository,
    ChecklistItemRepository,
)
from app.schemas.requirement import (
    RequirementCreate,
    RequirementUpdate,
    SubRequirementCreate,
    ChecklistItemCreate,
)


class RequirementService:
    """Service for requirement operations."""
    
    @staticmethod
    def create_requirement(db: Session, requirement: RequirementCreate, owner_id: Optional[int] = None):
        """Create a requirement with validation."""
        return RequirementRepository.create(db, requirement, owner_id)
    
    @staticmethod
    def get_requirement(db: Session, requirement_id: int):
        """Get a requirement by ID."""
        return RequirementRepository.get(db, requirement_id)
    
    @staticmethod
    def get_all_requirements(db: Session, skip: int = 0, limit: int = 100):
        """Get all requirements."""
        return RequirementRepository.get_all(db, skip, limit)
    
    @staticmethod
    def update_requirement(db: Session, requirement_id: int, requirement_update: RequirementUpdate):
        """Update a requirement."""
        return RequirementRepository.update(db, requirement_id, requirement_update)
    
    @staticmethod
    def delete_requirement(db: Session, requirement_id: int) -> bool:
        """Delete a requirement."""
        return RequirementRepository.delete(db, requirement_id)
    
    @staticmethod
    def create_sub_requirement(db: Session, requirement_id: int, sub_requirement: SubRequirementCreate):
        """Create a sub-requirement."""
        # Verify parent requirement exists
        parent = RequirementRepository.get(db, requirement_id)
        if not parent:
            return None
        
        return SubRequirementRepository.create(db, sub_requirement.dict(), requirement_id)
    
    @staticmethod
    def get_sub_requirements(db: Session, requirement_id: int) -> List:
        """Get all sub-requirements for a requirement."""
        return SubRequirementRepository.get_by_requirement(db, requirement_id)
    
    @staticmethod
    def update_sub_requirement(db: Session, sub_requirement_id: int, sub_requirement_update: dict):
        """Update a sub-requirement."""
        return SubRequirementRepository.update(db, sub_requirement_id, sub_requirement_update)
    
    @staticmethod
    def delete_sub_requirement(db: Session, sub_requirement_id: int) -> bool:
        """Delete a sub-requirement."""
        return SubRequirementRepository.delete(db, sub_requirement_id)
    
    @staticmethod
    def create_checklist_item(db: Session, requirement_id: Optional[int], 
                              checklist_item: ChecklistItemCreate, 
                              sub_requirement_id: Optional[int] = None):
        """Create a checklist item."""
        sub_req_id = checklist_item.sub_requirement_id or sub_requirement_id
        
        # Verify parent exists
        if requirement_id:
            parent = RequirementRepository.get(db, requirement_id)
            if not parent:
                return None
        elif sub_req_id:
            parent = SubRequirementRepository.get(db, sub_req_id)
            if not parent:
                return None
        else:
            return None
        
        return ChecklistItemRepository.create(
            db, 
            checklist_item.dict(exclude={"sub_requirement_id"}), 
            requirement_id, 
            sub_req_id
        )
    
    @staticmethod
    def get_checklist_items(db: Session, requirement_id: Optional[int] = None, 
                           sub_requirement_id: Optional[int] = None) -> List:
        """Get checklist items."""
        if requirement_id:
            return ChecklistItemRepository.get_by_requirement(db, requirement_id)
        elif sub_requirement_id:
            return ChecklistItemRepository.get_by_sub_requirement(db, sub_requirement_id)
        return []
    
    @staticmethod
    def update_checklist_item(db: Session, checklist_item_id: int, checklist_item_update: dict):
        """Update a checklist item."""
        return ChecklistItemRepository.update(db, checklist_item_id, checklist_item_update)
    
    @staticmethod
    def delete_checklist_item(db: Session, checklist_item_id: int) -> bool:
        """Delete a checklist item."""
        return ChecklistItemRepository.delete(db, checklist_item_id)


