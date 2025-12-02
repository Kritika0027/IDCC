@echo off
echo ========================================
echo PRATT - Setup Script
echo ========================================
echo.

echo Step 1: Checking Python...
py --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo.

echo Step 2: Installing dependencies...
echo This may take a few minutes...
py -m pip install --upgrade pip
py -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install dependencies!
    echo Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo You can now run the application with:
echo   py run.py
echo.
echo Or use: run.bat
echo.
pause

