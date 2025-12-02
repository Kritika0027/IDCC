"""
Attachment schemas.
"""
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class AttachmentResponse(BaseModel):
    """Schema for attachment response."""
    id: int
    requirement_id: int
    filename: str
    file_path: str
    file_type: str
    file_size: int
    mime_type: Optional[str] = None
    is_image: bool
    extracted_text: Optional[str] = None
    processing_status: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    @field_validator('is_image', mode='before')
    @classmethod
    def convert_is_image(cls, v):
        """Convert string to bool for is_image field."""
        if isinstance(v, str):
            return v.lower() == "true"
        return bool(v)
    
    class Config:
        from_attributes = True


class AttachmentCreate(BaseModel):
    """Schema for creating an attachment (used internally)."""
    requirement_id: int
    filename: str
    file_path: str
    file_type: str
    file_size: int
    mime_type: Optional[str] = None
    is_image: bool = False


