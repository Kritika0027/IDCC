"""
Attachment model.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Attachment(Base):
    """Attachment model for files and images."""
    
    __tablename__ = "attachments"
    
    id = Column(Integer, primary_key=True, index=True)
    requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # pdf, docx, image, etc.
    file_size = Column(Integer, nullable=False)  # in bytes
    mime_type = Column(String, nullable=True)
    
    # For image processing
    is_image = Column(String, default="False")  # Boolean-like string for SQLite compatibility
    extracted_text = Column(Text, nullable=True)  # OCR/extracted text
    processing_status = Column(String, nullable=True)  # pending, processed, failed
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    requirement = relationship("Requirement", back_populates="attachments")


