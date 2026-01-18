@echo off
REM Check if venv exists, if not create it
if not exist "venv\Scripts\python.exe" (
    echo Virtual environment not found. Creating...
    python setup_venv.py
    if errorlevel 1 (
        echo Failed to create virtual environment!
        pause
        exit /b 1
    )
)
"venv\Scripts\python.exe" test_system.py %*
