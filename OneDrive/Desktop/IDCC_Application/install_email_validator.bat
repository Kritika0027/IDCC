@echo off
echo Installing email-validator...
py -m pip install email-validator
if %errorlevel% equ 0 (
    echo.
    echo email-validator installed successfully!
    echo You can now run: py run.py
) else (
    echo.
    echo Installation failed. Try running manually:
    echo   py -m pip install email-validator
)
pause

