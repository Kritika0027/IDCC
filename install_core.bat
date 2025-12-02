@echo off
echo ========================================
echo Installing Core Packages
echo ========================================
echo.

echo Installing essential packages...
py -m pip install --upgrade pip
echo.

echo Installing FastAPI and Uvicorn...
py -m pip install fastapi uvicorn[standard]
echo.

echo Installing database and ORM...
py -m pip install sqlalchemy alembic
echo.

echo Installing validation and forms...
py -m pip install pydantic pydantic-settings python-multipart
echo.

echo Installing templates...
py -m pip install jinja2
echo.

echo Installing authentication...
py -m pip install python-jose[cryptography] passlib[bcrypt]
echo.

echo Installing file handling...
py -m pip install aiofiles PyPDF2 python-docx
echo.

echo Installing testing...
py -m pip install pytest pytest-asyncio httpx
echo.

echo ========================================
echo Core packages installed!
echo ========================================
echo.
echo You can now run: py run.py
echo.
pause

