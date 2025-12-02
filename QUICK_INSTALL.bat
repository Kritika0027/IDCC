@echo off
REM Quick install script - installs everything needed to run the app
echo Installing all required packages...
echo.

py -m pip install --upgrade pip
py -m pip install fastapi "uvicorn[standard]" sqlalchemy alembic pydantic pydantic-settings email-validator python-multipart jinja2 "python-jose[cryptography]" "passlib[bcrypt]" aiofiles PyPDF2 python-docx pytest pytest-asyncio httpx

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo Installation successful!
    echo ========================================
    echo.
    echo Run the app with: py run.py
    echo.
) else (
    echo.
    echo ========================================
    echo Installation had errors
    echo ========================================
    echo.
    echo Try running: install_core.bat
    echo.
)

pause

