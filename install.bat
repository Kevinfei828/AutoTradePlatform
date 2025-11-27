@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
color 0A

echo.
echo ==================================================
echo     SJ-Trading Project Setup
echo ==================================================
echo.

REM Check if Python is installed
python --version >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found. Please install Python 3.9+ first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python found: 
python --version
echo.

REM Check if uv is installed
where uv >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo [INFO] uv not found. Installing uv...
    echo.
    powershell -Command "iwr https://astral.sh/uv/install.ps1 -useb | iex"
    
    if !ERRORLEVEL! NEQ 0 (
        echo [ERROR] Failed to install uv. Please install manually:
        echo https://docs.astral.sh/uv/getting-started/installation/
        pause
        exit /b 1
    )
    echo [OK] uv installed successfully.
    echo.
)

REM Refresh PATH to recognize newly installed uv
set PATH=%APPDATA%\Python\Scripts;%PATH%

echo [OK] uv found:
uv --version
echo.

echo ==================================================
echo  Creating virtual environment and syncing deps...
echo ==================================================
echo.

uv sync
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to sync dependencies.
    pause
    exit /b 1
)

echo.
echo ==================================================
echo  Setup completed successfully!
echo ==================================================
echo.
echo Next steps:
echo   1. Run the project:
echo      uv run python src/sj_trading/main.py
echo   2. Or activate the virtual environment:
echo      .\.venv\Scripts\activate
echo      python src/sj_trading/main.py
echo.
echo For more info, see README.md
echo ==================================================
echo.
pause