#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flight Tool - Virtual Environment Setup
Creates and configures a Python virtual environment for the project
"""

import sys
import os
import subprocess
import platform

# Fix Windows console encoding issues
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def print_step(step_num, total_steps, description):
    """Print step information"""
    print(f"\n[Step {step_num}/{total_steps}] {description}")
    print("-" * 60)


def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("ERROR: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"Python version: {sys.version.split()[0]} - OK")
    return True


def create_venv(venv_path):
    """Create virtual environment"""
    try:
        import venv
        print(f"Creating virtual environment at: {venv_path}")
        venv.create(venv_path, with_pip=True)
        print("Virtual environment created successfully")
        return True
    except Exception as e:
        print(f"ERROR creating virtual environment: {e}")
        return False


def get_venv_python(venv_path):
    """Get path to Python executable in venv"""
    if platform.system() == 'Windows':
        return os.path.join(venv_path, 'Scripts', 'python.exe')
    else:
        return os.path.join(venv_path, 'bin', 'python')


def get_venv_pip(venv_path):
    """Get path to pip executable in venv"""
    if platform.system() == 'Windows':
        return os.path.join(venv_path, 'Scripts', 'pip.exe')
    else:
        return os.path.join(venv_path, 'bin', 'pip')


def upgrade_pip(venv_path):
    """Upgrade pip in virtual environment"""
    pip_path = get_venv_pip(venv_path)
    python_path = get_venv_python(venv_path)

    try:
        print("Upgrading pip...")
        subprocess.run(
            [python_path, '-m', 'pip', 'install', '--upgrade', 'pip'],
            check=True,
            capture_output=True,
            text=True
        )
        print("Pip upgraded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"WARNING: Could not upgrade pip: {e}")
        return False


def install_requirements(venv_path):
    """Install required packages in virtual environment"""
    pip_path = get_venv_pip(venv_path)

    packages = [
        'selenium',
        'webdriver-manager',
        'requests',
        'beautifulsoup4',
        'pandas',
        'openpyxl'
    ]

    print("Installing required packages:")
    for package in packages:
        print(f"  - {package}")

    try:
        subprocess.run(
            [pip_path, 'install'] + packages,
            check=True
        )
        print("\nAll packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nERROR installing packages: {e}")
        return False


def create_activation_script():
    """Create easy activation script"""
    if platform.system() == 'Windows':
        script_path = 'activate_venv.bat'
        content = """@echo off
echo Activating Flight Tool virtual environment...
call venv\\Scripts\\activate.bat
echo.
echo Virtual environment activated!
echo To deactivate, type: deactivate
echo.
"""
    else:
        script_path = 'activate_venv.sh'
        content = """#!/bin/bash
echo "Activating Flight Tool virtual environment..."
source venv/bin/activate
echo ""
echo "Virtual environment activated!"
echo "To deactivate, type: deactivate"
echo ""
"""

    try:
        with open(script_path, 'w') as f:
            f.write(content)

        if platform.system() != 'Windows':
            os.chmod(script_path, 0o755)

        print(f"Created activation script: {script_path}")
        return True
    except Exception as e:
        print(f"WARNING: Could not create activation script: {e}")
        return False


def create_run_scripts(venv_path):
    """Create scripts to run tools with venv"""
    python_path = get_venv_python(venv_path)

    scripts = {
        'run_test.bat' if platform.system() == 'Windows' else 'run_test.sh': 'test_system.py',
        'run_scraper.bat' if platform.system() == 'Windows' else 'run_scraper.sh': 'scrap_only_extended.py'
    }

    for script_name, python_file in scripts.items():
        if platform.system() == 'Windows':
            content = f"""@echo off
"{python_path}" {python_file} %*
"""
        else:
            content = f"""#!/bin/bash
"{python_path}" {python_file} "$@"
"""

        try:
            with open(script_name, 'w') as f:
                f.write(content)

            if platform.system() != 'Windows':
                os.chmod(script_name, 0o755)

            print(f"Created: {script_name}")
        except Exception as e:
            print(f"WARNING: Could not create {script_name}: {e}")

    return True


def print_usage_instructions():
    """Print instructions for using the virtual environment"""
    print_header("SETUP COMPLETE!")

    if platform.system() == 'Windows':
        print("\nTo activate the virtual environment:")
        print("  Method 1: Double-click 'activate_venv.bat'")
        print("  Method 2: Run in terminal: activate_venv.bat")
        print("  Method 3: Run in terminal: venv\\Scripts\\activate.bat")
        print("\nTo run tools without activating:")
        print("  - Test system: run_test.bat")
        print("  - Run scraper: run_scraper.bat")
    else:
        print("\nTo activate the virtual environment:")
        print("  Method 1: ./activate_venv.sh")
        print("  Method 2: source venv/bin/activate")
        print("\nTo run tools without activating:")
        print("  - Test system: ./run_test.sh")
        print("  - Run scraper: ./run_scraper.sh")

    print("\nTo deactivate the virtual environment:")
    print("  deactivate")

    print("\nThe virtual environment includes all required packages:")
    print("  - Selenium WebDriver")
    print("  - WebDriver Manager")
    print("  - Requests")
    print("  - BeautifulSoup4")
    print("  - Pandas")
    print("  - OpenPyXL")


def main():
    """Main setup function"""
    print_header("FLIGHT TOOL - VIRTUAL ENVIRONMENT SETUP")

    venv_path = 'venv'
    total_steps = 6

    # Step 1: Check Python version
    print_step(1, total_steps, "Checking Python version")
    if not check_python_version():
        return False

    # Step 2: Create virtual environment
    print_step(2, total_steps, "Creating virtual environment")
    if os.path.exists(venv_path):
        print(f"Virtual environment already exists at: {venv_path}")
        response = input("Do you want to recreate it? (y/n): ").lower()
        if response == 'y':
            import shutil
            print("Removing existing virtual environment...")
            shutil.rmtree(venv_path)
            if not create_venv(venv_path):
                return False
        else:
            print("Using existing virtual environment")
    else:
        if not create_venv(venv_path):
            return False

    # Step 3: Upgrade pip
    print_step(3, total_steps, "Upgrading pip")
    upgrade_pip(venv_path)

    # Step 4: Install packages
    print_step(4, total_steps, "Installing required packages")
    if not install_requirements(venv_path):
        return False

    # Step 5: Create activation script
    print_step(5, total_steps, "Creating activation scripts")
    create_activation_script()

    # Step 6: Create run scripts
    print_step(6, total_steps, "Creating run scripts")
    create_run_scripts(venv_path)

    # Print usage instructions
    print_usage_instructions()

    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: Setup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
