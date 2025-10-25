# Listener Professional v4.0 Project Structure

```
Listener_Professional/
├── 📁 src/                          # Source code
│   └── 📄 main.py                   # Main application file
│
├── 📁 config/                       # Configuration files
│   └── 📄 config.json               # Default configuration
│
├── 📁 data/                         # Application data
│   └── 📄 CaCallstatus.dat          # Call status file (auto-generated)
│
├── 📁 logs/                         # Log files (auto-generated)
│   └── 📄 listener_YYYYMMDD.log     # Daily log files
│
├── 📁 icons/                        # Application icons (auto-generated)
│   ├── 📄 listener.ico              # Windows icon
│   └── 📄 listener.png              # PNG icon
│
├── 📁 build_tools/                  # Build and development tools
│   ├── 📄 build.py                  # Main build script
│   ├── 📄 BUILD.bat                 # Windows build script
│   ├── 📄 create_icon.py            # Icon generation tool
│   └── 📄 dev_tools.py              # Development utilities
│
├── 📁 installer/                    # Installer files (auto-generated)
│   └── 📄 installer.nsi             # NSIS installer script
│
├── 📁 docs/                         # Documentation
│   ├── 📄 README.md                 # Project overview
│   └── 📄 USER_GUIDE.md             # Comprehensive user guide
│
├── 📁 dist/                         # Build output (auto-generated)
│   └── 📄 Listener.exe              # Compiled executable
│
├── 📄 requirements.txt              # Python dependencies
├── 📄 RUN.bat                       # Quick run script (development)
├── 📄 CHANGELOG.md                  # Version history
├── 📄 LICENSE.txt                   # License file (auto-generated)
└── 📄 ListenerInstaller.exe         # Windows installer (auto-generated)
```

## Directory Descriptions

### 📁 Source Code (`src/`)
Contains the main Python application code. The `main.py` file is the entry point for the entire application.

### 📁 Configuration (`config/`)
Stores application configuration files. The `config.json` file contains all user settings including PBX connection details, agent settings, and UI preferences.

### 📁 Data (`data/`)
Contains application data files. The `CaCallstatus.dat` file is automatically created and updated with call information for CRM integration.

### 📁 Logs (`logs/`)
Automatically created directory for application log files. Logs are rotated daily and old files are automatically cleaned up.

### 📁 Icons (`icons/`)
Contains application icons in various formats. Icons are automatically generated during the build process.

### 📁 Build Tools (`build_tools/`)
Development and build utilities:
- `build.py` - Main build script for creating executables and installers
- `BUILD.bat` - Windows batch script for easy building
- `create_icon.py` - Generates application icons
- `dev_tools.py` - Development utilities and testing tools

### 📁 Installer (`installer/`)
Contains NSIS installer scripts and related files for creating Windows installers.

### 📁 Documentation (`docs/`)
Comprehensive documentation including README, user guides, and technical documentation.

### 📁 Distribution (`dist/`)
Output directory for compiled executables and distribution files.

## File Descriptions

### Core Files
- `main.py` - Main application with PyQt6 GUI
- `config.json` - Application configuration file
- `requirements.txt` - Python package dependencies
- `CHANGELOG.md` - Version history and release notes

### Build Files
- `build.py` - Automated build system
- `BUILD.bat` - Windows build script
- `RUN.bat` - Development run script

### Output Files (Generated)
- `Listener.exe` - Standalone executable
- `ListenerInstaller.exe` - Windows installer
- `LICENSE.txt` - MIT license
- Various log and icon files

## Build Process

1. **Dependencies Check** - Verify all required packages
2. **Icon Generation** - Create application icons
3. **Executable Build** - Use PyInstaller to create standalone exe
4. **Installer Creation** - Generate NSIS-based Windows installer
5. **File Organization** - Organize output files for distribution

## Installation Layout

When installed using the Windows installer, the application creates the following structure:

```
C:\Program Files\Listener Professional\
├── 📄 Listener.exe
├── 📁 config\
├── 📁 logs\
├── 📁 data\
├── 📁 icons\
└── 📄 Uninstall.exe
```

## Development Workflow

1. **Setup**: Install dependencies with `pip install -r requirements.txt`
2. **Develop**: Edit `src/main.py` and test with `RUN.bat`
3. **Test**: Use `dev_tools.py` for testing and validation
4. **Build**: Run `BUILD.bat` to create executable and installer
5. **Distribute**: Share `ListenerInstaller.exe` for installation

---

*This structure provides a professional, maintainable, and scalable foundation for the Listener Professional application.*