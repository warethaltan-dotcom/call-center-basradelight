#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Listener Professional v4.0 - Setup and Installation Script
Automated setup for development and production environments
"""

import os
import sys
import json
import subprocess
import platform
from pathlib import Path

def print_header():
    """Print setup header"""
    print("=" * 70)
    print("        Listener Professional v4.0 - Setup & Installation")
    print("                    Developed by MiniMax Agent")
    print("=" * 70)
    print()

def check_python_version():
    """Check Python version compatibility"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required")
        print("   Please upgrade Python from: https://www.python.org/downloads/")
        return False
    
    print("✅ Python version is compatible")
    return True

def check_platform():
    """Check platform compatibility"""
    system = platform.system()
    print(f"💻 Platform: {system} {platform.release()}")
    
    if system != "Windows":
        print("⚠️  Warning: This application is designed for Windows")
        print("   Some features may not work on other platforms")
    else:
        print("✅ Platform is fully supported")
    
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        print("✅ pip upgraded successfully")
        
        # Install requirements
        if Path("requirements.txt").exists():
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                          check=True, capture_output=True)
            print("✅ Dependencies installed successfully")
        else:
            # Install essential packages manually
            essential_packages = ["PyQt6", "pyinstaller"]
            for package in essential_packages:
                subprocess.run([sys.executable, "-m", "pip", "install", package], 
                              check=True, capture_output=True)
                print(f"✅ {package} installed")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("   Try running: pip install -r requirements.txt")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        "config",
        "logs", 
        "data",
        "icons",
        "build_tools",
        "installer",
        "docs",
        "dist"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created: {directory}/")
    
    return True

def create_default_config():
    """Create default configuration file"""
    print("\n⚙️ Creating default configuration...")
    
    config_path = Path("config/config.json")
    
    if config_path.exists():
        print("ℹ️  Configuration file already exists, skipping...")
        return True
    
    default_config = {
        "pbx": {
            "ip": "",
            "port": 5038,
            "username": "",
            "password": "",
            "enabled": False
        },
        "agent": {
            "extension": "",
            "callstatus_file": "data/CaCallstatus.dat",
            "auto_clear_delay": 3
        },
        "ui": {
            "theme": "light",
            "window_geometry": "900x700",
            "auto_start": False,
            "minimize_to_tray": True
        },
        "logging": {
            "level": "INFO",
            "max_files": 30,
            "max_size_mb": 10
        }
    }
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4)
        print(f"✅ Configuration created: {config_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to create configuration: {e}")
        return False

def create_callstatus_file():
    """Create empty call status file"""
    print("\n📄 Creating call status file...")
    
    callstatus_path = Path("data/CaCallstatus.dat")
    
    try:
        callstatus_path.touch()
        print(f"✅ Call status file created: {callstatus_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to create call status file: {e}")
        return False

def test_imports():
    """Test if all required modules can be imported"""
    print("\n🧪 Testing imports...")
    
    required_modules = [
        ("PyQt6.QtWidgets", "PyQt6 GUI framework"),
        ("PyQt6.QtCore", "PyQt6 core"),
        ("PyQt6.QtGui", "PyQt6 GUI components")
    ]
    
    optional_modules = [
        ("PIL", "Python Imaging Library (for icon generation)"),
        ("psutil", "System utilities")
    ]
    
    all_required_available = True
    
    for module, description in required_modules:
        try:
            __import__(module)
            print(f"✅ {description}")
        except ImportError:
            print(f"❌ {description} - REQUIRED")
            all_required_available = False
    
    for module, description in optional_modules:
        try:
            __import__(module)
            print(f"✅ {description} (optional)")
        except ImportError:
            print(f"⚠️  {description} (optional) - not available")
    
    return all_required_available

def run_quick_test():
    """Run a quick test of the application"""
    print("\n⚡ Running quick test...")
    
    try:
        # Test if main.py can be imported without errors
        if not Path("src/main.py").exists():
            print("❌ Main application file (src/main.py) not found")
            return False
        
        # Test configuration loading
        if Path("config/config.json").exists():
            with open("config/config.json", 'r', encoding='utf-8') as f:
                json.load(f)
            print("✅ Configuration file is valid JSON")
        
        print("✅ Quick test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return False

def show_next_steps():
    """Show next steps for the user"""
    print("\n" + "=" * 70)
    print("                        SETUP COMPLETE!")
    print("=" * 70)
    print("\n🎉 Listener Professional v4.0 is ready!")
    print("\n📋 Next steps:")
    print("   1. 🚀 Run the application:")
    print("      • Development mode: RUN.bat")
    print("      • Or: python src/main.py")
    print()
    print("   2. ⚙️ Configure the application:")
    print("      • Open PBX Settings tab")
    print("      • Enter your PBX connection details")
    print("      • Configure agent settings")
    print()
    print("   3. 🏗️ Build for production:")
    print("      • Run: build_tools/BUILD.bat")
    print("      • Or: python build_tools/build.py")
    print()
    print("   4. 📚 Read documentation:")
    print("      • docs/README.md")
    print("      • docs/USER_GUIDE.md")
    print()
    print("🎯 Key features:")
    print("   • Professional PyQt6 GUI")
    print("   • Real-time PBX call monitoring")
    print("   • Windows installer generation")
    print("   • System tray integration")
    print("   • Demo mode for testing")
    print("   • Comprehensive logging")
    print()
    print("🆘 Need help?")
    print("   • Check logs/ directory for diagnostic info")
    print("   • Use demo mode if PBX is not available")
    print("   • Review docs/USER_GUIDE.md for detailed instructions")
    print()

def main():
    """Main setup process"""
    print_header()
    
    # Change to script directory
    script_dir = Path(__file__).parent
    if script_dir != Path('.'):
        os.chdir(script_dir)
        print(f"📍 Working directory: {Path.cwd()}")
        print()
    
    success = True
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check platform
    check_platform()
    
    # Install dependencies
    if not install_dependencies():
        success = False
    
    # Create directories
    if not create_directories():
        success = False
    
    # Create configuration
    if not create_default_config():
        success = False
    
    # Create call status file
    if not create_callstatus_file():
        success = False
    
    # Test imports
    if not test_imports():
        success = False
    
    # Run quick test
    if not run_quick_test():
        success = False
    
    if success:
        show_next_steps()
    else:
        print("\n" + "=" * 70)
        print("                      SETUP INCOMPLETE")
        print("=" * 70)
        print("\n❌ Some setup steps failed.")
        print("   Please review the error messages above and try again.")
        print("   You may need to:")
        print("   • Install Python 3.8 or higher")
        print("   • Install required packages manually")
        print("   • Run with administrator privileges")
        print("   • Check your internet connection")
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        input("\nPress Enter to exit...")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Setup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        input("Press Enter to exit...")
        sys.exit(1)