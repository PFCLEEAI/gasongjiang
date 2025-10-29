#!/usr/bin/env python3
"""
Build Script for 가송장 생성기
Creates standalone executables for macOS and Windows
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header(text):
    """Print section header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def run_command(cmd, description=""):
    """Run command and check for errors"""
    if description:
        print(f"\n📦 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=False)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main build function"""
    print_header("🔨 가송장 생성기 Build Tool")

    # Detect platform
    system = platform.system()
    print(f"\n🖥️  Detected OS: {system}")

    if system not in ["Darwin", "Windows", "Linux"]:
        print("❌ Unsupported operating system")
        return False

    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ required")
        return False

    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")

    # Get project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)

    print(f"\n📍 Project Directory: {project_dir}")

    # Step 1: Create virtual environment
    print_header("Step 1: Virtual Environment")
    venv_dir = "venv"

    if not Path(venv_dir).exists():
        print(f"Creating virtual environment in {venv_dir}...")
        if not run_command(f"{sys.executable} -m venv {venv_dir}"):
            return False
        print("✅ Virtual environment created")
    else:
        print("✅ Virtual environment already exists")

    # Determine venv activate command
    if system == "Windows":
        activate_cmd = f"{venv_dir}\\Scripts\\activate &&"
        pip_cmd = f"{venv_dir}\\Scripts\\pip"
        python_cmd = f"{venv_dir}\\Scripts\\python"
    else:
        activate_cmd = f"source {venv_dir}/bin/activate &&"
        pip_cmd = f"{venv_dir}/bin/pip"
        python_cmd = f"{venv_dir}/bin/python"

    # Step 2: Install dependencies
    print_header("Step 2: Install Dependencies")

    print("Upgrading pip...")
    if not run_command(f"{pip_cmd} install --upgrade pip"):
        return False

    print("\nInstalling requirements.txt...")
    if not run_command(f"{pip_cmd} install -r requirements.txt"):
        print("⚠️  Some dependencies may have failed, continuing anyway...")

    print("\nInstalling PyInstaller...")
    if not run_command(f"{pip_cmd} install pyinstaller"):
        return False

    print("✅ All dependencies installed")

    # Step 3: Build executable
    print_header("Step 3: Building Executable")

    # Build parameters
    if system == "Darwin":  # macOS
        build_cmd = f"{python_cmd} -m PyInstaller --onefile --windowed --name=가송장_생성기 main.py"
        output_name = "dist/가송장_생성기"
        app_name = "가송장 생성기 (macOS)"
    elif system == "Windows":
        build_cmd = f"{python_cmd} -m PyInstaller --onefile --windowed --name=가송장_생성기 main.py"
        output_name = "dist\\가송장_생성기.exe"
        app_name = "가송장 생성기 (Windows)"
    else:  # Linux
        build_cmd = f"{python_cmd} -m PyInstaller --onefile --name=가송장_생성기 main.py"
        output_name = "dist/가송장_생성기"
        app_name = "가송장 생성기 (Linux)"

    print(f"\n🏗️  Building {app_name}...")
    print("This may take 2-3 minutes on first build...\n")

    if not run_command(build_cmd):
        print("❌ Build failed")
        return False

    # Step 4: Verify build
    print_header("Step 4: Verify Build")

    if Path(output_name).exists() or Path(f"{output_name}.app").exists():
        print("✅ BUILD SUCCESSFUL!")

        if system == "Darwin":
            app_path = f"dist/가송장_생성기.app"
            print(f"\n📍 Your application: {app_path}")
            print(f"\n🚀 To run it:")
            print(f"   1. Double-click in Finder, OR")
            print(f"   2. Run: open {app_path}")
            print(f"   3. Or: ./dist/가송장_생성기")
        elif system == "Windows":
            exe_path = "dist\\가송장_생성기.exe"
            print(f"\n📍 Your application: {exe_path}")
            print(f"\n🚀 To run it:")
            print(f"   1. Double-click dist\\가송장_생성기.exe in Explorer")
            print(f"   2. Or run from PowerShell: .\\dist\\가송장_생성기.exe")
        else:  # Linux
            print(f"\n📍 Your application: dist/가송장_생성기")
            print(f"\n🚀 To run it:")
            print(f"   ./dist/가송장_생성기")

        return True
    else:
        print("❌ Build verification failed")
        print(f"Expected output not found at: {output_name}")
        return False

if __name__ == "__main__":
    print("\n🎉 가송장 생성기 Build Script\n")

    try:
        success = main()

        print("\n" + "=" * 60)
        if success:
            print("✅ BUILD COMPLETE - Ready to use!")
            print("=" * 60)
            sys.exit(0)
        else:
            print("❌ BUILD FAILED - Check errors above")
            print("=" * 60)
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Build cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
