"""
Repository for requirement operations.
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from app.models.requirement import Requirement, SubRequirement, ChecklistItem
from app.schemas.requirement import RequirementCreate, RequirementUpdate


class RequirementRepository:
    """Repository for requirement CRUD operations."""
    
    @staticmethod
    def create(db: Session, requirement: RequirementCreate, owner_id: Optional[int] = None) -> Requirement:
        """Create a new requirement."""
        db_requirement = Requirement(**requirement.dict(), owner_id=owner_id)
        db.add(db_requirement)
        db.commit()
        db.refresh(db_requirement)
        return db_requirement
    
    @staticmethod
    def get(db: Session, requirement_id: int) -> Optional[Requirement]:
        """Get a requirement by ID."""
        return db.query(Requirement).filter(Requirement.id == requirement_id).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Requirement]:
        """Get all requirements with pagination."""
        return db.query(Requirement).order_by(desc(Requirement.created_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    def update(db: Session, requirement_id: int, requirement_update: RequirementUpdate) -> Optional[Requirement]:
        """Update a requirement."""
        db_requirement = RequirementRepository.get(db, requirement_id)
        if not db_requirement:
            return None
        
        update_data = requirement_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_requirement, field, value)
        
        db.commit()
        db.refresh(db_requirement)
        return db_requirement
    
    @staticmethod
    def delete(db: Session, requirement_id: int) -> bool:
        """Delete a requirement."""
        db_requirement = RequirementRepository.get(db, requirement_id)
        if not db_requirement:
            return False
        
        db.delete(db_requirement)
        db.commit()
        return True


class SubRequirementRepository:
    """Repository for sub-requirement operations."""
    
    @staticmethod
    def create(db: Session, sub_requirement: dict, requirement_id: int) -> SubRequirement:
        """Create a new sub-requirement."""
        db_sub = SubRequirement(**sub_requirement, requirement_id=requirement_id)
        db.add(db_sub)
        db.commit()
        db.refresh(db_sub)
        return db_sub
    
    @staticmethod
    def get(db: Session, sub_requirement_id: int) -> Optional[SubRequirement]:
        """Get a sub-requirement by ID."""
        return db.query(SubRequirement).filter(SubRequirement.id == sub_requirement_id).first()
    
    @staticmethod
    def get_by_requirement(db: Session, requirement_id: int) -> List[SubRequirement]:
        """Get all sub-requirements for a requirement."""
        return db.query(SubRequirement).filter(
            SubRequirement.requirement_id == requirement_id
        ).order_by(SubRequirement.order).all()
    
    @staticmethod
    def update(db: Session, sub_requirement_id: int, sub_requirement_update: dict) -> Optional[SubRequirement]:
        """Update a sub-requirement."""
        db_sub = SubRequirementRepository.get(db, sub_requirement_id)
        if not db_sub:
            return None
        
        for field, value in sub_requirement_update.items():
            if value is not None:
                setattr(db_sub, field, value)
        
        db.commit()
        db.refresh(db_sub)
        return db_sub
    
    @staticmethod
    def delete(db: Session, sub_requirement_id: int) -> bool:
        """Delete a sub-requirement."""
        db_sub = SubRequirementRepository.get(db, sub_requirement_id)
        if not db_sub:
            return False
        
        db.delete(db_sub)
        db.commit()
        return True


class ChecklistItemRepository:
    """Repository for checklist item operations."""
    
    @staticmethod
    def create(db: Session, checklist_item: dict, requirement_id: Optional[int] = None, 
               sub_requirement_id: Optional[int] = None) -> ChecklistItem:
        """Create a new checklist item."""
        db_item = ChecklistItem(**checklist_item, requirement_id=requirement_id, 
                                sub_requirement_id=sub_requirement_id)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    
    @staticmethod
    def get(db: Session, checklist_item_id: int) -> Optional[ChecklistItem]:
        """Get a checklist item by ID."""
        return db.query(ChecklistItem).filter(ChecklistItem.id == checklist_item_id).first()
    
    @staticmethod
    def get_by_requirement(db: Session, requirement_id: int) -> List[ChecklistItem]:
        """Get all checklist items for a requirement."""
        return db.query(ChecklistItem).filter(
            ChecklistItem.requirement_id == requirement_id
        ).order_by(ChecklistItem.order).all()
    
    @staticmethod
    def get_by_sub_requirement(db: Session, sub_requirement_id: int) -> List[ChecklistItem]:
        """Get all checklist items for a sub-requirement."""
        return db.query(ChecklistItem).filter(
            ChecklistItem.sub_requirement_id == sub_requirement_id
        ).order_by(ChecklistItem.order).all()
    
    @staticmethod
    def update(db: Session, checklist_item_id: int, checklist_item_update: dict) -> Optional[ChecklistItem]:
        """Update a checklist item."""
        db_item = ChecklistItemRepository.get(db, checklist_item_id)
        if not db_item:
            return None
        
        for field, value in checklist_item_update.items():
            if value is not None:
                setattr(db_item, field, value)
        
        db.commit()
        db.refresh(db_item)
        return db_item
    
    @staticmethod
    def delete(db: Session, checklist_item_id: int) -> bool:
        """Delete a checklist item."""
        db_item = ChecklistItemRepository.get(db, checklist_item_id)
        if not db_item:
            return False
        
        db.delete(db_item)
        db.commit()
        return True


