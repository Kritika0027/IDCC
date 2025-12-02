"""
Requirement schemas.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from app.models.requirement import Priority, RequirementStatus

if TYPE_CHECKING:
    from app.schemas.tag import TagResponse


class RequirementBase(BaseModel):
    """Base requirement schema."""
    project_name: str
    business_owner: str
    business_unit: Optional[str] = None
    title: str
    description: str
    priority: Priority = Priority.MEDIUM
    expected_outcome: Optional[str] = None
    success_criteria: Optional[str] = None
    constraints: Optional[str] = None
    dependencies: Optional[str] = None
    desired_deadline: Optional[datetime] = None
    category: Optional[str] = None


class RequirementCreate(RequirementBase):
    """Schema for creating a requirement."""
    pass


class RequirementUpdate(BaseModel):
    """Schema for updating a requirement."""
    project_name: Optional[str] = None
    business_owner: Optional[str] = None
    business_unit: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Priority] = None
    status: Optional[RequirementStatus] = None
    expected_outcome: Optional[str] = None
    success_criteria: Optional[str] = None
    constraints: Optional[str] = None
    dependencies: Optional[str] = None
    desired_deadline: Optional[datetime] = None
    category: Optional[str] = None


class RequirementResponse(RequirementBase):
    """Schema for requirement response."""
    id: int
    status: RequirementStatus
    quality_score: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    sub_requirements: List["SubRequirementResponse"] = []
    checklist_items: List["ChecklistItemResponse"] = []
    tags: List["TagResponse"] = []
    
    class Config:
        from_attributes = True


class SubRequirementBase(BaseModel):
    """Base sub-requirement schema."""
    title: str
    description: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    order: int = 0
    parent_id: Optional[int] = None


class SubRequirementCreate(SubRequirementBase):
    """Schema for creating a sub-requirement."""
    pass


class SubRequirementUpdate(BaseModel):
    """Schema for updating a sub-requirement."""
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Priority] = None
    status: Optional[RequirementStatus] = None
    order: Optional[int] = None
    parent_id: Optional[int] = None


class SubRequirementResponse(SubRequirementBase):
    """Schema for sub-requirement response."""
    id: int
    requirement_id: int
    status: RequirementStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    checklist_items: List["ChecklistItemResponse"] = []
    
    class Config:
        from_attributes = True


class ChecklistItemBase(BaseModel):
    """Base checklist item schema."""
    title: str
    description: Optional[str] = None
    order: int = 0


class ChecklistItemCreate(ChecklistItemBase):
    """Schema for creating a checklist item."""
    sub_requirement_id: Optional[int] = None


class ChecklistItemUpdate(BaseModel):
    """Schema for updating a checklist item."""
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    order: Optional[int] = None


class ChecklistItemResponse(ChecklistItemBase):
    """Schema for checklist item response."""
    id: int
    requirement_id: Optional[int] = None
    sub_requirement_id: Optional[int] = None
    is_completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Update forward references - import TagResponse before rebuilding
def _rebuild_models():
    """Rebuild models with all forward references available."""
    from app.schemas.tag import TagResponse
    RequirementResponse.model_rebuild()
    SubRequirementResponse.model_rebuild()

_rebuild_models()


