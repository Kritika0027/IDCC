"""
File upload API endpoints.
"""
import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from pathlib import Path
from app.core.database import get_db
from app.core.config import settings
from app.services.document_parser import DocumentParser
from app.services.image_processor import ImageProcessor
from app.services.requirement_service import RequirementService
from app.schemas.requirement import RequirementCreate, RequirementResponse
from app.models.attachment import Attachment

router = APIRouter()

# Ensure upload directory exists
UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/document", response_model=RequirementResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    project_name: str = Form(...),
    business_owner: str = Form(...),
    db: Session = Depends(get_db)
):
    """Upload and parse a requirement document in special format."""
    # Validate file type
    allowed_extensions = {'.pdf', '.docx', '.doc', '.txt'}
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Save file
    file_path = UPLOAD_DIR / f"{file.filename}"
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file: {str(e)}"
        )
    
    # Parse document
    try:
        parsed_data = DocumentParser.parse_document(str(file_path))
        requirement_data = DocumentParser.map_to_requirement_create(
            parsed_data, project_name, business_owner
        )
    except Exception as e:
        # Clean up file on error
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error parsing document: {str(e)}"
        )
    
    # Create requirement
    requirement_create = RequirementCreate(**requirement_data)
    requirement = RequirementService.create_requirement(db, requirement_create)
    
    # Create attachment record
    attachment = Attachment(
        requirement_id=requirement.id,
        filename=file.filename,
        file_path=str(file_path),
        file_type=file_ext[1:],  # Remove dot
        file_size=file_path.stat().st_size,
        mime_type=file.content_type,
        is_image="False",
        processing_status="processed"
    )
    db.add(attachment)
    db.commit()
    
    return requirement


@router.post("/image", response_model=RequirementResponse, status_code=status.HTTP_201_CREATED)
async def upload_image(
    file: UploadFile = File(...),
    project_name: str = Form(...),
    business_owner: str = Form(...),
    db: Session = Depends(get_db)
):
    """Upload an image, perform OCR, and create requirement from extracted text."""
    # Validate file type
    if not ImageProcessor.is_image_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is not a valid image"
        )
    
    # Save file
    file_path = UPLOAD_DIR / f"{file.filename}"
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file: {str(e)}"
        )
    
    # Process image (OCR)
    processing_result = ImageProcessor.process_image_upload(str(file_path))
    extracted_text = processing_result.get("extracted_text", "")
    processing_status = processing_result.get("processing_status", "unknown")
    
    if not extracted_text:
        # Still create requirement but with note about OCR failure
        description = f"[OCR processing failed: {processing_status}] Please review the uploaded image manually."
    else:
        description = f"Extracted from image via OCR:\n\n{extracted_text}"
    
    # Create requirement from extracted text
    requirement_data = {
        "project_name": project_name,
        "business_owner": business_owner,
        "title": extracted_text[:100] if extracted_text else "Requirement from Image",
        "description": description,
        "category": "image_import",
    }
    
    requirement_create = RequirementCreate(**requirement_data)
    requirement = RequirementService.create_requirement(db, requirement_create)
    
    # Create attachment record
    attachment = Attachment(
        requirement_id=requirement.id,
        filename=file.filename,
        file_path=str(file_path),
        file_type=Path(file.filename).suffix[1:].lower(),
        file_size=file_path.stat().st_size,
        mime_type=file.content_type,
        is_image="True",
        extracted_text=extracted_text,
        processing_status=processing_status
    )
    db.add(attachment)
    db.commit()
    
    return requirement


