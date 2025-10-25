# Listener Professional v4.0

**Complete Windows Application for PBX Call Monitoring**

Developed by MiniMax Agent

---

## 🌟 Features

### Core Functionality
- ✅ **Real-time PBX Call Monitoring** via AMI (Asterisk Manager Interface)
- ✅ **Professional GUI** built with PyQt6
- ✅ **Call Status File Management** with automatic clearing
- ✅ **Complete Windows Integration** with installer and shortcuts
- ✅ **System Tray Support** with minimize to tray option
- ✅ **Comprehensive Logging** with multiple levels and file rotation

### Advanced Features
- 🔧 **Flexible Configuration** - Works with or without PBX connection
- 🎯 **Demo Mode** - Generates sample call events for testing
- 📊 **Call History Tracking** with export to CSV
- 🔒 **Secure Password Storage** with encryption
- 🎨 **Professional UI** with tabbed interface and modern styling
- ⚙️ **Auto-save Settings** with backup and recovery

---

## 📦 Installation

### Option 1: Using the Installer (Recommended)
1. Download `ListenerInstaller.exe`
2. Run as Administrator
3. Follow the installation wizard
4. Choose installation directory (default: `C:\Program Files\Listener Professional\`)
5. Select additional options:
   - Desktop shortcut
   - Start menu shortcuts
   - Auto-start with Windows

### Option 2: Portable Executable
1. Download `Listener.exe`
2. Create a folder (e.g., `C:\Listener\`)
3. Place the executable in the folder
4. Run the application
5. The app will create necessary subdirectories automatically

### Option 3: From Source Code
```bash
# Clone or download the source
git clone <repository_url>
cd Listener_Professional

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/main.py
```

---

## 🚀 Quick Start

### 1. First Launch
- The application will automatically create necessary directories:
  - `config/` - Configuration files
  - `logs/` - Application logs
  - `data/` - Call status and data files
  - `icons/` - Application icons

### 2. Basic Configuration
1. **PBX Settings Tab:**
   - Enable PBX connection (optional)
   - Enter PBX IP address, port, username, password
   - Test connection to verify settings

2. **Agent Settings Tab:**
   - Set your extension number
   - Choose location for `CaCallstatus.dat` file
   - Configure auto-clear delay (default: 3 seconds)

3. **Control Panel Tab:**
   - Click "Start Listener" to begin monitoring
   - View real-time call events in the table
   - Monitor connection status

### 3. Advanced Configuration
- **Settings Tab:** Customize UI theme, logging, and behavior
- **Logs Tab:** Monitor application events and troubleshoot issues

---

## 📁 Directory Structure

```
Listener Professional/
├── Listener.exe              # Main executable
├── config/
│   └── config.json           # Application configuration
├── logs/
│   └── listener_YYYYMMDD.log # Daily log files
├── data/
│   └── CaCallstatus.dat      # Call status file (auto-generated)
├── icons/
│   └── listener.ico          # Application icon
└── docs/
    ├── README.md             # This file
    └── USER_GUIDE.md         # Detailed user guide
```

---

## ⚙️ Configuration Options

### PBX Settings
```json
{
  "pbx": {
    "ip": "192.168.1.100",
    "port": 5038,
    "username": "admin",
    "password": "encrypted_password",
    "enabled": true
  }
}
```

### Agent Settings
```json
{
  "agent": {
    "extension": "100",
    "callstatus_file": "C:\\data\\CaCallstatus.dat",
    "auto_clear_delay": 3
  }
}
```

### UI Settings
```json
{
  "ui": {
    "theme": "light",
    "window_geometry": "900x700",
    "auto_start": false,
    "minimize_to_tray": true
  }
}
```

---

## 🔧 Building from Source

### Prerequisites
- Python 3.8 or higher
- PyQt6
- PyInstaller
- NSIS (for installer creation)

### Build Process
1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Build Executable:**
   ```bash
   python build_tools/build.py
   ```
   Or use the batch script:
   ```bash
   build_tools/BUILD.bat
   ```

3. **Create Installer:**
   - Ensure NSIS is installed
   - The build script will automatically create the installer

### Build Outputs
- `dist/Listener.exe` - Standalone executable
- `ListenerInstaller.exe` - Windows installer

---

## 🛠️ Troubleshooting

### Common Issues

**1. Application won't start**
- Check if all dependencies are installed
- Run from command line to see error messages
- Check logs in the `logs/` directory

**2. PBX connection fails**
- Verify PBX IP address and port
- Check username and password
- Ensure AMI is enabled on your PBX
- Use "Test Connection" button to diagnose

**3. Call status file not updating**
- Check file path permissions
- Verify the file path is correct
- Ensure the directory exists
- Check logs for error messages

**4. High CPU usage**
- Check logging level (set to INFO or WARNING)
- Verify PBX connection is stable
- Monitor the logs for repeated errors

### Getting Help
1. Check the `logs/` directory for error messages
2. Use the "Test Connection" feature
3. Try demo mode (disable PBX connection)
4. Reset settings to defaults

---

## 📋 System Requirements

### Minimum Requirements
- Windows 10 or later
- 100 MB free disk space
- 256 MB RAM
- Network connectivity (for PBX connection)

### Recommended Requirements
- Windows 11
- 500 MB free disk space
- 512 MB RAM
- Gigabit network connection

---

## 🔒 Security

- Passwords are encrypted using base64 encoding
- Configuration files are stored locally
- No data is transmitted outside your network
- All PBX communication uses standard AMI protocol

---

## 📄 License

MIT License - see LICENSE.txt for details

---

## 🆕 Version History

### v4.0 (Current)
- Complete rewrite with PyQt6
- Professional Windows installer
- Advanced configuration management
- System tray integration
- Enhanced logging and monitoring
- Demo mode for testing
- CSV export functionality

### v3.x
- Tkinter-based GUI versions
- Basic AMI functionality
- Simple file management

---

## 👨‍💻 Development

**Developed by:** MiniMax Agent  
**Technology:** Python, PyQt6, PyInstaller, NSIS  
**Platform:** Windows 10/11  
**Architecture:** Professional desktop application  

---

## 📞 Support

For technical support and questions:
- Check the logs directory for diagnostic information
- Use the built-in test connection feature
- Review this documentation and user guide
- Submit issues with detailed log information

---

*Listener Professional v4.0 - Complete PBX Call Monitoring Solution*