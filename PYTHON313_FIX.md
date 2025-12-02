# Python 3.13 Installation Fix

## Problem

Python 3.13 is very new and some packages (like NumPy) don't have pre-built wheels yet, requiring a C compiler to build from source.

## Solutions

### Solution 1: Use Pre-built Wheels (Recommended)

Run the fix script:

```cmd
install_fix.bat
```

This will:
- Upgrade pip
- Install NumPy with pre-built wheels
- Install other packages with binary wheels when available

### Solution 2: Install Minimal Version First

If Solution 1 doesn't work, install minimal requirements first:

```cmd
py -m pip install -r requirements-minimal.txt
```

Then try installing NumPy separately:

```cmd
py -m pip install --only-binary :all: numpy
```

### Solution 3: Install Visual Studio Build Tools

If you need to build from source:

1. Download: https://visualstudio.microsoft.com/downloads/
2. Install "Desktop development with C++" workload
3. Then run: `py -m pip install -r requirements.txt`

**Note**: This is a large download (~6GB) and takes time.

### Solution 4: Use Python 3.11 or 3.12 (Best Solution)

Python 3.11 or 3.12 are more stable and have better package support:

1. Download Python 3.11 or 3.12 from: https://www.python.org/downloads/
2. Install it (can coexist with 3.13)
3. Use it specifically:
   ```cmd
   py -3.11 -m pip install -r requirements.txt
   py -3.11 run.py
   ```

Or create a virtual environment with specific Python version:

```cmd
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

### Solution 5: Skip Optional Packages

If you don't need image processing or advanced analytics immediately:

```cmd
py -m pip install -r requirements-minimal.txt
```

This installs core functionality without:
- NumPy
- Pandas
- scikit-learn
- OpenCV
- Pillow
- pytesseract

You can add these later when needed.

## Quick Test

After installation, test if it works:

```cmd
py -c "import fastapi; print('FastAPI OK')"
py -c "import uvicorn; print('Uvicorn OK')"
```

If these work, you can run the app:

```cmd
py run.py
```

## Recommended Approach

**For immediate use**: Use Solution 4 (Python 3.11 or 3.12)

**For Python 3.13**: Use Solution 1 (install_fix.bat) or Solution 5 (minimal install)

## What Each Package Does

- **Core (required)**: fastapi, uvicorn, sqlalchemy, pydantic - Essential for the app
- **Analytics (optional)**: numpy, pandas, scikit-learn - For ML features
- **Image Processing (optional)**: pillow, opencv-python, pytesseract - For OCR

The app will work without the optional packages, but some features (image OCR, advanced analytics) won't be available.

