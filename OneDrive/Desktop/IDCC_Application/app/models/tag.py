"""
Tag models.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Tag(Base):
    """Tag model for categorizing requirements."""
    
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=True)
    color = Column(String, nullable=True)  # For UI display
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    requirements = relationship("RequirementTag", back_populates="tag")


class RequirementTag(Base):
    """Many-to-many relationship between requirements and tags."""
    
    __tablename__ = "requirement_tags"
    
    id = Column(Integer, primary_key=True, index=True)
    requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    requirement = relationship("Requirement", back_populates="tags")
    tag = relationship("Tag", back_populates="requirements")


