"""
Tag schemas.
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TagBase(BaseModel):
    """Base tag schema."""
    name: str
    description: Optional[str] = None
    color: Optional[str] = None


class TagCreate(TagBase):
    """Schema for creating a tag."""
    pass


class TagResponse(TagBase):
    """Schema for tag response."""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


