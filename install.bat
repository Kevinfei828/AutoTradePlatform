@echo off
echo --------------------------------------------------
echo  Installing project Python environment using uv...
echo --------------------------------------------------

REM 安裝 uv
where uv >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo uv not found. Installing uv...
    powershell -Command "iwr https://astral.sh/uv/install.ps1 -useb | iex"
)

REM 確認 uv 可用
if ERRORLEVEL 1 (
    echo uv installation failed
    exit /b 1
)

REM uv 會自動讀取 .python-version，下載對應 Python
uv sync

echo --------------------------------------------------
echo  Python environment setup completed!
echo --------------------------------------------------
pause