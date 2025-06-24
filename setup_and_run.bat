@echo off
title Flight Tool - Setup and Run
color 0A

:: Change to script directory
cd /d "%~dp0"

echo.
echo ===============================================
echo       FLIGHT TOOL - SETUP AND RUN
echo ===============================================
echo.
echo Current directory: %CD%
echo.

:: Check if Python is installed
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8+ from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

python --version
echo OK: Python is installed
echo.

:: Check if setup script exists
if not exist "setup_components.py" (
    echo ERROR: setup_components.py not found in current directory
    echo Make sure all files are in the same folder as this batch file
    echo.
    echo Current directory: %CD%
    echo Expected files:
    echo - setup_components.py
    echo - test_system.py  
    echo - FlightTool_Simple.py
    echo.
    pause
    exit /b 1
)

:: Run setup script
echo [2/4] Running setup script...
python setup_components.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Setup failed. Check the messages above.
    pause
    exit /b 1
)

echo.
echo [3/4] Running system tests...
if exist "test_system.py" (
    python test_system.py
    if %errorlevel% neq 0 (
        echo.
        echo WARNING: Some tests failed, but continuing...
        timeout /t 3 >nul
    )
) else (
    echo WARNING: test_system.py not found, skipping tests
)

echo.
echo [4/4] Starting Flight Tool GUI...
if exist "FlightTool_Simple.py" (
    echo.
    python FlightTool_Simple.py
) else (
    echo ERROR: FlightTool_Simple.py not found
    pause
    exit /b 1
)

echo.
echo Flight Tool closed.
pause