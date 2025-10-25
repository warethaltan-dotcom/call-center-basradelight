#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Listener Professional v4.0 - Complete Windows Application
Developed by MiniMax Agent
"""

import sys
import os
import json
import base64
import socket
import threading
import time
from datetime import datetime
from pathlib import Path

# PyQt6 imports
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QTableWidget,
    QTableWidgetItem, QFileDialog, QMessageBox, QProgressBar, QStatusBar,
    QFrame, QGroupBox, QGridLayout, QCheckBox, QSpinBox, QSplitter,
    QScrollArea, QComboBox, QSystemTrayIcon, QMenu
)
from PyQt6.QtCore import (
    QThread, pyqtSignal, QTimer, QSettings, Qt, QSize, QRect
)
from PyQt6.QtGui import (
    QIcon, QFont, QPixmap, QPalette, QColor, QAction
)

# Configuration manager
class ConfigManager:
    """Manages application configuration and security"""
    
    def __init__(self, app_dir):
        self.app_dir = Path(app_dir)
        self.config_dir = self.app_dir / "config"
        self.config_file = self.config_dir / "config.json"
        self.ensure_directories()
        self.default_config = {
            "pbx": {
                "ip": "",
                "port": 5038,
                "username": "",
                "password": "",
                "enabled": False
            },
            "agent": {
                "extension": "",
                "callstatus_file": str(self.app_dir / "data" / "CaCallstatus.dat"),
                "auto_clear_delay": 3
            },
            "ui": {
                "theme": "light",
                "window_geometry": "800x600",
                "auto_start": False,
                "minimize_to_tray": True
            },
            "logging": {
                "level": "INFO",
                "max_files": 30,
                "max_size_mb": 10
            }
        }
    
    def ensure_directories(self):
        """Create necessary directories"""
        directories = ['config', 'logs', 'data', 'icons']
        for dir_name in directories:
            (self.app_dir / dir_name).mkdir(parents=True, exist_ok=True)
    
    def encrypt_password(self, password):
        """Simple password encryption using base64"""
        if not password:
            return ""
        return base64.b64encode(password.encode()).decode()
    
    def decrypt_password(self, encrypted_password):
        """Decrypt password"""
        if not encrypted_password:
            return ""
        try:
            return base64.b64decode(encrypted_password.encode()).decode()
        except:
            return ""
    
    def load_config(self):
        """Load configuration from file"""
        if not self.config_file.exists():
            return self.default_config.copy()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Merge with defaults to ensure all keys exist
            result = self.default_config.copy()
            result.update(config)
            
            # Decrypt password
            if result['pbx']['password']:
                result['pbx']['password'] = self.decrypt_password(result['pbx']['password'])
            
            return result
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.default_config.copy()
    
    def save_config(self, config):
        """Save configuration to file"""
        try:
            # Encrypt password before saving
            config_to_save = config.copy()
            if config_to_save['pbx']['password']:
                config_to_save['pbx']['password'] = self.encrypt_password(config_to_save['pbx']['password'])
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

# AMI Listener Thread
class AMIListenerThread(QThread):
    """AMI Listener running in separate thread"""
    
    status_changed = pyqtSignal(str)
    call_event = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.running = False
        self.socket = None
        self.clear_timer = None
    
    def run(self):
        """Main listening loop"""
        self.running = True
        self.status_changed.emit("Connecting...")
        
        while self.running:
            try:
                if not self.connect_ami():
                    self.status_changed.emit("Connection Failed - Retrying...")
                    time.sleep(5)
                    continue
                
                self.status_changed.emit("Connected - Listening for calls...")
                self.listen_for_events()
                
            except Exception as e:
                self.error_occurred.emit(f"Listening error: {str(e)}")
                time.sleep(5)
    
    def connect_ami(self):
        """Connect to AMI interface"""
        try:
            if not self.config['pbx']['enabled'] or not self.config['pbx']['ip']:
                self.status_changed.emit("PBX not configured - Running in demo mode")
                time.sleep(2)
                # Generate demo events for testing
                self.generate_demo_events()
                return False
            
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)
            self.socket.connect((self.config['pbx']['ip'], self.config['pbx']['port']))
            
            # Login to AMI
            login_cmd = (
                f"Action: Login\\r\\n"
                f"Username: {self.config['pbx']['username']}\\r\\n"
                f"Secret: {self.config['pbx']['password']}\\r\\n"
                f"Events: on\\r\\n\\r\\n"
            )
            self.socket.send(login_cmd.encode())
            
            response = self.socket.recv(1024).decode()
            if "Authentication accepted" in response:
                return True
            else:
                self.error_occurred.emit("AMI Authentication failed")
                return False
                
        except Exception as e:
            self.error_occurred.emit(f"Connection failed: {str(e)}")
            return False
    
    def listen_for_events(self):
        """Listen for AMI events"""
        buffer = ""
        
        while self.running and self.socket:
            try:
                data = self.socket.recv(4096).decode(errors='ignore')
                if not data:
                    break
                
                buffer += data
                
                # Process complete events
                while "\\r\\n\\r\\n" in buffer:
                    event, buffer = buffer.split("\\r\\n\\r\\n", 1)
                    self.process_event(event)
                    
            except socket.timeout:
                continue
            except Exception as e:
                self.error_occurred.emit(f"Event processing error: {str(e)}")
                break
    
    def process_event(self, event_text):
        """Process AMI event"""
        lines = event_text.strip().split("\\r\\n")
        event_data = {}
        
        for line in lines:
            if ": " in line:
                key, value = line.split(": ", 1)
                event_data[key.strip()] = value.strip()
        
        event_type = event_data.get("Event", "")
        
        # Handle specific events
        if event_type in ["DialBegin", "Hangup", "Bridge"]:
            call_info = {
                'event': event_type,
                'caller_id': event_data.get('CallerIDNum', ''),
                'destination': event_data.get('DestCallerIDNum', ''),
                'channel': event_data.get('Channel', ''),
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'uniqueid': event_data.get('Uniqueid', '')
            }
            
            # Check if this concerns our extension
            target_ext = self.config['agent']['extension']
            if target_ext and (
                call_info['destination'] == target_ext or
                call_info['caller_id'] == target_ext or
                target_ext in call_info['channel']
            ):
                self.call_event.emit(call_info)
                self.update_call_status_file(call_info)
    
    def generate_demo_events(self):
        """Generate demo events for testing when PBX is not configured"""
        import random
        
        while self.running:
            time.sleep(random.randint(10, 30))  # Random interval
            
            if not self.running:
                break
            
            # Generate random call event
            events = ["DialBegin", "Hangup"]
            event_type = random.choice(events)
            
            call_info = {
                'event': event_type,
                'caller_id': f"0{random.randint(100000000, 999999999)}",
                'destination': self.config['agent']['extension'] or "100",
                'channel': f"SIP/trunk-{random.randint(1000, 9999)}",
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'uniqueid': str(random.randint(1000000, 9999999))
            }
            
            self.call_event.emit(call_info)
            self.update_call_status_file(call_info)
    
    def update_call_status_file(self, call_info):
        """Update CaCallstatus.dat file"""
        try:
            callstatus_file = self.config['agent']['callstatus_file']
            
            if call_info['event'] == "DialBegin":
                # Incoming call - write call data
                xml_content = f"""<CRM>
    <callRecord>
        <CallerID>{call_info['caller_id']}</CallerID>
        <DDI>{call_info['destination']}</DDI>
        <Date>{datetime.now().strftime('%d-%m-%Y')}</Date>
        <Time>{datetime.now().strftime('%H:%M:%S')}</Time>
    </callRecord>
</CRM>"""
                
                with open(callstatus_file, 'w', encoding='utf-8') as f:
                    f.write(xml_content)
                
                # Set timer to clear file after delay
                if self.clear_timer:
                    self.clear_timer.cancel()
                
                self.clear_timer = threading.Timer(
                    self.config['agent']['auto_clear_delay'],
                    self.clear_call_status_file
                )
                self.clear_timer.start()
                
            elif call_info['event'] == "Hangup":
                # Call ended - clear immediately
                self.clear_call_status_file()
                
        except Exception as e:
            self.error_occurred.emit(f"Error updating call status file: {str(e)}")
    
    def clear_call_status_file(self):
        """Clear call status file"""
        try:
            callstatus_file = self.config['agent']['callstatus_file']
            with open(callstatus_file, 'w', encoding='utf-8') as f:
                f.write("")  # Clear file
        except Exception as e:
            self.error_occurred.emit(f"Error clearing call status file: {str(e)}")
    
    def stop(self):
        """Stop the listener"""
        self.running = False
        
        if self.clear_timer:
            self.clear_timer.cancel()
        
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        
        self.quit()
        self.wait()

# Main Application Window
class ListenerMainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Get application directory
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            self.app_dir = Path(sys.executable).parent
        else:
            # Running as script
            self.app_dir = Path(__file__).parent.parent
        
        # Initialize config manager
        self.config_manager = ConfigManager(self.app_dir)
        self.config = self.config_manager.load_config()
        
        # Initialize variables
        self.ami_thread = None
        self.call_history = []
        
        # Setup UI
        self.init_ui()
        self.load_window_geometry()
        
        # Setup system tray
        self.setup_system_tray()
        
        # Setup auto-save timer
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.save_config)
        self.auto_save_timer.start(30000)  # Save every 30 seconds
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("Listener Professional v4.0")
        self.setMinimumSize(900, 700)
        
        # Set window icon (will be created later)
        self.setWindowIcon(QIcon())
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Create tabs
        self.create_login_tab()
        self.create_agent_tab()
        self.create_control_tab()
        self.create_logs_tab()
        self.create_settings_tab()
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Apply styling
        self.apply_styling()
    
    def create_login_tab(self):
        """Create PBX login/settings tab"""
        tab = QWidget()
        self.tab_widget.addTab(tab, "🌐 PBX Settings")
        
        layout = QVBoxLayout(tab)
        
        # PBX Connection Group
        pbx_group = QGroupBox("PBX Connection Settings")
        pbx_layout = QGridLayout(pbx_group)
        
        # Enable PBX checkbox
        self.pbx_enabled_cb = QCheckBox("Enable PBX Connection")
        self.pbx_enabled_cb.setChecked(self.config['pbx']['enabled'])
        self.pbx_enabled_cb.toggled.connect(self.on_pbx_enabled_changed)
        pbx_layout.addWidget(self.pbx_enabled_cb, 0, 0, 1, 2)
        
        # PBX IP
        pbx_layout.addWidget(QLabel("PBX IP Address:"), 1, 0)
        self.pbx_ip_edit = QLineEdit(self.config['pbx']['ip'])
        self.pbx_ip_edit.setPlaceholderText("e.g., 192.168.1.100")
        pbx_layout.addWidget(self.pbx_ip_edit, 1, 1)
        
        # PBX Port
        pbx_layout.addWidget(QLabel("PBX Port:"), 2, 0)
        self.pbx_port_spin = QSpinBox()
        self.pbx_port_spin.setRange(1, 65535)
        self.pbx_port_spin.setValue(self.config['pbx']['port'])
        pbx_layout.addWidget(self.pbx_port_spin, 2, 1)
        
        # Username
        pbx_layout.addWidget(QLabel("Username:"), 3, 0)
        self.pbx_username_edit = QLineEdit(self.config['pbx']['username'])
        self.pbx_username_edit.setPlaceholderText("AMI Username")
        pbx_layout.addWidget(self.pbx_username_edit, 3, 1)
        
        # Password
        pbx_layout.addWidget(QLabel("Password:"), 4, 0)
        self.pbx_password_edit = QLineEdit(self.config['pbx']['password'])
        self.pbx_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.pbx_password_edit.setPlaceholderText("AMI Password")
        pbx_layout.addWidget(self.pbx_password_edit, 4, 1)
        
        # Test connection button
        self.test_conn_btn = QPushButton("🔗 Test Connection")
        self.test_conn_btn.clicked.connect(self.test_pbx_connection)
        pbx_layout.addWidget(self.test_conn_btn, 5, 0, 1, 2)
        
        layout.addWidget(pbx_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 Save Settings")
        save_btn.clicked.connect(self.save_pbx_settings)
        btn_layout.addWidget(save_btn)
        
        reset_btn = QPushButton("🔄 Reset to Defaults")
        reset_btn.clicked.connect(self.reset_pbx_settings)
        btn_layout.addWidget(reset_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Info text
        info_text = QTextEdit()
        info_text.setMaximumHeight(100)
        info_text.setReadOnly(True)
        info_text.setHtml(
            "<b>ℹ️ Information:</b><br>"
            "• PBX connection is optional - the application works without it<br>"
            "• When disabled, demo mode generates sample call events<br>"
            "• All settings are automatically saved and encrypted"
        )
        layout.addWidget(info_text)
        
        layout.addStretch()
        
        # Update enabled state
        self.on_pbx_enabled_changed()
    
    def create_agent_tab(self):
        """Create agent settings tab"""
        tab = QWidget()
        self.tab_widget.addTab(tab, "👤 Agent Settings")
        
        layout = QVBoxLayout(tab)
        
        # Agent Settings Group
        agent_group = QGroupBox("Agent Configuration")
        agent_layout = QGridLayout(agent_group)
        
        # Extension
        agent_layout.addWidget(QLabel("Extension Number:"), 0, 0)
        self.extension_edit = QLineEdit(self.config['agent']['extension'])
        self.extension_edit.setPlaceholderText("e.g., 100, 101, 102...")
        agent_layout.addWidget(self.extension_edit, 0, 1)
        
        # Call Status File
        agent_layout.addWidget(QLabel("Call Status File:"), 1, 0)
        file_layout = QHBoxLayout()
        
        self.callstatus_path_edit = QLineEdit(self.config['agent']['callstatus_file'])
        self.callstatus_path_edit.setReadOnly(True)
        file_layout.addWidget(self.callstatus_path_edit)
        
        browse_btn = QPushButton("📁 Browse")
        browse_btn.clicked.connect(self.browse_callstatus_file)
        file_layout.addWidget(browse_btn)
        
        agent_layout.addLayout(file_layout, 1, 1)
        
        # Auto-clear delay
        agent_layout.addWidget(QLabel("Auto-clear delay (seconds):"), 2, 0)
        self.auto_clear_spin = QSpinBox()
        self.auto_clear_spin.setRange(1, 60)
        self.auto_clear_spin.setValue(self.config['agent']['auto_clear_delay'])
        agent_layout.addWidget(self.auto_clear_spin, 2, 1)
        
        layout.addWidget(agent_group)
        
        # File Preview Group
        preview_group = QGroupBox("Call Status File Preview")
        preview_layout = QVBoxLayout(preview_group)
        
        self.file_preview = QTextEdit()
        self.file_preview.setMaximumHeight(150)
        self.file_preview.setReadOnly(True)
        self.file_preview.setPlaceholderText("File content will appear here...")
        preview_layout.addWidget(self.file_preview)
        
        # Refresh preview button
        refresh_btn = QPushButton("🔄 Refresh Preview")
        refresh_btn.clicked.connect(self.refresh_file_preview)
        preview_layout.addWidget(refresh_btn)
        
        layout.addWidget(preview_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 Save Agent Settings")
        save_btn.clicked.connect(self.save_agent_settings)
        btn_layout.addWidget(save_btn)
        
        create_file_btn = QPushButton("📄 Create Default File")
        create_file_btn.clicked.connect(self.create_default_callstatus_file)
        btn_layout.addWidget(create_file_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        layout.addStretch()
        
        # Load initial preview
        self.refresh_file_preview()
    
    def create_control_tab(self):
        """Create control panel tab"""
        tab = QWidget()
        self.tab_widget.addTab(tab, "🎛️ Control Panel")
        
        layout = QVBoxLayout(tab)
        
        # Control buttons
        control_group = QGroupBox("Listener Control")
        control_layout = QVBoxLayout(control_group)
        
        btn_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("▶️ Start Listener")
        self.start_btn.clicked.connect(self.start_listener)
        self.start_btn.setMinimumHeight(50)
        btn_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹️ Stop Listener")
        self.stop_btn.clicked.connect(self.stop_listener)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setMinimumHeight(50)
        btn_layout.addWidget(self.stop_btn)
        
        control_layout.addLayout(btn_layout)
        
        # Status display
        self.status_label = QLabel("Status: Ready to start")
        self.status_label.setStyleSheet("font-weight: bold; font-size: 14px; color: blue;")
        control_layout.addWidget(self.status_label)
        
        layout.addWidget(control_group)
        
        # Call History Table
        history_group = QGroupBox("Call History")
        history_layout = QVBoxLayout(history_group)
        
        # Table
        self.call_table = QTableWidget()
        self.call_table.setColumnCount(5)
        self.call_table.setHorizontalHeaderLabels([
            "Time", "Event", "Caller ID", "Destination", "Channel"
        ])
        
        # Set column widths
        header = self.call_table.horizontalHeader()
        header.setStretchLastSection(True)
        
        history_layout.addWidget(self.call_table)
        
        # Table controls
        table_btn_layout = QHBoxLayout()
        
        clear_table_btn = QPushButton("🗑️ Clear History")
        clear_table_btn.clicked.connect(self.clear_call_history)
        table_btn_layout.addWidget(clear_table_btn)
        
        export_btn = QPushButton("📤 Export to CSV")
        export_btn.clicked.connect(self.export_call_history)
        table_btn_layout.addWidget(export_btn)
        
        table_btn_layout.addStretch()
        history_layout.addLayout(table_btn_layout)
        
        layout.addWidget(history_group)
    
    def create_logs_tab(self):
        """Create logs tab"""
        tab = QWidget()
        self.tab_widget.addTab(tab, "📋 Logs")
        
        layout = QVBoxLayout(tab)
        
        # Log display
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setFont(QFont("Consolas", 9))
        layout.addWidget(self.log_display)
        
        # Log controls
        log_btn_layout = QHBoxLayout()
        
        clear_logs_btn = QPushButton("🗑️ Clear Logs")
        clear_logs_btn.clicked.connect(self.clear_logs)
        log_btn_layout.addWidget(clear_logs_btn)
        
        save_logs_btn = QPushButton("💾 Save Logs")
        save_logs_btn.clicked.connect(self.save_logs)
        log_btn_layout.addWidget(save_logs_btn)
        
        auto_scroll_cb = QCheckBox("Auto-scroll")
        auto_scroll_cb.setChecked(True)
        self.auto_scroll_logs = auto_scroll_cb.isChecked()
        auto_scroll_cb.toggled.connect(lambda checked: setattr(self, 'auto_scroll_logs', checked))
        log_btn_layout.addWidget(auto_scroll_cb)
        
        log_btn_layout.addStretch()
        layout.addLayout(log_btn_layout)
        
        # Add initial log entry
        self.add_log_entry("Application started")
    
    def create_settings_tab(self):
        """Create general settings tab"""
        tab = QWidget()
        self.tab_widget.addTab(tab, "⚙️ Settings")
        
        layout = QVBoxLayout(tab)
        
        # UI Settings
        ui_group = QGroupBox("User Interface")
        ui_layout = QGridLayout(ui_group)
        
        # Theme selection
        ui_layout.addWidget(QLabel("Theme:"), 0, 0)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        self.theme_combo.setCurrentText(self.config['ui']['theme'].title())
        ui_layout.addWidget(self.theme_combo, 0, 1)
        
        # Auto-start
        self.auto_start_cb = QCheckBox("Start listener automatically")
        self.auto_start_cb.setChecked(self.config['ui']['auto_start'])
        ui_layout.addWidget(self.auto_start_cb, 1, 0, 1, 2)
        
        # Minimize to tray
        self.minimize_tray_cb = QCheckBox("Minimize to system tray")
        self.minimize_tray_cb.setChecked(self.config['ui']['minimize_to_tray'])
        ui_layout.addWidget(self.minimize_tray_cb, 2, 0, 1, 2)
        
        layout.addWidget(ui_group)
        
        # Logging Settings
        logging_group = QGroupBox("Logging")
        logging_layout = QGridLayout(logging_group)
        
        # Log level
        logging_layout.addWidget(QLabel("Log Level:"), 0, 0)
        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        self.log_level_combo.setCurrentText(self.config['logging']['level'])
        logging_layout.addWidget(self.log_level_combo, 0, 1)
        
        # Max log files
        logging_layout.addWidget(QLabel("Max log files:"), 1, 0)
        self.max_files_spin = QSpinBox()
        self.max_files_spin.setRange(1, 100)
        self.max_files_spin.setValue(self.config['logging']['max_files'])
        logging_layout.addWidget(self.max_files_spin, 1, 1)
        
        layout.addWidget(logging_group)
        
        # About section
        about_group = QGroupBox("About")
        about_layout = QVBoxLayout(about_group)
        
        about_text = QLabel(
            "<h3>Listener Professional v4.0</h3>"
            "<p>Professional PBX call monitoring application</p>"
            "<p>Developed by MiniMax Agent</p>"
            "<p>Built with PyQt6 and Python</p>"
        )
        about_text.setWordWrap(True)
        about_layout.addWidget(about_text)
        
        layout.addWidget(about_group)
        
        # Settings buttons
        settings_btn_layout = QHBoxLayout()
        
        save_settings_btn = QPushButton("💾 Save All Settings")
        save_settings_btn.clicked.connect(self.save_all_settings)
        settings_btn_layout.addWidget(save_settings_btn)
        
        reset_settings_btn = QPushButton("🔄 Reset All Settings")
        reset_settings_btn.clicked.connect(self.reset_all_settings)
        settings_btn_layout.addWidget(reset_settings_btn)
        
        settings_btn_layout.addStretch()
        layout.addLayout(settings_btn_layout)
        
        layout.addStretch()
    
    def apply_styling(self):
        """Apply custom styling to the application"""
        style = """
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #c0c0c0;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 1px solid white;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QLineEdit, QSpinBox, QComboBox {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
            QTextEdit {
                border: 1px solid #ccc;
                border-radius: 3px;
            }
        """
        self.setStyleSheet(style)
    
    def setup_system_tray(self):
        """Setup system tray icon and menu"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return
        
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon())  # Will set proper icon later
        
        # Tray menu
        tray_menu = QMenu()
        
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        # Handle tray icon clicks
        self.tray_icon.activated.connect(self.tray_icon_activated)
    
    def tray_icon_activated(self, reason):
        """Handle system tray icon activation"""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            if self.isVisible():
                self.hide()
            else:
                self.show()
                self.raise_()
                self.activateWindow()
    
    # Event handlers
    def on_pbx_enabled_changed(self):
        """Handle PBX enabled checkbox change"""
        enabled = self.pbx_enabled_cb.isChecked()
        
        self.pbx_ip_edit.setEnabled(enabled)
        self.pbx_port_spin.setEnabled(enabled)
        self.pbx_username_edit.setEnabled(enabled)
        self.pbx_password_edit.setEnabled(enabled)
        self.test_conn_btn.setEnabled(enabled)
    
    def test_pbx_connection(self):
        """Test PBX connection"""
        if not self.pbx_enabled_cb.isChecked():
            return
        
        host = self.pbx_ip_edit.text().strip()
        port = self.pbx_port_spin.value()
        username = self.pbx_username_edit.text().strip()
        password = self.pbx_password_edit.text()
        
        if not all([host, username, password]):
            QMessageBox.warning(self, "Warning", "Please fill in all connection details")
            return
        
        # Test connection in separate thread
        self.test_conn_btn.setEnabled(False)
        self.test_conn_btn.setText("Testing...")
        
        def test_connection():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((host, port))
                
                # Try to login
                login_cmd = f"Action: Login\\r\\nUsername: {username}\\r\\nSecret: {password}\\r\\n\\r\\n"
                sock.send(login_cmd.encode())
                
                response = sock.recv(1024).decode()
                sock.close()
                
                return "Authentication accepted" in response
                
            except Exception as e:
                return str(e)
        
        def on_test_complete(result):
            self.test_conn_btn.setEnabled(True)
            self.test_conn_btn.setText("🔗 Test Connection")
            
            if result is True:
                QMessageBox.information(self, "Success", "Connection successful!")
                self.add_log_entry("PBX connection test successful")
            else:
                error_msg = str(result) if isinstance(result, str) else "Authentication failed"
                QMessageBox.warning(self, "Connection Failed", f"Failed to connect: {error_msg}")
                self.add_log_entry(f"PBX connection test failed: {error_msg}")
        
        # Run test in thread to avoid blocking UI
        threading.Thread(
            target=lambda: on_test_complete(test_connection()),
            daemon=True
        ).start()
    
    def save_pbx_settings(self):
        """Save PBX settings"""
        self.config['pbx']['enabled'] = self.pbx_enabled_cb.isChecked()
        self.config['pbx']['ip'] = self.pbx_ip_edit.text().strip()
        self.config['pbx']['port'] = self.pbx_port_spin.value()
        self.config['pbx']['username'] = self.pbx_username_edit.text().strip()
        self.config['pbx']['password'] = self.pbx_password_edit.text()
        
        if self.config_manager.save_config(self.config):
            QMessageBox.information(self, "Success", "PBX settings saved successfully!")
            self.add_log_entry("PBX settings saved")
        else:
            QMessageBox.warning(self, "Error", "Failed to save PBX settings")
    
    def reset_pbx_settings(self):
        """Reset PBX settings to defaults"""
        if QMessageBox.question(
            self, "Confirm Reset", 
            "Reset PBX settings to defaults?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            
            defaults = self.config_manager.default_config['pbx']
            
            self.pbx_enabled_cb.setChecked(defaults['enabled'])
            self.pbx_ip_edit.setText(defaults['ip'])
            self.pbx_port_spin.setValue(defaults['port'])
            self.pbx_username_edit.setText(defaults['username'])
            self.pbx_password_edit.setText(defaults['password'])
            
            self.add_log_entry("PBX settings reset to defaults")
    
    def browse_callstatus_file(self):
        """Browse for call status file location"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Choose Call Status File Location",
            self.callstatus_path_edit.text() or str(self.app_dir / "data" / "CaCallstatus.dat"),
            "Data Files (*.dat);;All Files (*)"
        )
        
        if filename:
            self.callstatus_path_edit.setText(filename)
            self.add_log_entry(f"Call status file path set to: {filename}")
    
    def refresh_file_preview(self):
        """Refresh call status file preview"""
        filepath = self.callstatus_path_edit.text()
        
        if not filepath or not os.path.exists(filepath):
            self.file_preview.setText("File does not exist or path not set")
            return
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if content.strip():
                self.file_preview.setText(content)
            else:
                self.file_preview.setText("File is empty (ready for next call)")
                
        except Exception as e:
            self.file_preview.setText(f"Error reading file: {str(e)}")
    
    def save_agent_settings(self):
        """Save agent settings"""
        self.config['agent']['extension'] = self.extension_edit.text().strip()
        self.config['agent']['callstatus_file'] = self.callstatus_path_edit.text()
        self.config['agent']['auto_clear_delay'] = self.auto_clear_spin.value()
        
        if self.config_manager.save_config(self.config):
            QMessageBox.information(self, "Success", "Agent settings saved successfully!")
            self.add_log_entry("Agent settings saved")
        else:
            QMessageBox.warning(self, "Error", "Failed to save agent settings")
    
    def create_default_callstatus_file(self):
        """Create default call status file"""
        filepath = self.callstatus_path_edit.text()
        
        if not filepath:
            QMessageBox.warning(self, "Warning", "Please select a file path first")
            return
        
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Create empty file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("")
            
            QMessageBox.information(self, "Success", f"Created file: {filepath}")
            self.add_log_entry(f"Created call status file: {filepath}")
            self.refresh_file_preview()
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to create file: {str(e)}")
    
    def start_listener(self):
        """Start the AMI listener"""
        if self.ami_thread and self.ami_thread.isRunning():
            return
        
        # Save current settings
        self.save_config()
        
        # Create and start AMI thread
        self.ami_thread = AMIListenerThread(self.config)
        self.ami_thread.status_changed.connect(self.on_listener_status_changed)
        self.ami_thread.call_event.connect(self.on_call_event)
        self.ami_thread.error_occurred.connect(self.on_listener_error)
        
        self.ami_thread.start()
        
        # Update UI
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        
        self.add_log_entry("AMI Listener started")
    
    def stop_listener(self):
        """Stop the AMI listener"""
        if self.ami_thread:
            self.ami_thread.stop()
            self.ami_thread = None
        
        # Update UI
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText("Status: Stopped")
        self.status_bar.showMessage("Listener stopped")
        
        self.add_log_entry("AMI Listener stopped")
    
    def on_listener_status_changed(self, status):
        """Handle listener status change"""
        self.status_label.setText(f"Status: {status}")
        self.status_bar.showMessage(status)
        self.add_log_entry(f"Listener status: {status}")
    
    def on_call_event(self, call_info):
        """Handle incoming call event"""
        # Add to call history table
        row_position = self.call_table.rowCount()
        self.call_table.insertRow(row_position)
        
        self.call_table.setItem(row_position, 0, QTableWidgetItem(call_info['timestamp']))
        self.call_table.setItem(row_position, 1, QTableWidgetItem(call_info['event']))
        self.call_table.setItem(row_position, 2, QTableWidgetItem(call_info['caller_id']))
        self.call_table.setItem(row_position, 3, QTableWidgetItem(call_info['destination']))
        self.call_table.setItem(row_position, 4, QTableWidgetItem(call_info['channel']))
        
        # Scroll to bottom
        self.call_table.scrollToBottom()
        
        # Add to call history list
        self.call_history.append(call_info)
        
        # Log the event
        self.add_log_entry(
            f"Call event: {call_info['event']} | "
            f"From: {call_info['caller_id']} | "
            f"To: {call_info['destination']}"
        )
        
        # Refresh file preview if on agent tab
        if self.tab_widget.currentIndex() == 1:  # Agent tab
            self.refresh_file_preview()
    
    def on_listener_error(self, error_msg):
        """Handle listener error"""
        self.add_log_entry(f"ERROR: {error_msg}")
        
        # Show error in status
        self.status_label.setText(f"Status: Error - {error_msg}")
        self.status_bar.showMessage(f"Error: {error_msg}")
    
    def clear_call_history(self):
        """Clear call history table"""
        if QMessageBox.question(
            self, "Confirm Clear",
            "Clear all call history?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            
            self.call_table.setRowCount(0)
            self.call_history.clear()
            self.add_log_entry("Call history cleared")
    
    def export_call_history(self):
        """Export call history to CSV"""
        if not self.call_history:
            QMessageBox.information(self, "Info", "No call history to export")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Call History",
            f"call_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    import csv
                    writer = csv.writer(f)
                    
                    # Write header
                    writer.writerow(['Timestamp', 'Event', 'Caller ID', 'Destination', 'Channel', 'Unique ID'])
                    
                    # Write data
                    for call in self.call_history:
                        writer.writerow([
                            call['timestamp'],
                            call['event'],
                            call['caller_id'],
                            call['destination'],
                            call['channel'],
                            call['uniqueid']
                        ])
                
                QMessageBox.information(self, "Success", f"Call history exported to: {filename}")
                self.add_log_entry(f"Call history exported to: {filename}")
                
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to export: {str(e)}")
    
    def add_log_entry(self, message):
        """Add entry to log display"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        self.log_display.append(log_entry)
        
        if self.auto_scroll_logs:
            cursor = self.log_display.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            self.log_display.setTextCursor(cursor)
    
    def clear_logs(self):
        """Clear log display"""
        if QMessageBox.question(
            self, "Confirm Clear",
            "Clear all logs?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            
            self.log_display.clear()
            self.add_log_entry("Logs cleared")
    
    def save_logs(self):
        """Save logs to file"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Logs",
            f"listener_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.log_display.toPlainText())
                
                QMessageBox.information(self, "Success", f"Logs saved to: {filename}")
                self.add_log_entry(f"Logs saved to: {filename}")
                
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save logs: {str(e)}")
    
    def save_all_settings(self):
        """Save all settings from UI to config"""
        # UI settings
        self.config['ui']['theme'] = self.theme_combo.currentText().lower()
        self.config['ui']['auto_start'] = self.auto_start_cb.isChecked()
        self.config['ui']['minimize_to_tray'] = self.minimize_tray_cb.isChecked()
        
        # Logging settings
        self.config['logging']['level'] = self.log_level_combo.currentText()
        self.config['logging']['max_files'] = self.max_files_spin.value()
        
        if self.config_manager.save_config(self.config):
            QMessageBox.information(self, "Success", "All settings saved successfully!")
            self.add_log_entry("All settings saved")
        else:
            QMessageBox.warning(self, "Error", "Failed to save settings")
    
    def reset_all_settings(self):
        """Reset all settings to defaults"""
        if QMessageBox.question(
            self, "Confirm Reset",
            "Reset ALL settings to defaults? This will clear all your configurations.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            
            self.config = self.config_manager.default_config.copy()
            self.load_settings_to_ui()
            
            QMessageBox.information(self, "Reset Complete", "All settings have been reset to defaults")
            self.add_log_entry("All settings reset to defaults")
    
    def load_settings_to_ui(self):
        """Load settings from config to UI elements"""
        # PBX settings
        self.pbx_enabled_cb.setChecked(self.config['pbx']['enabled'])
        self.pbx_ip_edit.setText(self.config['pbx']['ip'])
        self.pbx_port_spin.setValue(self.config['pbx']['port'])
        self.pbx_username_edit.setText(self.config['pbx']['username'])
        self.pbx_password_edit.setText(self.config['pbx']['password'])
        
        # Agent settings
        self.extension_edit.setText(self.config['agent']['extension'])
        self.callstatus_path_edit.setText(self.config['agent']['callstatus_file'])
        self.auto_clear_spin.setValue(self.config['agent']['auto_clear_delay'])
        
        # UI settings
        self.theme_combo.setCurrentText(self.config['ui']['theme'].title())
        self.auto_start_cb.setChecked(self.config['ui']['auto_start'])
        self.minimize_tray_cb.setChecked(self.config['ui']['minimize_to_tray'])
        
        # Logging settings
        self.log_level_combo.setCurrentText(self.config['logging']['level'])
        self.max_files_spin.setValue(self.config['logging']['max_files'])
        
        self.on_pbx_enabled_changed()
    
    def save_config(self):
        """Save current configuration"""
        # Collect all settings from UI
        self.config['pbx']['enabled'] = self.pbx_enabled_cb.isChecked()
        self.config['pbx']['ip'] = self.pbx_ip_edit.text().strip()
        self.config['pbx']['port'] = self.pbx_port_spin.value()
        self.config['pbx']['username'] = self.pbx_username_edit.text().strip()
        self.config['pbx']['password'] = self.pbx_password_edit.text()
        
        self.config['agent']['extension'] = self.extension_edit.text().strip()
        self.config['agent']['callstatus_file'] = self.callstatus_path_edit.text()
        self.config['agent']['auto_clear_delay'] = self.auto_clear_spin.value()
        
        # Save window geometry
        geometry = self.geometry()
        self.config['ui']['window_geometry'] = f"{geometry.width()}x{geometry.height()}"
        
        self.config_manager.save_config(self.config)
    
    def load_window_geometry(self):
        """Load and apply window geometry"""
        geometry_str = self.config['ui'].get('window_geometry', '900x700')
        try:
            width, height = map(int, geometry_str.split('x'))
            self.resize(width, height)
        except:
            self.resize(900, 700)
    
    def closeEvent(self, event):
        """Handle application close event"""
        if self.config['ui']['minimize_to_tray'] and hasattr(self, 'tray_icon'):
            event.ignore()
            self.hide()
            return
        
        # Stop listener if running
        if self.ami_thread:
            self.ami_thread.stop()
        
        # Save configuration
        self.save_config()
        
        event.accept()

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Listener Professional")
    app.setApplicationVersion("4.0")
    app.setOrganizationName("MiniMax Agent")
    
    # Set application icon (will be added later)
    app.setWindowIcon(QIcon())
    
    # Create and show main window
    window = ListenerMainWindow()
    window.show()
    
    # Auto-start listener if configured
    if window.config['ui']['auto_start']:
        QTimer.singleShot(1000, window.start_listener)
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()