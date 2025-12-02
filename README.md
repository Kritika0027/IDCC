# PRATT - IDCC Requirements Assistant

A comprehensive requirements intake and analytics application built with Python and FastAPI. This system helps business users enter, structure, and analyze requirements with AI/ML-powered insights.

## Features

- **Structured Data Entry**: Web-based form for entering business requirements
- **Document Parsing**: Automatic parsing of requirement documents (PDF, DOCX, TXT) in special format
- **Image Processing**: OCR support for extracting requirements from images
- **JIRA-like Hierarchy**: Break requirements into sub-requirements and checklist items
- **Analytics Engine**: Quality scoring, validation, and suggestions for improvement
- **REST API**: Full CRUD operations with OpenAPI documentation
- **ML Scaffolding**: Extensible framework for machine learning models

## Tech Stack

- **Backend**: FastAPI
- **Database**: SQLite (easily switchable to PostgreSQL)
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Frontend**: Jinja2 templates with modern CSS
- **AI/ML**: scikit-learn, pandas (scaffolding)
- **Image Processing**: OpenCV, Pillow, Tesseract OCR
- **Testing**: pytest

## Project Structure

```
IDCC_Application/
├── app/
│   ├── api/              # API routes
│   │   └── v1/           # API version 1
│   ├── core/             # Core configuration
│   ├── models/           # Database models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   ├── repositories/     # Data access layer
│   ├── web/              # Web UI routes
│   ├── templates/        # Jinja2 templates
│   └── static/           # Static files
├── tests/                # Test suite
├── alembic/              # Database migrations
├── uploads/              # Uploaded files
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
└── README.md           # This file
```

## Installation

### Prerequisites

- Python 3.11+
- Tesseract OCR (for image processing)
  - **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
  - **macOS**: `brew install tesseract`
  - **Linux**: `sudo apt-get install tesseract-ocr`

### Setup

1. **Clone the repository** (or navigate to project directory)

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment** (optional):
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Initialize database**:
   ```bash
   # Database tables are created automatically on first run
   # Or use Alembic for migrations:
   alembic upgrade head
   ```

6. **Run the application**:

   **Windows:**
   ```bash
   # Using py launcher (recommended)
   py run.py
   
   # Or using uvicorn
   py -m uvicorn app.main:app --reload
   
   # Or using batch file
   run.bat
   ```

   **Linux/Mac:**
   ```bash
   # Using run.py
   python3 run.py
   
   # Or using uvicorn
   uvicorn app.main:app --reload
   
   # Or using shell script
   chmod +x run.sh
   ./run.sh
   ```

7. **Access the application**:
   - Web UI: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## Usage

### Web UI

1. **Create a Requirement**:
   - Navigate to http://localhost:8000/requirements/new
   - Fill out the form with requirement details
   - Submit to create the requirement

2. **View Requirements**:
   - Home page lists all requirements
   - Click on a requirement to view details

3. **Add Sub-Requirements**:
   - On requirement detail page, click "Add Sub-Requirement"
   - Break down the requirement into smaller tasks

4. **Manage Checklist**:
   - Add checklist items to track progress
   - Toggle items as completed

5. **Upload Documents**:
   - Go to /upload
   - Upload PDF/DOCX/TXT documents in special format
   - Or upload images for OCR processing

6. **View Analytics**:
   - Navigate to /analytics for summary statistics
   - Get suggestions for improving requirements

### REST API

#### Requirements

**Create Requirement**:
```bash
curl -X POST "http://localhost:8000/api/v1/requirements/" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "My Project",
    "business_owner": "John Doe",
    "title": "New Feature",
    "description": "Detailed description here...",
    "priority": "high"
  }'
```

**Get All Requirements**:
```bash
curl "http://localhost:8000/api/v1/requirements/"
```

**Get Requirement by ID**:
```bash
curl "http://localhost:8000/api/v1/requirements/1"
```

**Update Requirement**:
```bash
curl -X PUT "http://localhost:8000/api/v1/requirements/1" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title"}'
```

**Delete Requirement**:
```bash
curl -X DELETE "http://localhost:8000/api/v1/requirements/1"
```

#### Sub-Requirements

**Create Sub-Requirement**:
```bash
curl -X POST "http://localhost:8000/api/v1/requirements/1/sub-requirements" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Sub-task 1",
    "description": "Description",
    "priority": "medium"
  }'
```

**Get Sub-Requirements**:
```bash
curl "http://localhost:8000/api/v1/requirements/1/sub-requirements"
```

#### Checklist

**Create Checklist Item**:
```bash
curl -X POST "http://localhost:8000/api/v1/requirements/1/checklist" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Check item",
    "description": "Description"
  }'
```

**Update Checklist Item**:
```bash
curl -X PUT "http://localhost:8000/api/v1/requirements/checklist/1" \
  -H "Content-Type: application/json" \
  -d '{"is_completed": true}'
```

#### Uploads

**Upload Document**:
```bash
curl -X POST "http://localhost:8000/api/v1/upload/document" \
  -F "file=@requirement.pdf" \
  -F "project_name=My Project" \
  -F "business_owner=John Doe"
```

**Upload Image (OCR)**:
```bash
curl -X POST "http://localhost:8000/api/v1/upload/image" \
  -F "file=@requirement.jpg" \
  -F "project_name=My Project" \
  -F "business_owner=John Doe"
```

#### Analytics

**Get Summary Statistics**:
```bash
curl "http://localhost:8000/api/v1/analytics/summary"
```

**Get Suggestions for Requirement**:
```bash
curl "http://localhost:8000/api/v1/analytics/suggestions/1"
```

**Validate Requirement**:
```bash
curl -X POST "http://localhost:8000/api/v1/analytics/validate/1"
```

#### Authentication

**Register User**:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "secretpassword",
    "full_name": "John Doe"
  }'
```

**Login**:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=secretpassword"
```

## Document Format

The system can parse requirement documents with the following structure:

```
Business Requirement
[Main requirement description]

Scope
[What is included]

Out of Scope
[What is excluded]

Assumptions
[Assumptions and risks]

Constraints
[Time, cost, technical constraints]

Dependencies
[Other requirements or systems]

Success Metrics
[How success will be measured]
```

The parser is flexible and can handle variations in section names.

## Database Migrations

Using Alembic for database migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app tests/
```

## Docker

### Build and Run

```bash
# Build image
docker build -t pratt-app .

# Run container
docker run -p 8000:8000 pratt-app
```

### Using Docker Compose

```bash
docker-compose up -d
```

## Configuration

Key configuration options in `.env`:

- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Secret key for JWT tokens
- `UPLOAD_DIR`: Directory for uploaded files
- `TESSERACT_CMD`: Path to Tesseract executable (if not in PATH)

## Analytics & ML

The analytics engine provides:

1. **Validation Rules**:
   - Completeness checks
   - Clarity analysis
   - Deadline validation

2. **Quality Scoring**: 0-100 score based on:
   - Field completeness
   - Structure (sub-requirements, checklist items)
   - Validation results

3. **ML Scaffolding**:
   - Feature extraction framework
   - Placeholder for success prediction
   - Ready for model training integration

## Future Enhancements

- [ ] Advanced ML models for success prediction
- [ ] Integration with external tools (JIRA, Confluence)
- [ ] Real-time collaboration features
- [ ] Advanced NLP for requirement analysis
- [ ] Export to various formats (Excel, PDF reports)
- [ ] User roles and permissions
- [ ] Requirement templates
- [ ] Version control for requirements
- [ ] Advanced search and filtering
- [ ] Dashboard with charts and visualizations

## Assumptions & Notes

1. **Database**: SQLite is used by default for simplicity. For production, switch to PostgreSQL by updating `DATABASE_URL`.

2. **OCR**: Tesseract OCR is optional. If not installed, image processing will fail gracefully.

3. **Authentication**: Basic token-based auth is implemented. For production, consider adding:
   - Refresh tokens
   - Role-based access control
   - OAuth2 integration

4. **File Storage**: Files are stored locally. For production, consider cloud storage (S3, Azure Blob, etc.).

5. **ML Models**: The ML engine is scaffolded. To train models:
   - Collect historical data with outcome labels
   - Implement training pipeline in `MLEngine.train_model()`
   - Save and load models

## Troubleshooting

**Database errors**: Ensure database file has write permissions.

**OCR not working**: Install Tesseract OCR and ensure it's in PATH, or set `TESSERACT_CMD` in `.env`.

**Import errors**: Ensure virtual environment is activated and all dependencies are installed.

**Port already in use**: Change port in `uvicorn` command or update `app/main.py`.

## License

Internal project for IDCC team.

## Support

For issues or questions, contact the development team.

---

**Version**: 0.1.0  
**Last Updated**: 2024
