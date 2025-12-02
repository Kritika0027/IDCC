# Installation Guide

## Step-by-Step Installation

### 1. Verify Python is Installed

Open Command Prompt and check:

```cmd
py --version
```

You should see something like: `Python 3.11.x` or higher.

If not installed, download from: https://www.python.org/downloads/

### 2. Navigate to Project Directory

```cmd
cd C:\Users\kriti\OneDrive\Desktop\IDCC_Application
```

### 3. Install Dependencies

**Option A: Using setup script (Easiest)**
```cmd
setup.bat
```

**Option B: Manual installation**
```cmd
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

**Option C: Using virtual environment (Recommended for production)**
```cmd
REM Create virtual environment
py -m venv venv

REM Activate it
venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt
```

### 4. Verify Installation

Check if uvicorn is installed:

```cmd
py -m pip show uvicorn
```

You should see package information.

### 5. Run the Application

```cmd
py run.py
```

Or:

```cmd
run.bat
```

## Troubleshooting

### "No module named uvicorn"

**Solution**: Install dependencies:
```cmd
py -m pip install -r requirements.txt
```

### "pip is not recognized"

**Solution**: Use:
```cmd
py -m pip install -r requirements.txt
```

### Permission Errors

**Solution**: Run Command Prompt as Administrator, or use:
```cmd
py -m pip install --user -r requirements.txt
```

### Slow Installation

**Solution**: Use a faster mirror:
```cmd
py -m pip install -r requirements.txt -i https://pypi.org/simple
```

### Virtual Environment Issues

If using virtual environment, make sure it's activated:
```cmd
venv\Scripts\activate
```

You should see `(venv)` in your prompt.

## What Gets Installed

The `requirements.txt` includes:
- FastAPI (web framework)
- Uvicorn (ASGI server)
- SQLAlchemy (database ORM)
- Pydantic (data validation)
- And many more dependencies...

## Next Steps

After installation:
1. Run `py run.py`
2. Open browser to http://localhost:8000
3. Check API docs at http://localhost:8000/docs

