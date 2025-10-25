# 🎯 Listener Professional v4.0 - Complete Package

**Professional Windows Application for PBX Call Monitoring**

---

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
1. **Run the setup script:**
   ```cmd
   python SETUP.py
   ```
2. **Follow the automated installation process**
3. **Run the application:**
   ```cmd
   RUN.bat
   ```

### Option 2: Manual Setup
1. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```
2. **Run the application:**
   ```cmd
   python src/main.py
   ```

### Option 3: Build Executable
1. **Run the build script:**
   ```cmd
   build_tools/BUILD.bat
   ```
2. **Use the generated executable:**
   ```cmd
   dist/Listener.exe
   ```

---

## 📦 What's Included

### 🎯 Core Application
- **Professional GUI** built with PyQt6
- **Real-time PBX monitoring** via AMI
- **Call status file management** with auto-clearing
- **System tray integration** with minimize to tray
- **Demo mode** for testing without PBX

### 🏗️ Build System
- **Automated building** with PyInstaller
- **Windows installer** generation with NSIS
- **Icon generation** with professional graphics
- **Development tools** for testing and validation

### 📚 Documentation
- **Comprehensive README** (this file)
- **Detailed User Guide** with step-by-step instructions
- **Project Structure** documentation
- **Change Log** with version history

### ⚙️ Configuration
- **JSON-based settings** with encryption
- **Auto-save functionality** 
- **Multiple themes** (light/dark)
- **Flexible file paths** with browser dialog

---

## 🛠️ System Requirements

### Minimum Requirements
- **OS:** Windows 10 or later
- **RAM:** 256 MB
- **Storage:** 100 MB free space
- **Network:** TCP/IP connectivity (for PBX connection)

### Recommended Requirements
- **OS:** Windows 11
- **RAM:** 512 MB  
- **Storage:** 500 MB free space
- **Network:** Gigabit connection to PBX

### Software Requirements
- **Python 3.8+** (for source code)
- **PyQt6** (GUI framework)
- **PyInstaller** (for building executables)

---

## 🎮 Features Overview

### 🌐 PBX Integration
- ✅ **AMI Connection** - Real-time Asterisk monitoring
- ✅ **Connection Testing** - Built-in connection verification
- ✅ **Flexible Configuration** - Works with any AMI-compatible PBX
- ✅ **Demo Mode** - Testing without PBX connection

### 👤 Agent Management
- ✅ **Extension Monitoring** - Track specific agent extensions
- ✅ **Call Status Files** - CRM integration via XML files
- ✅ **Auto-clearing** - Configurable cleanup delays
- ✅ **File Preview** - Real-time file content viewing

### 🎛️ Control Panel
- ✅ **Start/Stop Controls** - Easy service management
- ✅ **Live Call History** - Real-time event tracking
- ✅ **CSV Export** - Data export for analysis
- ✅ **Status Monitoring** - Connection and service status

### 📋 Logging & Monitoring
- ✅ **Multi-level Logging** - DEBUG, INFO, WARNING, ERROR
- ✅ **File Rotation** - Automatic log management
- ✅ **Real-time Display** - Live log viewing
- ✅ **Export Functionality** - Save logs for analysis

### ⚙️ Advanced Settings
- ✅ **Theme Support** - Light and dark themes
- ✅ **Auto-start Options** - Windows startup integration
- ✅ **Tray Integration** - Minimize to system tray
- ✅ **Window Management** - Remember size and position

---

## 🗂️ File Structure

```
Listener_Professional/
├── 📄 SETUP.py                    # Automated setup script
├── 📄 RUN.bat                     # Quick run script
├── 📄 requirements.txt            # Python dependencies
│
├── 📁 src/
│   └── 📄 main.py                 # Main application
│
├── 📁 config/
│   └── 📄 config.json             # Configuration file
│
├── 📁 data/
│   └── 📄 CaCallstatus.dat        # Call status file
│
├── 📁 build_tools/
│   ├── 📄 build.py                # Build script
│   ├── 📄 BUILD.bat               # Windows build script
│   ├── 📄 create_icon.py          # Icon generator
│   └── 📄 dev_tools.py            # Development tools
│
├── 📁 docs/
│   ├── 📄 README.md               # Project overview
│   └── 📄 USER_GUIDE.md           # Detailed guide
│
└── 📁 dist/                       # Build output (generated)
    └── 📄 Listener.exe            # Compiled executable
```

---

## 📖 Usage Instructions

### 1. First Time Setup
1. **Run SETUP.py** for automated installation
2. **Configure PBX settings** in the application
3. **Set agent extension** and file paths
4. **Test connection** before starting monitoring

### 2. Daily Operation
1. **Launch the application**
2. **Go to Control Panel tab**
3. **Click "Start Listener"**
4. **Monitor call events** in real-time
5. **Check logs** for troubleshooting

### 3. Configuration
- **PBX Settings:** Enter IP, port, username, password
- **Agent Settings:** Set extension and file paths
- **UI Settings:** Choose theme and behavior
- **Logging:** Configure detail level and retention

### 4. Integration
- **CRM Integration:** Monitor `CaCallstatus.dat` file
- **Export Data:** Use CSV export for analysis
- **System Integration:** Use Windows startup options

---

## 🔧 Building and Distribution

### Development Workflow
1. **Edit source code** in `src/main.py`
2. **Test changes** with `RUN.bat`
3. **Build executable** with `build_tools/BUILD.bat`
4. **Test executable** in `dist/` folder
5. **Create installer** (automatic with build script)

### Distribution Options
- **Standalone EXE:** Share `dist/Listener.exe`
- **Windows Installer:** Share `ListenerInstaller.exe`
- **Source Code:** Share entire project folder

### Build Requirements
- **Python 3.8+** with PyQt6 and PyInstaller
- **NSIS** (optional, for installer creation)
- **PIL/Pillow** (optional, for icon generation)

---

## 🆘 Troubleshooting

### Common Issues

**Application won't start:**
- Check Python installation
- Install dependencies: `pip install -r requirements.txt`
- Run from command line to see errors

**PBX connection fails:**
- Verify IP address and port
- Check credentials
- Test with demo mode first
- Review firewall settings

**File access errors:**
- Check write permissions
- Try different file location
- Run as administrator if needed

**Build failures:**
- Install PyInstaller: `pip install pyinstaller`
- Check for antivirus interference
- Try building as administrator

### Getting Help
1. **Check logs** in `logs/` directory
2. **Use demo mode** for testing
3. **Review documentation** in `docs/`
4. **Try connection test** feature
5. **Reset to defaults** if needed

---

## 📄 License and Credits

### License
**MIT License** - Free for personal and commercial use

### Credits
- **Developed by:** MiniMax Agent
- **Technology:** Python, PyQt6, PyInstaller, NSIS
- **Platform:** Windows 10/11
- **Version:** 4.0 (Professional Release)

### Third-party Components
- **PyQt6:** Cross-platform GUI toolkit
- **PyInstaller:** Python to executable converter
- **NSIS:** Nullsoft Scriptable Install System

---

## 🔮 Future Development

### Planned Features (v4.1)
- 🔮 **Database integration** for call history
- 🔮 **Web dashboard** for remote monitoring
- 🔮 **REST API** for external integration
- 🔮 **Advanced reporting** and analytics

### Potential Enhancements (v4.2+)
- 🔮 **Multiple extension monitoring**
- 🔮 **Cloud connectivity** 
- 🔮 **Mobile companion app**
- 🔮 **Machine learning** for call analysis

---

## 📞 Support

### Documentation
- **README.md** - This overview
- **USER_GUIDE.md** - Comprehensive user guide
- **CHANGELOG.md** - Version history
- **PROJECT_STRUCTURE.md** - Technical details

### Self-Help Resources
- Built-in connection testing
- Demo mode for evaluation
- Comprehensive logging
- Configuration validation

### Contact
- **Developer:** MiniMax Agent
- **Project:** Listener Professional v4.0
- **Platform:** Windows Desktop Application
- **License:** MIT Open Source

---

**🎉 Thank you for choosing Listener Professional v4.0!**

*Your complete solution for professional PBX call monitoring on Windows.*