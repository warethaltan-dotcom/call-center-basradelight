#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Listener Professional v4.0 - Development Tools
Utilities for development and testing
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are available"""
    required_packages = [
        'PyQt6',
        'pyinstaller',
    ]
    
    optional_packages = [
        'PIL',  # For icon generation
        'psutil',  # For system monitoring
    ]
    
    print("🔍 Checking dependencies...")
    
    missing_required = []
    missing_optional = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            missing_required.append(package)
            print(f"  ❌ {package} (REQUIRED)")
    
    for package in optional_packages:
        try:
            __import__(package)
            print(f"  ✅ {package} (optional)")
        except ImportError:
            missing_optional.append(package)
            print(f"  ⚠️  {package} (optional)")
    
    if missing_required:
        print(f"\n❌ Missing required packages: {', '.join(missing_required)}")
        print("   Install with: pip install " + ' '.join(missing_required))
        return False
    
    if missing_optional:
        print(f"\n⚠️  Missing optional packages: {', '.join(missing_optional)}")
        print("   Install with: pip install " + ' '.join(missing_optional))
    
    print("\n✅ All required dependencies are available")
    return True

def validate_config():
    """Validate configuration file"""
    config_path = Path('config/config.json')
    
    if not config_path.exists():
        print("❌ Configuration file not found")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        required_sections = ['pbx', 'agent', 'ui', 'logging']
        
        for section in required_sections:
            if section not in config:
                print(f"❌ Missing configuration section: {section}")
                return False
            print(f"✅ Configuration section: {section}")
        
        print("\n✅ Configuration file is valid")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in configuration file: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading configuration: {e}")
        return False

def test_application():
    """Run basic application tests"""
    print("🧪 Testing application...")
    
    # Check if main.py exists and is valid Python
    main_path = Path('src/main.py')
    if not main_path.exists():
        print("❌ Main application file not found")
        return False
    
    # Try to compile the main file
    try:
        with open(main_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        compile(source, str(main_path), 'exec')
        print("✅ Main application file compiles successfully")
        
    except SyntaxError as e:
        print(f"❌ Syntax error in main application: {e}")
        return False
    except Exception as e:
        print(f"❌ Error compiling main application: {e}")
        return False
    
    print("\n✅ Basic application tests passed")
    return True

def create_development_config():
    """Create development configuration with demo settings"""
    dev_config = {
        "pbx": {
            "ip": "127.0.0.1",
            "port": 5038,
            "username": "admin",
            "password": "admin",
            "enabled": False  # Start in demo mode for development
        },
        "agent": {
            "extension": "100",
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
            "level": "DEBUG",  # More verbose for development
            "max_files": 10,
            "max_size_mb": 5
        }
    }
    
    config_path = Path('config/config_dev.json')
    config_path.parent.mkdir(exist_ok=True)
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(dev_config, f, indent=4)
    
    print(f"✅ Created development configuration: {config_path}")
    return str(config_path)

def clean_development_files():
    """Clean development and build artifacts"""
    print("🧹 Cleaning development files...")
    
    patterns_to_clean = [
        '__pycache__',
        '*.pyc',
        '*.pyo',
        'build',
        'dist',
        '*.spec',
        '*.log',
        '.pytest_cache'
    ]
    
    import glob
    import shutil
    
    for pattern in patterns_to_clean:
        for path in glob.glob(pattern, recursive=True):
            path_obj = Path(path)
            try:
                if path_obj.is_dir():
                    shutil.rmtree(path_obj)
                    print(f"  🗑️  Removed directory: {path}")
                else:
                    path_obj.unlink()
                    print(f"  🗑️  Removed file: {path}")
            except Exception as e:
                print(f"  ⚠️  Could not remove {path}: {e}")
    
    print("✅ Development files cleaned")

def run_quick_test():
    """Run a quick test of the application"""
    print("⚡ Running quick test...")
    
    try:
        # Import main modules to check for import errors
        sys.path.insert(0, 'src')
        
        # Test imports
        import main
        print("✅ Main module imports successfully")
        
        # Test configuration manager
        if hasattr(main, 'ConfigManager'):
            config_mgr = main.ConfigManager('.')
            test_config = config_mgr.load_config()
            print("✅ Configuration manager works")
        
        print("\n✅ Quick test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return False
    finally:
        if 'src' in sys.path:
            sys.path.remove('src')

def main():
    """Main development tools menu"""
    print("="*60)
    print("    Listener Professional v4.0 - Development Tools")
    print("="*60)
    
    while True:
        print("\n🛠️  Available tools:")
        print("   1. Check dependencies")
        print("   2. Validate configuration")
        print("   3. Test application")
        print("   4. Create development config")
        print("   5. Clean development files")
        print("   6. Run quick test")
        print("   7. Run full check (all tests)")
        print("   0. Exit")
        
        try:
            choice = input("\nSelect option (0-7): ").strip()
            
            if choice == '0':
                print("👋 Goodbye!")
                break
            elif choice == '1':
                check_dependencies()
            elif choice == '2':
                validate_config()
            elif choice == '3':
                test_application()
            elif choice == '4':
                create_development_config()
            elif choice == '5':
                clean_development_files()
            elif choice == '6':
                run_quick_test()
            elif choice == '7':
                print("🔄 Running full check...")
                all_passed = True
                all_passed &= check_dependencies()
                all_passed &= validate_config()
                all_passed &= test_application()
                all_passed &= run_quick_test()
                
                if all_passed:
                    print("\n🎉 All checks passed! Ready for development.")
                else:
                    print("\n❌ Some checks failed. Please review the issues above.")
            else:
                print("❌ Invalid option. Please try again.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()