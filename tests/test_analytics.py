"""
Tests for analytics engine.
"""
import pytest
from app.services.analytics_engine import AnalyticsEngine, QualityScorer
from app.models.requirement import Requirement, Priority, RequirementStatus
from app.schemas.requirement import RequirementCreate


def test_completeness_validation(db):
    """Test completeness validation rule."""
    from app.services.analytics_engine import CompletenessRule
    
    # Create requirement with missing fields
    req = Requirement(
        title="Test",
        description="Short",
        priority=Priority.MEDIUM,
        status=RequirementStatus.DRAFT,
        project_name="Test Project",
        business_owner="Test Owner"
    )
    
    result = CompletenessRule.validate(req)
    assert result["valid"] is False
    assert len(result["errors"]) > 0
    assert len(result["warnings"]) > 0


def test_quality_scoring(db, sample_requirement_data):
    """Test quality score calculation."""
    from app.services.requirement_service import RequirementService
    from app.schemas.requirement import RequirementCreate
    
    requirement_create = RequirementCreate(**sample_requirement_data)
    requirement = RequirementService.create_requirement(db, requirement_create)
    
    validation_result = AnalyticsEngine.validate_requirement(requirement)
    assert "quality_score" in validation_result
    assert 0 <= validation_result["quality_score"] <= 100


def test_analytics_summary(db, sample_requirement_data):
    """Test analytics summary statistics."""
    from app.services.requirement_service import RequirementService
    from app.schemas.requirement import RequirementCreate
    
    # Create a few requirements
    for i in range(3):
        data = sample_requirement_data.copy()
        data["title"] = f"Requirement {i}"
        requirement_create = RequirementCreate(**data)
        RequirementService.create_requirement(db, requirement_create)
    
    stats = AnalyticsEngine.get_summary_stats(db)
    assert stats["total_requirements"] == 3
    assert "by_priority" in stats
    assert "by_status" in stats


