@echo off
REM ============================================================
REM Flight Tool - Universal Launcher with Auto-venv
REM Automatically checks/creates venv and runs tools
REM ============================================================

setlocal EnableDelayedExpansion

REM Define venv path
set VENV_DIR=venv
set VENV_PYTHON=%VENV_DIR%\Scripts\python.exe
set VENV_PIP=%VENV_DIR%\Scripts\pip.exe

REM Colors using ANSI escape codes (works on Windows 10+)
echo [92m============================================================[0m
echo [92m  Flight Tool - Smart Launcher[0m
echo [92m============================================================[0m
echo.

REM Check if venv exists
if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo [93m! Virtual environment not found[0m
    echo [96m+ Creating virtual environment...[0m
    echo.

    REM Check if Python is available
    python --version >nul 2>&1
    if errorlevel 1 (
        echo [91mERROR: Python not found![0m
        echo Please install Python 3.7+ from https://python.org
        echo Make sure to check "Add to PATH" during installation
        pause
        exit /b 1
    )

    REM Create venv
    echo [96m+ Running setup_venv.py...[0m
    python setup_venv.py

    if errorlevel 1 (
        echo.
        echo [91mERROR: Failed to create virtual environment![0m
        pause
        exit /b 1
    )

    echo.
    echo [92m✓ Virtual environment created successfully![0m
    echo.
) else (
    echo [92m✓ Virtual environment found[0m
    echo.
)

REM Check which tool to run
if "%1"=="" (
    echo [96mUsage:[0m
    echo   run.bat test          - Run system tests
    echo   run.bat gui           - Launch Flight Tool GUI
    echo   run.bat scraper       - Run extended scraper
    echo   run.bat excel         - Run Excel scraper
    echo   run.bat extractor     - Run data extractor
    echo.
    echo [93mNo arguments provided - launching GUI by default...[0m
    echo.
    "%VENV_PYTHON%" FlightTool_Simple.py
    goto :end
)

REM Route to appropriate tool
if /i "%1"=="test" (
    echo [96m+ Running system tests...[0m
    echo.
    "%VENV_PYTHON%" test_system.py
    goto :end
)

if /i "%1"=="gui" (
    echo [96m+ Launching Flight Tool GUI...[0m
    echo.
    "%VENV_PYTHON%" FlightTool_Simple.py
    goto :end
)

if /i "%1"=="scraper" (
    echo [96m+ Running extended scraper...[0m
    echo.
    "%VENV_PYTHON%" scrap_only_extended.py
    goto :end
)

if /i "%1"=="excel" (
    echo [96m+ Running Excel scraper...[0m
    echo.
    "%VENV_PYTHON%" kayak_excel_scraper.py
    goto :end
)

if /i "%1"=="extractor" (
    echo [96m+ Running data extractor...[0m
    echo.
    if "%2"=="" (
        echo [91mERROR: Please provide folder path[0m
        echo Example: run.bat extractor kayak_text_data\txt_session_20250118
        pause
        exit /b 1
    )
    "%VENV_PYTHON%" simple_kayak_extractor.py %2
    goto :end
)

REM Unknown command
echo [91mUnknown command: %1[0m
echo.
echo [96mAvailable commands:[0m
echo   test          - Run system tests
echo   gui           - Launch Flight Tool GUI
echo   scraper       - Run extended scraper
echo   excel         - Run Excel scraper
echo   extractor     - Run data extractor
echo.
pause
exit /b 1

:end
echo.
echo [92m============================================================[0m
echo [92m  Done![0m
echo [92m============================================================[0m
if "%1"=="test" (
    pause
)
