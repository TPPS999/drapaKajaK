#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flight Tool - Components Setup Script
Installs and verifies all required components
"""

import subprocess
import sys
import importlib

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*50)
    print(f"  {text}")
    print("="*50)

def print_step(step, total, text):
    """Print step info"""
    print(f"\n[{step}/{total}] {text}")

def is_module_installed(module_name):
    """Check if Python module is installed"""
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

def install_module(module_name):
    """Install Python module using pip"""
    print(f"Installing {module_name}...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", module_name, "--upgrade"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"  ✓ {module_name} installed successfully")
            return True
        else:
            print(f"  ✗ Failed to install {module_name}")
            print(f"    Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  ✗ Timeout installing {module_name}")
        return False
    except Exception as e:
        print(f"  ✗ Error installing {module_name}: {e}")
        return False

def main():
    """Main setup function"""
    
    print_header("FLIGHT TOOL SETUP")
    print("This script will install all required components")
    print("Please wait, this may take several minutes...")
    
    # Required modules mapping
    required_modules = {
        'selenium': 'selenium',
        'webdriver_manager': 'webdriver-manager',
        'requests': 'requests',
        'beautifulsoup4': 'beautifulsoup4', 
        'pandas': 'pandas',
        'openpyxl': 'openpyxl'
    }
    
    print_step(1, 3, "Checking current installation status")
    
    missing_modules = []
    installed_modules = []
    
    for import_name, pip_name in required_modules.items():
        # Handle special import names
        check_import_name = import_name
        if pip_name == 'beautifulsoup4':
            check_import_name = 'bs4'
        elif pip_name == 'webdriver-manager':
            check_import_name = 'webdriver_manager'
        
        if is_module_installed(check_import_name):
            installed_modules.append(pip_name)
            print(f"  ✓ {pip_name} - already installed")
        else:
            missing_modules.append(pip_name)
            print(f"  ✗ {pip_name} - missing")
    
    if not missing_modules:
        print("\n🎉 All components are already installed!")
        return True
    
    print_step(2, 3, f"Installing {len(missing_modules)} missing components")
    print(f"Missing: {', '.join(missing_modules)}")
    
    # Install missing modules
    failed_installations = []
    
    for module in missing_modules:
        if not install_module(module):
            failed_installations.append(module)
    
    print_step(3, 3, "Verifying installation")
    
    # Verify installations
    verification_failed = []
    for import_name, pip_name in required_modules.items():
        if pip_name in missing_modules:  # Only check newly installed
            # Handle special import names
            check_import_name = import_name
            if pip_name == 'beautifulsoup4':
                check_import_name = 'bs4'
            elif pip_name == 'webdriver-manager':
                check_import_name = 'webdriver_manager'
            
            if is_module_installed(check_import_name):
                print(f"  ✓ {pip_name} - verification passed")
            else:
                verification_failed.append(pip_name)
                print(f"  ✗ {pip_name} - verification failed")
    
    # Summary
    print("\n" + "="*50)
    print("  INSTALLATION SUMMARY")
    print("="*50)
    
    if not failed_installations and not verification_failed:
        print("🎉 SUCCESS: All components installed and verified!")
        print(f"✓ Total modules: {len(required_modules)}")
        print(f"✓ Already installed: {len(installed_modules)}")
        print(f"✓ Newly installed: {len(missing_modules)}")
        return True
    else:
        print("⚠️  PARTIAL SUCCESS: Some issues occurred")
        
        if failed_installations:
            print(f"✗ Failed to install: {', '.join(failed_installations)}")
        
        if verification_failed:
            print(f"✗ Failed verification: {', '.join(verification_failed)}")
        
        print("\nTroubleshooting:")
        print("1. Check your internet connection")
        print("2. Run as administrator")
        print("3. Update pip: python -m pip install --upgrade pip")
        print("4. Try manual installation: pip install module_name")
        
        return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✓ Setup completed successfully!")
            sys.exit(0)
        else:
            print("\n✗ Setup completed with errors!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)