@echo off
REM Windows batch script to run PRATT application
echo ========================================
echo PRATT - IDCC Requirements Assistant
echo ========================================
echo.

REM Check if uvicorn is installed
py -m pip show uvicorn >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Dependencies not installed!
    echo.
    echo Please run setup.bat first, or install manually:
    echo   py -m pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo Starting application...
echo.
echo Access the app at: http://localhost:8000
echo API docs at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Try different Python commands
py run.py 2>nul
if %errorlevel% equ 0 goto :end

python run.py 2>nul
if %errorlevel% equ 0 goto :end

python3 run.py 2>nul
if %errorlevel% equ 0 goto :end

echo.
echo ERROR: Python not found!
echo.
echo Please try one of these:
echo   1. Use: py run.py
echo   2. Use: python3 run.py
echo   3. Install Python from https://www.python.org/downloads/
echo   4. Add Python to your PATH environment variable
echo.
pause
:end

