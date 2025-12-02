@echo off
echo ========================================
echo PRATT - Installation Fix for Python 3.13
echo ========================================
echo.

echo Detected Python 3.13 - using alternative installation method...
echo.

REM Upgrade pip first
echo Step 1: Upgrading pip...
py -m pip install --upgrade pip
echo.

REM Install numpy first with pre-built wheel
echo Step 2: Installing NumPy (this may take a moment)...
py -m pip install --only-binary :all: numpy
if %errorlevel% neq 0 (
    echo.
    echo Trying alternative NumPy installation...
    py -m pip install numpy --prefer-binary
)
echo.

REM Install other packages that might need special handling
echo Step 3: Installing other dependencies...
py -m pip install --only-binary :all: pandas scikit-learn
if %errorlevel% neq 0 (
    echo Trying with prefer-binary...
    py -m pip install --prefer-binary pandas scikit-learn
)
echo.

REM Install rest of requirements
echo Step 4: Installing remaining packages...
py -m pip install --prefer-binary -r requirements.txt
echo.

echo ========================================
echo Installation complete!
echo ========================================
echo.
echo If you still have errors, try:
echo   1. Install Visual Studio Build Tools (large download)
echo   2. Use Python 3.11 or 3.12 instead
echo.
pause

