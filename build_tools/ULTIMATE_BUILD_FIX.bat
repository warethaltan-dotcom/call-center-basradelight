@echo off
title Ultimate Build Fix - Listener v4.0
echo ========================================
echo   Ultimate Build Solution
echo   Works from anywhere!
echo ========================================
echo.

REM Find the correct directory automatically
echo [INFO] Searching for Listener files...
echo.

REM Check current directory first
if exist "src\main.py" (
    echo [FOUND] Already in correct directory
    set "PROJECT_DIR=%cd%"
    goto :build_start
)

if exist "Listener_Professional\src\main.py" (
    echo [FOUND] Listener_Professional in current directory
    set "PROJECT_DIR=%cd%\Listener_Professional"
    goto :build_start
)

if exist "..\src\main.py" (
    echo [FOUND] Project in parent directory
    cd ..
    set "PROJECT_DIR=%cd%"
    goto :build_start
)

if exist "..\Listener_Professional\src\main.py" (
    echo [FOUND] Listener_Professional in parent directory
    cd ..\Listener_Professional
    set "PROJECT_DIR=%cd%"
    goto :build_start
)

REM Search in common locations
for %%d in ("C:\Users\%USERNAME%\Desktop" "C:\Users\%USERNAME%\Downloads" "C:\temp" "C:\workspace") do (
    if exist "%%d\Listener_Professional\src\main.py" (
        echo [FOUND] Project in %%d
        cd "%%d\Listener_Professional"
        set "PROJECT_DIR=%%d\Listener_Professional"
        goto :build_start
    )
    if exist "%%d\src\main.py" (
        echo [FOUND] Project in %%d
        cd "%%d"
        set "PROJECT_DIR=%%d"
        goto :build_start
    )
)

REM If not found, create from scratch
echo [INFO] Creating project from scratch...
echo.
echo [INFO] Extracting from zip files...

for %%z in ("Listener_Professional_v4.0_Complete.zip" "*.zip") do (
    if exist "%%z" (
        echo [INFO] Found zip file: %%z
        echo [INFO] Extracting...
        powershell -command "Expand-Archive -Path '%%z' -DestinationPath '.' -Force"
        
        REM Check if extraction worked
        if exist "Listener_Professional\src\main.py" (
            echo [SUCCESS] Extracted successfully
            cd Listener_Professional
            set "PROJECT_DIR=%cd%"
            goto :build_start
        )
        
        REM Check other possible extracted folder names
        for /d %%f in (*) do (
            if exist "%%f\src\main.py" (
                echo [SUCCESS] Found project in %%f
                cd "%%f"
                set "PROJECT_DIR=%cd%"
                goto :build_start
            )
        )
    )
)

echo [ERROR] Could not find or create Listener project!
echo.
echo Available files in current directory:
dir /b
echo.
echo Please ensure you have one of:
echo 1. Listener_Professional folder with src\main.py
echo 2. A zip file with the project
echo 3. src\main.py in current directory
echo.
pause
exit /b 1

:build_start
echo.
echo ========================================
echo   Project found: %PROJECT_DIR%
echo ========================================
echo.

echo [INFO] Checking project structure...
if exist "src\main.py" (
    echo [OK] main.py found
) else (
    echo [ERROR] main.py not found in src folder!
    dir /b
    pause
    exit /b 1
)

echo.
echo [INFO] Checking Python environment...
python --version
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo.
    echo Please install Python from python.org
    echo Make sure to check "Add Python to PATH"
    pause
    exit /b 1
)

echo.
echo [INFO] Installing dependencies...
pip install pyinstaller PyQt6 requests --quiet --no-warn-script-location

echo.
echo [INFO] Cleaning previous builds...
if exist "build" rmdir /s /q "build" 2>nul
if exist "dist" rmdir /s /q "dist" 2>nul
for %%f in (*.spec) do del "%%f" 2>nul

echo [INFO] Creating output directory...
mkdir dist 2>nul

echo.
echo [INFO] Building Listener.exe...
echo This may take a few minutes...
echo.

pyinstaller ^^
    --onefile ^^
    --windowed ^^
    --name=Listener ^^
    --distpath=dist ^^
    --workpath=build ^^
    --clean ^^
    --hidden-import=PyQt6.sip ^^
    --collect-all=PyQt6 ^^
    src/main.py

echo.
echo [INFO] Checking build result...
if exist "dist\Listener.exe" (
    echo.
    echo ========================================
    echo           BUILD SUCCESS!
    echo ========================================
    echo.
    echo ✅ Executable created: %PROJECT_DIR%\dist\Listener.exe
    echo.
    echo 📁 File information:
    dir "dist\Listener.exe"
    echo.
    echo 🎉 The application is ready to use!
    echo.
    echo To run:
    echo   Double-click: dist\Listener.exe
    echo   Or from command: dist\Listener.exe
    echo.
    echo 📂 Full path: %PROJECT_DIR%\dist\Listener.exe
    echo.
) else (
    echo.
    echo ========================================
    echo           BUILD FAILED!
    echo ========================================
    echo.
    echo Checking for errors...
    if exist "build\Listener\warn-Listener.txt" (
        echo Warning file contents:
        type "build\Listener\warn-Listener.txt"
    )
    echo.
    echo Please check the error messages above.
    pause
    exit /b 1
)

echo ========================================
echo           ALL DONE!
echo ========================================
echo.
echo Your Listener.exe is ready!
echo Location: %PROJECT_DIR%\dist\Listener.exe
echo.
pause
