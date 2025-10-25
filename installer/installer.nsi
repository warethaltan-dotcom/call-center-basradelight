
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
InstallDir "$PROGRAMFILES\${APP_NAME}"

; Get installation folder from registry if available
InstallDirRegKey HKCU "Software\${APP_NAME}" ""

; Request application privileges
RequestExecutionLevel admin

; Interface Settings
!define MUI_ABORTWARNING
!define MUI_ICON "icons\listener.ico"
!define MUI_UNICON "icons\listener.ico"

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
    File "dist\${APP_EXECUTABLE}"
    
    ; Create directories
    CreateDirectory "$INSTDIR\config"
    CreateDirectory "$INSTDIR\logs"
    CreateDirectory "$INSTDIR\data"
    CreateDirectory "$INSTDIR\icons"
    
    ; Copy icon
    File /oname=icons\listener.ico "icons\listener.ico"
    
    ; Create default config
    FileOpen $0 "$INSTDIR\config\config.json" w
    FileWrite $0 '{$$
'
    FileWrite $0 '    "pbx": {$$
'
    FileWrite $0 '        "ip": "",$$
'
    FileWrite $0 '        "port": 5038,$$
'
    FileWrite $0 '        "username": "",$$
'
    FileWrite $0 '        "password": "",$$
'
    FileWrite $0 '        "enabled": false$$
'
    FileWrite $0 '    },$$
'
    FileWrite $0 '    "agent": {$$
'
    FileWrite $0 '        "extension": "",$$
'
    FileWrite $0 '        "callstatus_file": "$INSTDIR\\data\\CaCallstatus.dat",$$
'
    FileWrite $0 '        "auto_clear_delay": 3$$
'
    FileWrite $0 '    },$$
'
    FileWrite $0 '    "ui": {$$
'
    FileWrite $0 '        "theme": "light",$$
'
    FileWrite $0 '        "window_geometry": "900x700",$$
'
    FileWrite $0 '        "auto_start": false,$$
'
    FileWrite $0 '        "minimize_to_tray": true$$
'
    FileWrite $0 '    },$$
'
    FileWrite $0 '    "logging": {$$
'
    FileWrite $0 '        "level": "INFO",$$
'
    FileWrite $0 '        "max_files": 30,$$
'
    FileWrite $0 '        "max_size_mb": 10$$
'
    FileWrite $0 '    }$$
'
    FileWrite $0 '}$$
'
    FileClose $0
    
    ; Store installation folder
    WriteRegStr HKCU "Software\${APP_NAME}" "" $INSTDIR
    
    ; Create uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"
    
    ; Registry entries for Add/Remove Programs
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayName" "${APP_NAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString" "$INSTDIR\Uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "InstallLocation" "$INSTDIR"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayIcon" "$INSTDIR\${APP_EXECUTABLE}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "Publisher" "${APP_PUBLISHER}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "URLInfoAbout" "${APP_URL}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayVersion" "${APP_VERSION}"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoRepair" 1
SectionEnd

Section "Desktop Shortcut" SecDesktop
    CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXECUTABLE}" "" "$INSTDIR\icons\listener.ico"
SectionEnd

Section "Start Menu Shortcuts" SecStartMenu
    CreateDirectory "$SMPROGRAMS\${APP_NAME}"
    CreateShortcut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${APP_EXECUTABLE}" "" "$INSTDIR\icons\listener.ico"
    CreateShortcut "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Auto-start with Windows" SecAutoStart
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Run" "${APP_NAME}" "$INSTDIR\${APP_EXECUTABLE}"
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
    Delete "$INSTDIR\${APP_EXECUTABLE}"
    Delete "$INSTDIR\Uninstall.exe"
    Delete "$INSTDIR\icons\listener.ico"
    
    ; Remove directories if empty
    RMDir "$INSTDIR\icons"
    RMDir /r "$INSTDIR\logs"  ; Remove logs completely
    
    ; Ask user about config and data
    MessageBox MB_YESNO "Do you want to remove configuration and data files?" IDNO skip_user_data
    RMDir /r "$INSTDIR\config"
    RMDir /r "$INSTDIR\data"
    skip_user_data:
    
    RMDir "$INSTDIR"
    
    ; Remove shortcuts
    Delete "$DESKTOP\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk"
    RMDir "$SMPROGRAMS\${APP_NAME}"
    
    ; Remove registry entries
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
    DeleteRegKey HKCU "Software\${APP_NAME}"
    DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Run" "${APP_NAME}"
SectionEnd
