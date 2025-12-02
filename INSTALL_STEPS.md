# Installation Steps for Python 3.13

## ✅ Step 1: Core Packages (Already Done!)

Core packages are installed. The app should work for basic functionality.

## Step 2: Try Running the App

Run this command:

```cmd
py run.py
```

The app should start! You can access it at http://localhost:8000

**Note**: Some features (image OCR, advanced analytics) won't work without NumPy/Pandas, but the core functionality will work.

## Step 3: Install NumPy (Optional - for Analytics)

If you want full functionality, try these options:

### Option A: Install Latest NumPy (may have Python 3.13 wheels)

```cmd
py -m pip install numpy --upgrade
```

### Option B: Install NumPy 2.0+ (better Python 3.13 support)

```cmd
py -m pip install "numpy>=2.0.0"
```

### Option C: Skip NumPy for Now

The app works without NumPy! You just won't have:
- Advanced analytics features
- Image OCR processing
- ML model predictions

But you CAN:
- Create and manage requirements
- Upload documents (PDF/DOCX)
- Use the web UI
- Use the REST API
- View basic analytics

## Step 4: Install Other Optional Packages

If NumPy installs successfully, install the rest:

```cmd
py -m pip install pandas scikit-learn pillow opencv-python pytesseract
```

Or install all at once:

```cmd
py -m pip install -r requirements.txt
```

## Quick Test

Test if core packages work:

```cmd
py -c "import fastapi; print('FastAPI: OK')"
py -c "import uvicorn; print('Uvicorn: OK')"
```

## If NumPy Still Fails

### Solution 1: Use Python 3.11 or 3.12

Download from: https://www.python.org/downloads/

Then:
```cmd
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

### Solution 2: Install Visual Studio Build Tools

1. Download: https://visualstudio.microsoft.com/downloads/
2. Install "Desktop development with C++"
3. Restart terminal
4. Run: `py -m pip install -r requirements.txt`

### Solution 3: Use Minimal Installation

Just use what's already installed - the app works fine without NumPy for most features!

## Current Status

✅ Core packages installed
✅ App should run
⏳ NumPy (optional - for advanced features)
⏳ Other analytics packages (optional)

## Next Steps

1. **Try running the app now**: `py run.py`
2. **If it works**: Great! Use it and install NumPy later if needed
3. **If NumPy is needed**: Try the options above

