# Fix: "No module named 'uvicorn'"

## Quick Fix

Run this command in Command Prompt:

```cmd
py -m pip install uvicorn[standard] fastapi
```

## Complete Installation

If you want to install everything at once, run:

```cmd
QUICK_INSTALL.bat
```

Or manually install all packages:

```cmd
py -m pip install --upgrade pip
py -m pip install fastapi "uvicorn[standard]" sqlalchemy alembic pydantic pydantic-settings python-multipart jinja2 "python-jose[cryptography]" "passlib[bcrypt]" aiofiles PyPDF2 python-docx pytest pytest-asyncio httpx
```

## Step-by-Step Installation

1. **Open Command Prompt** in the project folder

2. **Upgrade pip**:
   ```cmd
   py -m pip install --upgrade pip
   ```

3. **Install core packages**:
   ```cmd
   py -m pip install fastapi uvicorn[standard]
   ```

4. **Install database packages**:
   ```cmd
   py -m pip install sqlalchemy alembic
   ```

5. **Install other essentials**:
   ```cmd
   py -m pip install pydantic pydantic-settings python-multipart jinja2
   ```

6. **Install authentication**:
   ```cmd
   py -m pip install python-jose[cryptography] passlib[bcrypt]
   ```

7. **Install file handling**:
   ```cmd
   py -m pip install aiofiles PyPDF2 python-docx
   ```

## Verify Installation

After installing, verify uvicorn is installed:

```cmd
py -m pip show uvicorn
```

You should see package information.

## Run the App

Once installed, run:

```cmd
py run.py
```

## If Still Having Issues

1. **Check Python version**:
   ```cmd
   py --version
   ```
   Should be 3.11, 3.12, or 3.13

2. **Check pip is working**:
   ```cmd
   py -m pip --version
   ```

3. **Try using python instead of py**:
   ```cmd
   python -m pip install uvicorn[standard] fastapi
   ```

4. **Use virtual environment** (recommended):
   ```cmd
   py -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Alternative: Use the Batch Files

I've created these batch files for you:

- **QUICK_INSTALL.bat** - Installs everything at once
- **install_core.bat** - Installs core packages step by step

Just double-click them or run from Command Prompt.

