# Listener Professional v4.0 - User Guide

**Complete Guide for Users and Administrators**

---

## 📚 Table of Contents

1. [Getting Started](#getting-started)
2. [User Interface Guide](#user-interface-guide)
3. [Configuration](#configuration)
4. [Operation](#operation)
5. [Troubleshooting](#troubleshooting)
6. [Advanced Features](#advanced-features)
7. [Integration Guide](#integration-guide)

---

## 🚀 Getting Started

### Installation Process

#### Method 1: Windows Installer (Recommended)
1. **Download the installer** (`ListenerInstaller.exe`)
2. **Right-click and select "Run as administrator"**
3. **Follow the installation wizard:**
   - Accept the license agreement
   - Choose components to install
   - Select installation directory
   - Configure shortcuts and auto-start options
4. **Launch the application** from desktop or start menu

#### Method 2: Portable Application
1. **Create a directory** (e.g., `C:\Listener\`)
2. **Copy `Listener.exe`** to the directory
3. **Run the application**
4. **The app will automatically create:**
   - `config/` folder for settings
   - `logs/` folder for log files
   - `data/` folder for call data
   - `icons/` folder for application icons

### First Time Setup

1. **Launch the application**
2. **The configuration wizard will appear:**
   - PBX connection is optional (demo mode available)
   - Extension number can be set later
   - File locations use sensible defaults
3. **Navigate through the tabs to configure your preferences**

---

## 🖥️ User Interface Guide

### Main Window Layout

The application features a **tabbed interface** with five main sections:

#### 1. 🌐 PBX Settings Tab
**Purpose:** Configure connection to your PBX system

**Key Elements:**
- **Enable PBX Connection:** Toggle for enabling/disabling PBX connectivity
- **PBX IP Address:** The IP address of your Asterisk/PBX server
- **PBX Port:** Usually 5038 for AMI connections
- **Username/Password:** AMI credentials for your PBX
- **Test Connection:** Verify your connection settings

**Important Notes:**
- 🔹 **PBX connection is completely optional**
- 🔹 **Demo mode works without PBX** (generates sample call events)
- 🔹 **Passwords are automatically encrypted** when saved
- 🔹 **Test connection before starting the listener**

#### 2. 👤 Agent Settings Tab
**Purpose:** Configure agent-specific settings

**Key Elements:**
- **Extension Number:** Your phone extension (e.g., 100, 101, 102)
- **Call Status File:** Location where call data is written
- **Auto-clear Delay:** Time in seconds before clearing call data
- **File Preview:** Real-time view of the call status file content

**File Management:**
- 📁 **Browse button:** Choose custom file location
- 🔄 **Refresh Preview:** Update file content display
- 📄 **Create Default File:** Generate empty call status file

#### 3. 🎛️ Control Panel Tab
**Purpose:** Monitor and control the listening service

**Key Elements:**
- **Start/Stop Buttons:** Control the AMI listener service
- **Status Display:** Real-time connection and service status
- **Call History Table:** Live view of all call events
- **Export Options:** Save call history to CSV format

**Call History Features:**
- ⏰ **Timestamp:** When the call event occurred
- 📞 **Event Type:** DialBegin, Hangup, Bridge, etc.
- 🔢 **Caller ID:** The calling phone number
- 🎯 **Destination:** The called extension or number
- 📡 **Channel:** Technical channel information

#### 4. 📋 Logs Tab
**Purpose:** View detailed application logs and events

**Key Elements:**
- **Log Display:** Scrollable view of all application events
- **Clear Logs:** Remove all displayed log entries
- **Save Logs:** Export logs to a text file
- **Auto-scroll:** Automatically scroll to show newest entries

**Log Information:**
- 🕐 **Timestamps:** Precise timing of all events
- 📊 **Event Types:** Status, errors, call events, configuration changes
- 🔍 **Detailed Messages:** Complete information for troubleshooting

#### 5. ⚙️ Settings Tab
**Purpose:** Configure application behavior and preferences

**Key Elements:**
- **Theme Selection:** Light or dark color schemes
- **Auto-start:** Launch listener automatically when opening app
- **System Tray:** Minimize to system tray option
- **Logging Level:** Control detail level of logged information
- **About Information:** Version and development details

---

## ⚙️ Configuration

### PBX Configuration

#### Asterisk AMI Setup
1. **Edit `/etc/asterisk/manager.conf`:**
   ```ini
   [general]
   enabled = yes
   port = 5038
   bindaddr = 0.0.0.0
   
   [listener_user]
   secret = your_password
   read = call,user,system
   write = call,user,system
   ```

2. **Restart Asterisk:**
   ```bash
   asterisk -rx "module reload manager"
   ```

3. **Configure firewall** to allow port 5038

#### Application Configuration
1. **Open PBX Settings tab**
2. **Enable PBX Connection**
3. **Enter your PBX details:**
   - IP: Your Asterisk server IP
   - Port: 5038 (default)
   - Username: listener_user (from manager.conf)
   - Password: your_password (from manager.conf)
4. **Click "Test Connection"** to verify
5. **Save Settings**

### Agent Configuration

#### Extension Setup
1. **Enter your extension number** (e.g., 100, 101, 102)
2. **This should match your SIP/IAX extension** in Asterisk
3. **The listener will monitor calls** to/from this extension

#### Call Status File
1. **Choose file location** using the Browse button
2. **Recommended locations:**
   - Desktop: `C:\Users\%USERNAME%\Desktop\CaCallstatus.dat`
   - Program folder: `C:\Program Files\Listener Professional\data\CaCallstatus.dat`
   - Custom location: Any writable directory
3. **Set auto-clear delay** (default: 3 seconds)

### Advanced Configuration

#### Configuration File Location
- **Installed version:** `C:\Program Files\Listener Professional\config\config.json`
- **Portable version:** `[AppDirectory]\config\config.json`

#### Manual Configuration
```json
{
  "pbx": {
    "ip": "192.168.1.100",
    "port": 5038,
    "username": "listener_user",
    "password": "base64_encoded_password",
    "enabled": true
  },
  "agent": {
    "extension": "100",
    "callstatus_file": "C:\\data\\CaCallstatus.dat",
    "auto_clear_delay": 3
  },
  "ui": {
    "theme": "light",
    "window_geometry": "900x700",
    "auto_start": false,
    "minimize_to_tray": true
  },
  "logging": {
    "level": "INFO",
    "max_files": 30,
    "max_size_mb": 10
  }
}
```

---

## 🔄 Operation

### Normal Operation

1. **Start the Application**
2. **Verify Configuration** in PBX and Agent tabs
3. **Go to Control Panel tab**
4. **Click "Start Listener"**
5. **Monitor the status display** for "Connected - Listening for calls..."
6. **Watch for call events** in the Call History table
7. **Check call status file** updates in real-time

### Call Event Flow

#### Incoming Call
1. **Phone rings** at your extension
2. **DialBegin event** is detected
3. **Call status file is updated** with caller information:
   ```xml
   <CRM>
       <callRecord>
           <CallerID>0123456789</CallerID>
           <DDI>100</DDI>
           <Date>17-10-2025</Date>
           <Time>13:45:30</Time>
       </callRecord>
   </CRM>
   ```
4. **Timer starts** for auto-clear delay
5. **Call appears** in the Call History table

#### Call End
1. **Hangup event** is detected
2. **Call status file is immediately cleared**
3. **Ready for next call** message appears
4. **Log entry** is created

### Demo Mode Operation

**When PBX is disabled:**
1. **Application runs in demo mode**
2. **Sample call events** are generated every 10-30 seconds
3. **All features work normally** for testing
4. **No real PBX connection** is required
5. **Perfect for evaluation** and training

---

## 🛠️ Troubleshooting

### Connection Issues

#### "Connection Failed" Error
**Possible Causes:**
- ❌ PBX IP address incorrect
- ❌ Port 5038 blocked by firewall
- ❌ AMI not enabled on PBX
- ❌ Username/password incorrect

**Solutions:**
1. **Verify PBX IP:** Ping the PBX server
2. **Check port:** `telnet pbx_ip 5038`
3. **Test credentials:** Use AMI debugging tools
4. **Check firewall:** Ensure port 5038 is open
5. **Try demo mode:** Disable PBX to test application

#### "Authentication Failed" Error
**Solutions:**
1. **Verify username** in manager.conf
2. **Check password** (case-sensitive)
3. **Reload Asterisk manager:** `asterisk -rx "module reload manager"`
4. **Check user permissions** in manager.conf

### File Access Issues

#### "Cannot Write to Call Status File"
**Solutions:**
1. **Check file permissions:** Ensure write access
2. **Try different location:** Use desktop or user folder
3. **Run as administrator:** For system directories
4. **Create directory:** Ensure parent directory exists

### Application Issues

#### Application Won't Start
**Solutions:**
1. **Check logs:** Look in logs/ directory
2. **Run from command line:** See error messages
3. **Reinstall:** Using the installer
4. **Check dependencies:** Ensure Python runtime (for source)

#### High CPU Usage
**Solutions:**
1. **Reduce logging level:** Set to WARNING or ERROR
2. **Check connection stability:** Reduce reconnection attempts
3. **Update configuration:** Disable unnecessary features

### Log Analysis

#### Common Log Messages
```
[INFO] Application started
[INFO] PBX connection test successful
[INFO] AMI Listener started
[INFO] Listener status: Connected - Listening for calls...
[INFO] Call event: DialBegin | From: 0123456789 | To: 100
[INFO] Call status written to: C:\data\CaCallstatus.dat
[INFO] Call status file cleared automatically
```

#### Error Messages
```
[ERROR] Connection failed: Connection refused
[ERROR] AMI Authentication failed
[ERROR] Error writing call status file: Permission denied
[ERROR] Listening error: Connection reset by peer
```

---

## 🚀 Advanced Features

### CSV Export
1. **Go to Control Panel tab**
2. **Click "Export to CSV"**
3. **Choose save location**
4. **File includes:** Timestamp, Event, Caller ID, Destination, Channel, Unique ID

### System Tray Integration
1. **Enable in Settings tab:** "Minimize to system tray"
2. **Close window** to minimize to tray
3. **Double-click tray icon** to restore
4. **Right-click tray icon** for context menu

### Auto-start Configuration
1. **During installation:** Select "Auto-start with Windows"
2. **In application:** Enable "Start listener automatically"
3. **Manual registry:** Add to Windows startup registry

### Logging Configuration

#### Log Levels
- **DEBUG:** Maximum detail (development)
- **INFO:** General information (default)
- **WARNING:** Important notices
- **ERROR:** Error conditions only

#### Log File Management
- **Daily rotation:** New file each day
- **Automatic cleanup:** Keeps last 30 files (configurable)
- **Size limits:** Maximum 10MB per file (configurable)

---

## 🔗 Integration Guide

### CRM Integration

The **CaCallstatus.dat** file is designed for CRM integration:

```xml
<CRM>
    <callRecord>
        <CallerID>0123456789</CallerID>
        <DDI>100</DDI>
        <Date>17-10-2025</Date>
        <Time>13:45:30</Time>
    </callRecord>
</CRM>
```

#### Integration Steps
1. **Configure file location** accessible to your CRM
2. **Set up file monitoring** in your CRM system
3. **Parse XML data** when file changes
4. **Handle empty file** (no active call)
5. **Implement error handling** for file access

### API Integration

For advanced integration, monitor the log files or extend the application:

1. **Log file monitoring:** Parse structured log entries
2. **Database integration:** Extend the application to write to database
3. **Web API:** Add HTTP endpoints for remote monitoring
4. **Webhook support:** Send HTTP notifications on call events

### Third-party Tools

#### File Monitoring Tools
- **FileSystemWatcher:** .NET component
- **inotify:** Linux file monitoring
- **PowerShell:** File change detection
- **Python watchdog:** Cross-platform file monitoring

#### Example PowerShell Monitor
```powershell
$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = "C:\data"
$watcher.Filter = "CaCallstatus.dat"
$watcher.EnableRaisingEvents = $true

Register-ObjectEvent -InputObject $watcher -EventName "Changed" -Action {
    $content = Get-Content "C:\data\CaCallstatus.dat"
    # Process call data...
}
```

---

## 📋 Best Practices

### Security
1. **Use strong AMI passwords**
2. **Limit AMI user permissions** to read/call only
3. **Secure the call status file** location
4. **Regular backup** of configuration
5. **Monitor access logs** on PBX

### Performance
1. **Use appropriate logging level** (INFO or WARNING)
2. **Monitor disk space** for logs
3. **Regular cleanup** of old call history
4. **Network stability** is crucial for PBX connection

### Maintenance
1. **Regular application updates**
2. **Monitor logs** for errors
3. **Test connection** periodically
4. **Backup configuration** before changes
5. **Document custom settings**

---

## 📞 Support and Resources

### Documentation
- **README.md:** Overview and quick start
- **USER_GUIDE.md:** This comprehensive guide
- **Application logs:** Detailed operational information

### Troubleshooting Resources
1. **Built-in test tools:** Connection testing
2. **Demo mode:** For testing without PBX
3. **Detailed logging:** For issue diagnosis
4. **Configuration reset:** Return to defaults

### Contact Information
- **Developer:** MiniMax Agent
- **Technology:** Python, PyQt6, PyInstaller
- **Platform:** Windows 10/11
- **License:** MIT License

---

*Listener Professional v4.0 - Your Complete PBX Call Monitoring Solution*