#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Listener Professional v4.0 - Build Script
Generates executable and installer
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Command: {cmd}")
        print(f"Error: {e.stderr}")
        return False

def clean_build_dirs():
    """Clean previous build directories"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🗑️  Cleaned {dir_name} directory")
    
    # Remove .spec files
    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()
        print(f"🗑️  Removed {spec_file}")

def create_icon():
    """Create application icon"""
    print("\n🎨 Creating application icon...")
    
    icon_dir = Path('icons')
    icon_dir.mkdir(exist_ok=True)
    
    # Create a simple icon using Python PIL (if available)
    try:
        from PIL import Image, ImageDraw
        
        # Create icon image
        img = Image.new('RGBA', (256, 256), (0, 120, 212, 255))  # Blue background
        draw = ImageDraw.Draw(img)
        
        # Draw a simple phone/listener icon
        # Phone body
        draw.rectangle([80, 60, 176, 196], fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=3)
        
        # Screen
        draw.rectangle([90, 80, 166, 140], fill=(0, 0, 0, 255))
        
        # Buttons
        for i in range(3):
            for j in range(3):
                x = 95 + j * 20
                y = 150 + i * 15
                draw.ellipse([x, y, x+10, y+10], fill=(200, 200, 200, 255))
        
        # Save as ICO
        ico_path = icon_dir / 'listener.ico'
        img.save(ico_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
        
        print(f"✅ Icon created: {ico_path}")
        return str(ico_path)
        
    except ImportError:
        print("⚠️  PIL not available, creating placeholder icon")
        
        # Create placeholder icon file
        ico_path = icon_dir / 'listener.ico'
        ico_path.touch()
        return str(ico_path)

def build_executable():
    """Build executable using PyInstaller"""
    print("\n🏗️  Building executable...")
    
    # Ensure icon exists
    icon_path = create_icon()
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',                    # Single file executable
        '--windowed',                   # No console window
        '--name=Listener',              # Executable name
        f'--icon={icon_path}',          # Application icon
        '--add-data=config;config',     # Include config directory
        '--hidden-import=PyQt6.sip',    # Ensure PyQt6 imports work
        '--collect-all=PyQt6',          # Collect all PyQt6 modules
        'src/main.py'                   # Main script
    ]
    
    return run_command(' '.join(cmd), "Building executable")

def create_installer_script():
    """Create NSIS installer script"""
    print("\n📦 Creating installer script...")
    
    installer_dir = Path('installer')
    installer_dir.mkdir(exist_ok=True)
    
    nsis_script = '''
; Listener Professional v4.0 Installer
; Created by MiniMax Agent

!define APP_NAME "Listener Professional"
!define APP_VERSION "4.0"
!define APP_PUBLISHER "MiniMax Agent"
!define APP_URL "https://minimax.ai"
!define APP_EXECUTABLE "Listener.exe"

; Compression
SetCompressor lzma

; Includes
!include "MUI2.nsh"
!include "FileAssociation.nsh"

; General
Name "${APP_NAME}"
OutFile "ListenerInstaller.exe"
Unicode True

; Default installation directory
InstallDir "$PROGRAMFILES\\${APP_NAME}"

; Get installation folder from registry if available
InstallDirRegKey HKCU "Software\\${APP_NAME}" ""

; Request application privileges
RequestExecutionLevel admin

; Interface Settings
!define MUI_ABORTWARNING
!define MUI_ICON "icons\\listener.ico"
!define MUI_UNICON "icons\\listener.ico"

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Languages
!insertmacro MUI_LANGUAGE "English"

; Installer Sections
Section "Core Application" SecCore
    SectionIn RO
    
    SetOutPath "$INSTDIR"
    
    ; Main executable
    File "dist\\${APP_EXECUTABLE}"
    
    ; Create directories
    CreateDirectory "$INSTDIR\\config"
    CreateDirectory "$INSTDIR\\logs"
    CreateDirectory "$INSTDIR\\data"
    CreateDirectory "$INSTDIR\\icons"
    
    ; Copy icon
    File /oname=icons\\listener.ico "icons\\listener.ico"
    
    ; Create default config
    FileOpen $0 "$INSTDIR\\config\\config.json" w
    FileWrite $0 '{$\r$\n'
    FileWrite $0 '    "pbx": {$\r$\n'
    FileWrite $0 '        "ip": "",$\r$\n'
    FileWrite $0 '        "port": 5038,$\r$\n'
    FileWrite $0 '        "username": "",$\r$\n'
    FileWrite $0 '        "password": "",$\r$\n'
    FileWrite $0 '        "enabled": false$\r$\n'
    FileWrite $0 '    },$\r$\n'
    FileWrite $0 '    "agent": {$\r$\n'
    FileWrite $0 '        "extension": "",$\r$\n'
    FileWrite $0 '        "callstatus_file": "$INSTDIR\\\\data\\\\CaCallstatus.dat",$\r$\n'
    FileWrite $0 '        "auto_clear_delay": 3$\r$\n'
    FileWrite $0 '    },$\r$\n'
    FileWrite $0 '    "ui": {$\r$\n'
    FileWrite $0 '        "theme": "light",$\r$\n'
    FileWrite $0 '        "window_geometry": "900x700",$\r$\n'
    FileWrite $0 '        "auto_start": false,$\r$\n'
    FileWrite $0 '        "minimize_to_tray": true$\r$\n'
    FileWrite $0 '    },$\r$\n'
    FileWrite $0 '    "logging": {$\r$\n'
    FileWrite $0 '        "level": "INFO",$\r$\n'
    FileWrite $0 '        "max_files": 30,$\r$\n'
    FileWrite $0 '        "max_size_mb": 10$\r$\n'
    FileWrite $0 '    }$\r$\n'
    FileWrite $0 '}$\r$\n'
    FileClose $0
    
    ; Store installation folder
    WriteRegStr HKCU "Software\\${APP_NAME}" "" $INSTDIR
    
    ; Create uninstaller
    WriteUninstaller "$INSTDIR\\Uninstall.exe"
    
    ; Registry entries for Add/Remove Programs
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}" "DisplayName" "${APP_NAME}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}" "UninstallString" "$INSTDIR\\Uninstall.exe"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}" "InstallLocation" "$INSTDIR"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}" "DisplayIcon" "$INSTDIR\\${APP_EXECUTABLE}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}" "Publisher" "${APP_PUBLISHER}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}" "URLInfoAbout" "${APP_URL}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}" "DisplayVersion" "${APP_VERSION}"
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}" "NoModify" 1
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}" "NoRepair" 1
SectionEnd

Section "Desktop Shortcut" SecDesktop
    CreateShortcut "$DESKTOP\\${APP_NAME}.lnk" "$INSTDIR\\${APP_EXECUTABLE}" "" "$INSTDIR\\icons\\listener.ico"
SectionEnd

Section "Start Menu Shortcuts" SecStartMenu
    CreateDirectory "$SMPROGRAMS\\${APP_NAME}"
    CreateShortcut "$SMPROGRAMS\\${APP_NAME}\\${APP_NAME}.lnk" "$INSTDIR\\${APP_EXECUTABLE}" "" "$INSTDIR\\icons\\listener.ico"
    CreateShortcut "$SMPROGRAMS\\${APP_NAME}\\Uninstall.lnk" "$INSTDIR\\Uninstall.exe"
SectionEnd

Section "Auto-start with Windows" SecAutoStart
    WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Run" "${APP_NAME}" "$INSTDIR\\${APP_EXECUTABLE}"
SectionEnd

; Descriptions
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SecCore} "Core application files (required)"
    !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} "Create a desktop shortcut"
    !insertmacro MUI_DESCRIPTION_TEXT ${SecStartMenu} "Create start menu shortcuts"
    !insertmacro MUI_DESCRIPTION_TEXT ${SecAutoStart} "Start automatically with Windows"
!insertmacro MUI_FUNCTION_DESCRIPTION_END

; Uninstaller Section
Section "Uninstall"
    ; Remove files
    Delete "$INSTDIR\\${APP_EXECUTABLE}"
    Delete "$INSTDIR\\Uninstall.exe"
    Delete "$INSTDIR\\icons\\listener.ico"
    
    ; Remove directories if empty
    RMDir "$INSTDIR\\icons"
    RMDir /r "$INSTDIR\\logs"  ; Remove logs completely
    
    ; Ask user about config and data
    MessageBox MB_YESNO "Do you want to remove configuration and data files?" IDNO skip_user_data
    RMDir /r "$INSTDIR\\config"
    RMDir /r "$INSTDIR\\data"
    skip_user_data:
    
    RMDir "$INSTDIR"
    
    ; Remove shortcuts
    Delete "$DESKTOP\\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\\${APP_NAME}\\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\\${APP_NAME}\\Uninstall.lnk"
    RMDir "$SMPROGRAMS\\${APP_NAME}"
    
    ; Remove registry entries
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}"
    DeleteRegKey HKCU "Software\\${APP_NAME}"
    DeleteRegValue HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Run" "${APP_NAME}"
SectionEnd
'''
    
    with open(installer_dir / 'installer.nsi', 'w', encoding='utf-8') as f:
        f.write(nsis_script)
    
    print(f"✅ NSIS installer script created")
    return True

def create_license():
    """Create license file"""
    license_text = '''
Listener Professional v4.0
Copyright (c) 2024 MiniMax Agent

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
    
    with open('LICENSE.txt', 'w', encoding='utf-8') as f:
        f.write(license_text)
    
    print("✅ License file created")

def build_installer():
    """Build installer using NSIS"""
    print("\n📦 Building installer...")
    
    # Check if NSIS is available
    nsis_paths = [
        r"C:\Program Files (x86)\NSIS\makensis.exe",
        r"C:\Program Files\NSIS\makensis.exe",
        "makensis"  # If in PATH
    ]
    
    nsis_exe = None
    for path in nsis_paths:
        if shutil.which(path):
            nsis_exe = path
            break
    
    if not nsis_exe:
        print("⚠️  NSIS not found. Installer creation skipped.")
        print("   To create installer, install NSIS from: https://nsis.sourceforge.io/")
        return False
    
    cmd = f'"{nsis_exe}" installer/installer.nsi'
    return run_command(cmd, "Building installer")

def create_batch_scripts():
    """Create convenient batch scripts"""
    print("\n📝 Creating batch scripts...")
    
    # Build script
    build_script = '''
@echo off
echo ================================================================
echo           Listener Professional v4.0 - Build Script
echo ================================================================
echo.

echo [INFO] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [INFO] Running build script...
python build_tools/build.py

echo.
echo [INFO] Build process completed!
echo Check the dist/ folder for the executable
echo Check the installer/ folder for the installer

echo.
echo Press any key to exit...
pause >nul
'''
    
    with open('build_tools/BUILD.bat', 'w', encoding='utf-8') as f:
        f.write(build_script)
    
    # Quick run script
    run_script = '''
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
'''
    
    with open('RUN.bat', 'w', encoding='utf-8') as f:
        f.write(run_script)
    
    print("✅ Batch scripts created")

def main():
    """Main build process"""
    print("="*60)
    print("        Listener Professional v4.0 - Build System")
    print("="*60)
    
    # Change to project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    print(f"\n📁 Working directory: {os.getcwd()}")
    
    # Clean previous builds
    clean_build_dirs()
    
    # Create license
    create_license()
    
    # Create installer script
    create_installer_script()
    
    # Create batch scripts
    create_batch_scripts()
    
    # Build executable
    if not build_executable():
        print("\n❌ Build failed!")
        return False
    
    # Build installer
    build_installer()
    
    print("\n" + "="*60)
    print("                    BUILD COMPLETE!")
    print("="*60)
    print("\n📁 Output files:")
    if os.path.exists('dist/Listener.exe'):
        print(f"   ✅ Executable: dist/Listener.exe")
    if os.path.exists('ListenerInstaller.exe'):
        print(f"   ✅ Installer: ListenerInstaller.exe")
    
    print("\n🎉 Your professional Listener application is ready!")
    print("   • Run the executable directly from dist/")
    print("   • Use the installer for distribution")
    print("   • Check docs/ for user documentation")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)