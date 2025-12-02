"""
Analytics and AI/ML engine for requirement quality assessment.
"""
from typing import Dict, List, Optional, Any
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.requirement import Requirement
from app.repositories.requirement_repository import RequirementRepository


class ValidationRule:
    """Base class for validation rules."""
    
    @staticmethod
    def validate(requirement: Requirement) -> Dict[str, Any]:
        """Validate a requirement and return warnings/errors."""
        return {"valid": True, "warnings": [], "errors": []}


class CompletenessRule(ValidationRule):
    """Check if all critical fields are filled."""
    
    @staticmethod
    def validate(requirement: Requirement) -> Dict[str, any]:
        warnings = []
        errors = []
        
        if not requirement.title or len(requirement.title.strip()) < 5:
            errors.append("Title is too short or missing")
        
        if not requirement.description or len(requirement.description.strip()) < 20:
            errors.append("Description is too short (minimum 20 characters)")
        
        if not requirement.success_criteria:
            warnings.append("Success criteria is missing")
        
        if not requirement.expected_outcome:
            warnings.append("Expected outcome is missing")
        
        if not requirement.desired_deadline:
            warnings.append("Desired deadline is not specified")
        
        if not requirement.constraints:
            warnings.append("Constraints are not specified")
        
        return {
            "valid": len(errors) == 0,
            "warnings": warnings,
            "errors": errors
        }


class ClarityRule(ValidationRule):
    """Check for ambiguous language and clarity issues."""
    
    AMBIGUOUS_PATTERNS = [
        r"\basap\b|\bas\s+soon\s+as\s+possible\b",
        r"\bsoon\b",
        r"\bbetter\b",
        r"\bfaster\b",
        r"\bimprove\b",
        r"\boptimize\b",
        r"\bsome\b",
        r"\bfew\b",
        r"\bmany\b",
    ]
    
    @staticmethod
    def validate(requirement: Requirement) -> Dict[str, any]:
        import re
        warnings = []
        
        text = f"{requirement.title} {requirement.description}".lower()
        
        for pattern in ClarityRule.AMBIGUOUS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                warnings.append(f"Ambiguous language detected: '{pattern}' - consider being more specific")
        
        return {
            "valid": True,
            "warnings": warnings,
            "errors": []
        }


class DeadlineRule(ValidationRule):
    """Validate deadline is reasonable."""
    
    @staticmethod
    def validate(requirement: Requirement) -> Dict[str, any]:
        warnings = []
        errors = []
        
        if requirement.desired_deadline:
            if requirement.desired_deadline < datetime.now(requirement.desired_deadline.tzinfo):
                errors.append("Desired deadline is in the past")
            elif (requirement.desired_deadline - datetime.now(requirement.desired_deadline.tzinfo)).days < 7:
                warnings.append("Deadline is less than 7 days away - ensure it's realistic")
        
        return {
            "valid": len(errors) == 0,
            "warnings": warnings,
            "errors": errors
        }


class QualityScorer:
    """Calculate quality score for a requirement."""
    
    @staticmethod
    def calculate_score(requirement: Requirement, validation_results: List[Dict]) -> int:
        """Calculate quality score (0-100) based on completeness and validation."""
        score = 100
        
        # Deduct for errors
        for result in validation_results:
            score -= len(result.get("errors", [])) * 15
            score -= len(result.get("warnings", [])) * 5
        
        # Bonus for having sub-requirements
        if requirement.sub_requirements:
            score += min(len(requirement.sub_requirements) * 2, 10)
        
        # Bonus for having checklist items
        if requirement.checklist_items:
            score += min(len(requirement.checklist_items) * 1, 5)
        
        # Ensure score is between 0 and 100
        return max(0, min(100, score))


class AnalyticsEngine:
    """Main analytics engine."""
    
    VALIDATION_RULES = [
        CompletenessRule,
        ClarityRule,
        DeadlineRule,
    ]
    
    @staticmethod
    def validate_requirement(requirement: Requirement) -> Dict[str, Any]:
        """Run all validation rules on a requirement."""
        all_warnings = []
        all_errors = []
        rule_results = []
        
        for rule_class in AnalyticsEngine.VALIDATION_RULES:
            result = rule_class.validate(requirement)
            rule_results.append(result)
            all_warnings.extend(result.get("warnings", []))
            all_errors.extend(result.get("errors", []))
        
        # Calculate quality score
        quality_score = QualityScorer.calculate_score(requirement, rule_results)
        
        return {
            "valid": len(all_errors) == 0,
            "warnings": all_warnings,
            "errors": all_errors,
            "quality_score": quality_score,
            "rule_results": rule_results
        }
    
    @staticmethod
    def get_suggestions(requirement: Requirement) -> List[str]:
        """Get suggestions to improve requirement quality."""
        validation_result = AnalyticsEngine.validate_requirement(requirement)
        suggestions = []
        
        # Suggestions based on validation
        if validation_result["errors"]:
            suggestions.append("Fix critical errors: " + "; ".join(validation_result["errors"][:3]))
        
        if validation_result["warnings"]:
            suggestions.append("Address warnings: " + "; ".join(validation_result["warnings"][:3]))
        
        # Suggestions based on structure
        if not requirement.sub_requirements:
            suggestions.append("Consider breaking down into smaller sub-requirements for better tracking")
        
        if not requirement.checklist_items:
            suggestions.append("Add checklist items to track progress")
        
        # Suggestions based on quality score
        if validation_result["quality_score"] < 50:
            suggestions.append("Quality score is low - review and complete missing information")
        elif validation_result["quality_score"] < 70:
            suggestions.append("Quality score is moderate - consider adding more details")
        
        return suggestions
    
    @staticmethod
    def get_summary_stats(db: Session) -> Dict[str, any]:
        """Get summary statistics for all requirements."""
        requirements = RequirementRepository.get_all(db, skip=0, limit=10000)  # Get all
        
        total = len(requirements)
        if total == 0:
            return {
                "total_requirements": 0,
                "by_priority": {},
                "by_status": {},
                "by_category": {},
                "average_sub_requirements": 0,
                "average_checklist_items": 0,
                "average_quality_score": 0,
            }
        
        # Count by priority
        by_priority = {}
        for req in requirements:
            priority = req.priority.value if req.priority else "unknown"
            by_priority[priority] = by_priority.get(priority, 0) + 1
        
        # Count by status
        by_status = {}
        for req in requirements:
            status_val = req.status.value if req.status else "unknown"
            by_status[status_val] = by_status.get(status_val, 0) + 1
        
        # Count by category
        by_category = {}
        for req in requirements:
            category = req.category or "uncategorized"
            by_category[category] = by_category.get(category, 0) + 1
        
        # Calculate averages
        total_sub_reqs = sum(len(req.sub_requirements) for req in requirements)
        total_checklist_items = sum(len(req.checklist_items) for req in requirements)
        total_quality_score = sum(req.quality_score or 0 for req in requirements)
        quality_scores_count = sum(1 for req in requirements if req.quality_score is not None)
        
        return {
            "total_requirements": total,
            "by_priority": by_priority,
            "by_status": by_status,
            "by_category": by_category,
            "average_sub_requirements": round(total_sub_reqs / total, 2) if total > 0 else 0,
            "average_checklist_items": round(total_checklist_items / total, 2) if total > 0 else 0,
            "average_quality_score": round(total_quality_score / quality_scores_count, 2) if quality_scores_count > 0 else 0,
        }


class MLEngine:
    """ML/AI engine scaffolding for future model training."""
    
    @staticmethod
    def predict_success_probability(requirement: Requirement) -> float:
        """
        Placeholder for ML model to predict success probability.
        Currently returns a dummy value based on quality score.
        """
        # This is a placeholder - in production, this would use a trained model
        if requirement.quality_score is None:
            return 0.5
        
        # Simple heuristic: quality score / 100
        return requirement.quality_score / 100.0
    
    @staticmethod
    def train_model(db: Session, training_data: Optional[List] = None):
        """
        Placeholder for training ML model.
        In production, this would:
        1. Load historical requirements with outcome labels
        2. Extract features
        3. Train model (e.g., logistic regression, random forest)
        4. Save model
        """
        # Placeholder implementation
        pass
    
    @staticmethod
    def extract_features(requirement: Requirement) -> Dict[str, any]:
        """Extract features from requirement for ML model."""
        return {
            "title_length": len(requirement.title) if requirement.title else 0,
            "description_length": len(requirement.description) if requirement.description else 0,
            "has_success_criteria": bool(requirement.success_criteria),
            "has_deadline": bool(requirement.desired_deadline),
            "num_sub_requirements": len(requirement.sub_requirements),
            "num_checklist_items": len(requirement.checklist_items),
            "priority_high": 1 if requirement.priority.value == "high" else 0,
            "priority_medium": 1 if requirement.priority.value == "medium" else 0,
            "priority_low": 1 if requirement.priority.value == "low" else 0,
        }


