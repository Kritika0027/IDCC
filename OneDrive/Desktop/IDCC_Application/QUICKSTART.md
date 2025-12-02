# Quick Start Guide

## 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

## 2. Install Tesseract OCR (for image processing)

**Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki

**macOS**: 
```bash
brew install tesseract
```

**Linux**:
```bash
sudo apt-get install tesseract-ocr
```

## 3. Run the Application

### Windows:
```bash
# Option 1: Using py launcher (recommended for Windows)
py run.py

# Option 2: Using python3
python3 run.py

# Option 3: Using run.bat
run.bat

# Option 4: Using uvicorn directly
py -m uvicorn app.main:app --reload

# Option 5: Using Python module
py -m app.main
```

### Linux/Mac:
```bash
# Option 1: Using run.py
python3 run.py
# or
python run.py

# Option 2: Using run.sh
chmod +x run.sh
./run.sh

# Option 3: Using uvicorn directly
uvicorn app.main:app --reload

# Option 4: Using Python module
python -m app.main
```

## 4. Access the Application

- **Web UI**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## 5. Create Your First Requirement

1. Go to http://localhost:8000/requirements/new
2. Fill out the form
3. Submit to create the requirement
4. View it at http://localhost:8000

## 6. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Create a requirement
curl -X POST "http://localhost:8000/api/v1/requirements/" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Test Project",
    "business_owner": "John Doe",
    "title": "My First Requirement",
    "description": "This is a test requirement with enough text to pass validation."
  }'
```

## 7. Run Tests

```bash
pytest
```

## Troubleshooting

**Port 8000 already in use?**
- Change port: `uvicorn app.main:app --port 8001`

**Database errors?**
- Delete `pratt.db` and restart (tables will be recreated)

**OCR not working?**
- Ensure Tesseract is installed and in PATH
- Or set `TESSERACT_CMD` in `.env` file

**Import errors?**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

