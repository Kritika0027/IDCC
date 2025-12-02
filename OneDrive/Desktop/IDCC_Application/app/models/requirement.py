"""
Requirement models.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class Priority(str, enum.Enum):
    """Priority levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RequirementStatus(str, enum.Enum):
    """Requirement status."""
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Requirement(Base):
    """Main requirement model."""
    
    __tablename__ = "requirements"
    
    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, nullable=False, index=True)
    business_owner = Column(String, nullable=False)
    business_unit = Column(String, nullable=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    priority = Column(Enum(Priority), default=Priority.MEDIUM, nullable=False)
    status = Column(Enum(RequirementStatus), default=RequirementStatus.DRAFT, nullable=False)
    expected_outcome = Column(Text, nullable=True)
    success_criteria = Column(Text, nullable=True)
    constraints = Column(Text, nullable=True)
    dependencies = Column(Text, nullable=True)
    desired_deadline = Column(DateTime(timezone=True), nullable=True)
    category = Column(String, nullable=True)
    
    # Quality score from analytics engine
    quality_score = Column(Integer, nullable=True)  # 0-100
    
    # Ownership
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_by = Column(String, nullable=True)  # For non-authenticated users
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="requirements")
    sub_requirements = relationship("SubRequirement", back_populates="requirement", cascade="all, delete-orphan")
    checklist_items = relationship("ChecklistItem", back_populates="requirement", cascade="all, delete-orphan")
    attachments = relationship("Attachment", back_populates="requirement", cascade="all, delete-orphan")
    tags = relationship("RequirementTag", back_populates="requirement", cascade="all, delete-orphan")


class SubRequirement(Base):
    """Sub-requirement model (like JIRA subtasks)."""
    
    __tablename__ = "sub_requirements"
    
    id = Column(Integer, primary_key=True, index=True)
    requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(Enum(Priority), default=Priority.MEDIUM, nullable=False)
    status = Column(Enum(RequirementStatus), default=RequirementStatus.DRAFT, nullable=False)
    order = Column(Integer, default=0, nullable=False)  # For sequencing
    
    # Relationships
    parent_id = Column(Integer, ForeignKey("sub_requirements.id"), nullable=True)  # For nested subtasks
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    requirement = relationship("Requirement", back_populates="sub_requirements")
    parent = relationship("SubRequirement", remote_side=[id], backref="children")
    checklist_items = relationship("ChecklistItem", back_populates="sub_requirement", cascade="all, delete-orphan")


class ChecklistItem(Base):
    """Checklist item for requirements or sub-requirements."""
    
    __tablename__ = "checklist_items"
    
    id = Column(Integer, primary_key=True, index=True)
    requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=True)
    sub_requirement_id = Column(Integer, ForeignKey("sub_requirements.id"), nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False, nullable=False)
    order = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    requirement = relationship("Requirement", back_populates="checklist_items")
    sub_requirement = relationship("SubRequirement", back_populates="checklist_items")


