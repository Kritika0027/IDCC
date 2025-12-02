"""
Analytics API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, List
from app.core.database import get_db
from app.services.analytics_engine import AnalyticsEngine, MLEngine
from app.services.requirement_service import RequirementService

router = APIRouter()


@router.get("/summary", response_model=Dict)
def get_analytics_summary(db: Session = Depends(get_db)):
    """Get summary statistics for all requirements."""
    return AnalyticsEngine.get_summary_stats(db)


@router.get("/suggestions/{requirement_id}", response_model=Dict)
def get_suggestions(requirement_id: int, db: Session = Depends(get_db)):
    """Get suggestions to improve a requirement."""
    requirement = RequirementService.get_requirement(db, requirement_id)
    if not requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )
    
    # Validate and get quality score
    validation_result = AnalyticsEngine.validate_requirement(requirement)
    
    # Update quality score in database
    if requirement.quality_score != validation_result["quality_score"]:
        requirement.quality_score = validation_result["quality_score"]
        db.commit()
    
    # Get suggestions
    suggestions = AnalyticsEngine.get_suggestions(requirement)
    
    # Get ML prediction (placeholder)
    success_probability = MLEngine.predict_success_probability(requirement)
    
    return {
        "requirement_id": requirement_id,
        "quality_score": validation_result["quality_score"],
        "valid": validation_result["valid"],
        "warnings": validation_result["warnings"],
        "errors": validation_result["errors"],
        "suggestions": suggestions,
        "success_probability": success_probability,
    }


@router.post("/validate/{requirement_id}", response_model=Dict)
def validate_requirement(requirement_id: int, db: Session = Depends(get_db)):
    """Validate a requirement and update quality score."""
    requirement = RequirementService.get_requirement(db, requirement_id)
    if not requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )
    
    validation_result = AnalyticsEngine.validate_requirement(requirement)
    
    # Update quality score
    requirement.quality_score = validation_result["quality_score"]
    db.commit()
    
    return validation_result


