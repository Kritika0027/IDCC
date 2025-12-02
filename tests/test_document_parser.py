"""
Tests for document parser.
"""
import pytest
import tempfile
import os
from app.services.document_parser import DocumentParser


def test_detect_sections():
    """Test section detection in text."""
    text = """
    Business Requirement
    This is the main requirement description.
    
    Scope
    This is in scope.
    
    Out of Scope
    This is out of scope.
    
    Assumptions
    We assume X, Y, Z.
    """
    
    sections = DocumentParser.detect_sections(text)
    assert "business_requirement" in sections
    assert "scope" in sections
    assert "out_of_scope" in sections
    assert "assumptions" in sections


def test_map_to_requirement_create():
    """Test mapping parsed data to requirement create format."""
    parsed_data = {
        "description": "Main requirement",
        "scope": "In scope items",
        "constraints": "Budget limit",
        "success_criteria": "All tests pass"
    }
    
    result = DocumentParser.map_to_requirement_create(
        parsed_data, "Test Project", "John Doe"
    )
    
    assert result["project_name"] == "Test Project"
    assert result["business_owner"] == "John Doe"
    assert "description" in result
    assert result["constraints"] == "Budget limit"
    assert result["success_criteria"] == "All tests pass"


