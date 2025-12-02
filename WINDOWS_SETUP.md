# Windows Setup Guide

## Common Issue: "Python was not found"

If you see this error, here are solutions:

## Solution 1: Use `py` Launcher (Recommended)

Windows 10/11 comes with a Python launcher. Try:

```cmd
py run.py
```

Or:

```cmd
py -m uvicorn app.main:app --reload
```

## Solution 2: Use `python3`

If you have Python 3 installed:

```cmd
python3 run.py
```

## Solution 3: Fix Python PATH

1. **Find Python Installation**:
   - Usually at: `C:\Users\YourName\AppData\Local\Programs\Python\`
   - Or: `C:\Python3x\`

2. **Add to PATH**:
   - Press `Win + X` → System → Advanced system settings
   - Click "Environment Variables"
   - Under "System variables", find "Path" and click "Edit"
   - Click "New" and add your Python installation path
   - Also add: `C:\Python3x\Scripts\` (replace with your path)
   - Click OK on all dialogs

3. **Restart Command Prompt** and try again

## Solution 4: Disable Microsoft Store Redirect

1. Press `Win + I` (Settings)
2. Go to: Apps → Advanced app settings → App execution aliases
3. Turn OFF the toggles for:
   - `python.exe`
   - `python3.exe`
4. Close and reopen Command Prompt

## Solution 5: Install Python Properly

1. Download Python from: https://www.python.org/downloads/
2. **IMPORTANT**: During installation, check:
   - ✅ "Add Python to PATH"
   - ✅ "Install for all users" (if you have admin rights)
3. Complete installation
4. Restart Command Prompt

## Verify Python Installation

Check if Python is installed:

```cmd
py --version
```

Or:

```cmd
python --version
```

Or:

```cmd
python3 --version
```

## Recommended: Use Virtual Environment

```cmd
# Create virtual environment
py -m venv venv

# Activate (in Command Prompt)
venv\Scripts\activate

# Activate (in PowerShell)
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run application
py run.py
```

## Alternative: Use Anaconda/Miniconda

If you have Anaconda:

```cmd
conda create -n pratt python=3.11
conda activate pratt
pip install -r requirements.txt
python run.py
```

## Quick Test

Try these commands in order until one works:

```cmd
py run.py
python3 run.py
python run.py
```

## Still Having Issues?

1. Check Python is installed: `where python` or `where py`
2. Verify Python version: Should be 3.11 or higher
3. Make sure you're in the project directory
4. Try running from PowerShell instead of Command Prompt
5. Check if antivirus is blocking Python

---

**Note**: The `py` launcher is usually the most reliable on Windows.

