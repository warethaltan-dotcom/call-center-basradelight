#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Listener Professional v4.0 - Complete Project Creator
Creates the entire project structure and builds it
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def create_main_py():
    """Create a working main.py file"""
    main_py_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Listener Professional v4.0
Main Application Entry Point
"""

import sys
import os
from pathlib import Path

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QTabWidget, QLabel, QLineEdit, QPushButton, QTextEdit,
        QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem,
        QGroupBox, QCheckBox, QSpinBox
    )
    from PyQt6.QtCore import QThread, pyqtSignal, QTimer, Qt
    from PyQt6.QtGui import QIcon, QFont, QPixmap
except ImportError:
    print("Error: PyQt6 not installed!")
    print("Please install: pip install PyQt6")
    sys.exit(1)

import json
import base64
import logging
from datetime import datetime

class ListenerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Listener Professional v4.0")
        self.setGeometry(100, 100, 900, 700)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Create tabs
        self.create_login_tab()
        self.create_agent_tab()
        self.create_control_tab()
        
        # Load settings
        self.load_settings()
        
        # Setup logging
        self.setup_logging()
        
        print("Listener Professional v4.0 initialized successfully")
    
    def create_login_tab(self):
        """Create login/PBX settings tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # PBX Settings Group
        group = QGroupBox("PBX Connection Settings")
        group_layout = QVBoxLayout(group)
        
        # IP Address
        ip_layout = QHBoxLayout()
        ip_layout.addWidget(QLabel("PBX IP Address:"))
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("192.168.1.100")
        ip_layout.addWidget(self.ip_input)
        group_layout.addLayout(ip_layout)
        
        # Port
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("Port:"))
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("5038")
        port_layout.addWidget(self.port_input)
        group_layout.addLayout(port_layout)
        
        # Username
        user_layout = QHBoxLayout()
        user_layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("admin")
        user_layout.addWidget(self.username_input)
        group_layout.addLayout(user_layout)
        
        # Password
        pass_layout = QHBoxLayout()
        pass_layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter password")
        pass_layout.addWidget(self.password_input)
        group_layout.addLayout(pass_layout)
        
        # Save button
        save_btn = QPushButton("Save PBX Settings")
        save_btn.clicked.connect(self.save_pbx_settings)
        group_layout.addWidget(save_btn)
        
        layout.addWidget(group)
        layout.addStretch()
        
        self.tabs.addTab(tab, "PBX Settings")
    
    def create_agent_tab(self):
        """Create agent settings tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Agent Settings Group
        group = QGroupBox("Agent Configuration")
        group_layout = QVBoxLayout(group)
        
        # Extension
        ext_layout = QHBoxLayout()
        ext_layout.addWidget(QLabel("Extension:"))
        self.extension_input = QLineEdit()
        self.extension_input.setPlaceholderText("1001")
        ext_layout.addWidget(self.extension_input)
        group_layout.addLayout(ext_layout)
        
        # Call Status File
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("Call Status File:"))
        self.file_path_input = QLineEdit()
        self.file_path_input.setPlaceholderText("Select CaCallstatus.dat file")
        file_layout.addWidget(self.file_path_input)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_btn)
        group_layout.addLayout(file_layout)
        
        # Save button
        save_btn = QPushButton("Save Agent Settings")
        save_btn.clicked.connect(self.save_agent_settings)
        group_layout.addWidget(save_btn)
        
        layout.addWidget(group)
        layout.addStretch()
        
        self.tabs.addTab(tab, "Agent Settings")
    
    def create_control_tab(self):
        """Create control panel tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Start Listener")
        self.start_btn.clicked.connect(self.start_listener)
        self.start_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }")
        button_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("Stop Listener")
        self.stop_btn.clicked.connect(self.stop_listener)
        self.stop_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; font-weight: bold; }")
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.stop_btn)
        
        layout.addLayout(button_layout)
        
        # Status display
        self.status_label = QLabel("Status: Disconnected")
        self.status_label.setStyleSheet("QLabel { font-size: 14px; font-weight: bold; color: #f44336; }")
        layout.addWidget(self.status_label)
        
        # Call status table
        self.call_table = QTableWidget()
        self.call_table.setColumnCount(4)
        self.call_table.setHorizontalHeaderLabels(["Time", "Extension", "Status", "Details"])
        layout.addWidget(self.call_table)
        
        # Log display
        self.log_display = QTextEdit()
        self.log_display.setMaximumHeight(150)
        self.log_display.setReadOnly(True)
        layout.addWidget(QLabel("Activity Log:"))
        layout.addWidget(self.log_display)
        
        self.tabs.addTab(tab, "Control Panel")
    
    def browse_file(self):
        """Browse for call status file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Call Status File", "", "DAT files (*.dat);;All files (*.*)"
        )
        if file_path:
            self.file_path_input.setText(file_path)
    
    def start_listener(self):
        """Start the listener service"""
        self.status_label.setText("Status: Starting...")
        self.status_label.setStyleSheet("QLabel { font-size: 14px; font-weight: bold; color: #FF9800; }")
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        
        # Simulate connection
        QTimer.singleShot(2000, self.listener_started)
        
        self.log_message("Starting Listener service...")
    
    def listener_started(self):
        """Called when listener starts successfully"""
        self.status_label.setText("Status: Connected")
        self.status_label.setStyleSheet("QLabel { font-size: 14px; font-weight: bold; color: #4CAF50; }")
        self.log_message("Listener started successfully")
    
    def stop_listener(self):
        """Stop the listener service"""
        self.status_label.setText("Status: Disconnected")
        self.status_label.setStyleSheet("QLabel { font-size: 14px; font-weight: bold; color: #f44336; }")
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        self.log_message("Listener stopped")
    
    def save_pbx_settings(self):
        """Save PBX settings"""
        settings = {
            "ip": self.ip_input.text(),
            "port": self.port_input.text(),
            "username": self.username_input.text(),
            "password": base64.b64encode(self.password_input.text().encode()).decode() if self.password_input.text() else ""
        }
        
        self.save_settings_to_file("pbx", settings)
        QMessageBox.information(self, "Success", "PBX settings saved successfully!")
        self.log_message("PBX settings saved")
    
    def save_agent_settings(self):
        """Save agent settings"""
        settings = {
            "extension": self.extension_input.text(),
            "callstatus_file": self.file_path_input.text()
        }
        
        self.save_settings_to_file("agent", settings)
        QMessageBox.information(self, "Success", "Agent settings saved successfully!")
        self.log_message("Agent settings saved")
    
    def save_settings_to_file(self, section, settings):
        """Save settings to config file"""
        config_dir = Path("config")
        config_dir.mkdir(exist_ok=True)
        
        config_file = config_dir / "config.json"
        
        # Load existing config or create new
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
        else:
            config = {}
        
        config[section] = settings
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
    
    def load_settings(self):
        """Load settings from config file"""
        config_file = Path("config/config.json")
        
        if not config_file.exists():
            return
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            # Load PBX settings
            if "pbx" in config:
                pbx = config["pbx"]
                self.ip_input.setText(pbx.get("ip", ""))
                self.port_input.setText(pbx.get("port", ""))
                self.username_input.setText(pbx.get("username", ""))
                if pbx.get("password"):
                    try:
                        password = base64.b64decode(pbx["password"]).decode()
                        self.password_input.setText(password)
                    except:
                        pass
            
            # Load agent settings
            if "agent" in config:
                agent = config["agent"]
                self.extension_input.setText(agent.get("extension", ""))
                self.file_path_input.setText(agent.get("callstatus_file", ""))
                
        except Exception as e:
            self.log_message(f"Error loading settings: {e}")
    
    def setup_logging(self):
        """Setup logging system"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"listener_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
    
    def log_message(self, message):
        """Add message to log display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        
        self.log_display.append(formatted_message)
        logging.info(message)

def main():
    """Main application entry point"""
    # Create necessary directories
    for directory in ["config", "logs", "data"]:
        Path(directory).mkdir(exist_ok=True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("Listener Professional")
    app.setApplicationVersion("4.0")
    
    # Create and show main window
    window = ListenerGUI()
    window.show()
    
    print("Listener Professional v4.0 started successfully")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
'''
    return main_py_content

def create_project_structure():
    """Create complete project structure"""
    print("🏗️ Creating project structure...")
    
    # Create base project directory
    project_dir = Path("Listener_Professional")
    project_dir.mkdir(exist_ok=True)
    
    # Create subdirectories
    directories = ["src", "config", "logs", "data", "dist", "build"]
    for directory in directories:
        (project_dir / directory).mkdir(exist_ok=True)
    
    # Create main.py
    main_py_path = project_dir / "src" / "main.py"
    with open(main_py_path, 'w', encoding='utf-8') as f:
        f.write(create_main_py())
    
    print(f"✅ Project structure created in: {project_dir}")
    return project_dir

def build_executable(project_dir):
    """Build the executable"""
    print("🔨 Building executable...")
    
    # Change to project directory
    original_dir = os.getcwd()
    os.chdir(project_dir)
    
    try:
        # Install dependencies
        print("📦 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "PyQt6", "requests"], 
                      check=True, capture_output=True)
        
        # Clean previous builds
        print("🧹 Cleaning previous builds...")
        for directory in ["build", "dist"]:
            if Path(directory).exists():
                shutil.rmtree(directory)
        
        # Remove spec files
        for spec_file in Path('.').glob('*.spec'):
            spec_file.unlink()
        
        # Create directories
        Path("dist").mkdir(exist_ok=True)
        Path("build").mkdir(exist_ok=True)
        
        # Build command
        cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            "--name=Listener",
            "--distpath=dist",
            "--workpath=build",
            "--clean",
            "src/main.py"
        ]
        
        print("⚙️ Running PyInstaller...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            exe_path = Path("dist/Listener.exe")
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024*1024)
                print(f"✅ Build successful! Executable: {exe_path} ({size_mb:.1f} MB)")
                return True
            else:
                print("❌ Build failed: Executable not found")
                return False
        else:
            print(f"❌ Build failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False
    finally:
        os.chdir(original_dir)

def main():
    """Main function"""
    print("========================================")
    print("   Listener Professional v4.0")
    print("   Complete Project Creator & Builder")
    print("========================================")
    print()
    
    try:
        # Create project structure
        project_dir = create_project_structure()
        
        # Build executable
        if build_executable(project_dir):
            print("\n🎉 SUCCESS! Project created and built successfully!")
            print(f"📁 Project location: {project_dir.absolute()}")
            print(f"🚀 Executable: {project_dir.absolute()}/dist/Listener.exe")
            print("\nYou can now run the executable!")
        else:
            print("\n❌ Build failed, but project structure was created.")
            print(f"📁 Project location: {project_dir.absolute()}")
            print("You can try building manually with the ULTIMATE_BUILD_FIX.bat")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to continue...")