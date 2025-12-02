"""
Document parser for special format requirement documents.
"""
import re
from typing import Dict, Optional, List
from pathlib import Path
import PyPDF2
from docx import Document


class DocumentParser:
    """Parser for requirement documents in special format."""
    
    # Section patterns - extensible and can be improved with ML later
    SECTION_PATTERNS = {
        "business_requirement": [
            r"business\s+requirement[s]?",
            r"requirement[s]?",
            r"overview",
        ],
        "scope": [
            r"scope",
            r"in\s+scope",
        ],
        "out_of_scope": [
            r"out\s+of\s+scope",
            r"out\s+of\s+scope",
            r"exclusions?",
        ],
        "assumptions": [
            r"assumption[s]?",
            r"assumptions?\s+&?\s+risks?",
        ],
        "constraints": [
            r"constraint[s]?",
            r"limitations?",
        ],
        "dependencies": [
            r"dependenc[ies]?",
            r"dependencies?",
        ],
        "success_metrics": [
            r"success\s+metric[s]?",
            r"success\s+criteria",
            r"kpi[s]?",
            r"measurement[s]?",
        ],
    }
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """Extract text from PDF file."""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        """Extract text from DOCX file."""
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from DOCX: {str(e)}")
    
    @staticmethod
    def extract_text_from_txt(file_path: str) -> str:
        """Extract text from TXT file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Error reading text file: {str(e)}")
    
    @staticmethod
    def extract_text(file_path: str) -> str:
        """Extract text from document based on file extension."""
        path = Path(file_path)
        extension = path.suffix.lower()
        
        if extension == '.pdf':
            return DocumentParser.extract_text_from_pdf(file_path)
        elif extension in ['.docx', '.doc']:
            return DocumentParser.extract_text_from_docx(file_path)
        elif extension == '.txt':
            return DocumentParser.extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {extension}")
    
    @staticmethod
    def detect_sections(text: str) -> Dict[str, Optional[str]]:
        """Detect sections in document text based on headings."""
        text_lower = text.lower()
        sections = {}
        
        # Split text into lines for better section detection
        lines = text.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue
            
            # Check if line is a section header
            detected_section = None
            for section_key, patterns in DocumentParser.SECTION_PATTERNS.items():
                for pattern in patterns:
                    if re.search(pattern, line_lower := line_stripped.lower(), re.IGNORECASE):
                        detected_section = section_key
                        break
                if detected_section:
                    break
            
            if detected_section:
                # Save previous section
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                # Start new section
                current_section = detected_section
                current_content = []
            else:
                # Add to current section
                if current_section:
                    current_content.append(line_stripped)
        
        # Save last section
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    @staticmethod
    def parse_document(file_path: str) -> Dict[str, any]:
        """Parse a requirement document and return structured data."""
        # Extract text
        text = DocumentParser.extract_text(file_path)
        
        # Detect sections
        sections = DocumentParser.detect_sections(text)
        
        # Map to internal structure
        parsed_data = {
            "description": sections.get("business_requirement", text[:500]),  # Fallback to first 500 chars
            "scope": sections.get("scope"),
            "out_of_scope": sections.get("out_of_scope"),
            "constraints": sections.get("constraints"),
            "dependencies": sections.get("dependencies"),
            "success_criteria": sections.get("success_metrics"),
            "assumptions": sections.get("assumptions"),
            "raw_text": text,  # Keep raw text for reference
        }
        
        return parsed_data
    
    @staticmethod
    def map_to_requirement_create(parsed_data: Dict, project_name: str, business_owner: str) -> Dict:
        """Map parsed document data to RequirementCreate schema format."""
        # Combine description with scope and assumptions
        description_parts = []
        if parsed_data.get("description"):
            description_parts.append(parsed_data["description"])
        if parsed_data.get("scope"):
            description_parts.append(f"\n\nScope:\n{parsed_data['scope']}")
        if parsed_data.get("assumptions"):
            description_parts.append(f"\n\nAssumptions:\n{parsed_data['assumptions']}")
        
        description = "\n".join(description_parts) if description_parts else "No description provided"
        
        return {
            "project_name": project_name,
            "business_owner": business_owner,
            "title": description[:100] if description else "Untitled Requirement",  # Use first 100 chars as title
            "description": description,
            "constraints": parsed_data.get("constraints"),
            "dependencies": parsed_data.get("dependencies"),
            "success_criteria": parsed_data.get("success_criteria"),
            "category": "document_import",
        }


