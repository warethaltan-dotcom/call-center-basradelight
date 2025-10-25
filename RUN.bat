
@echo off
echo ================================================================
echo         Listener Professional v4.0 - Quick Run
echo ================================================================
echo.

echo [INFO] Installing dependencies if needed...
pip install -r requirements.txt --quiet

echo [INFO] Starting Listener Professional...
echo.

python src/main.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application failed to start
    echo Make sure all dependencies are installed
    pause
)
