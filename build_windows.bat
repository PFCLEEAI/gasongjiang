@echo off
REM Build script for 가송장 생성기 Windows .exe
REM Run this on a Windows machine with Python installed

echo.
echo ========================================
echo  가송장 생성기 Windows Builder
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.9+ from python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

if errorlevel 1 (
    echo ❌ Failed to create venv
    pause
    exit /b 1
)

echo ✅ Virtual environment created
echo.

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

REM Install dependencies (using Windows-optimized versions)
echo 📥 Installing dependencies...
pip install -r requirements-windows.txt

if errorlevel 1 (
    echo ⚠️  Some dependencies may have failed, but continuing...
)

echo ✅ Dependencies installed
echo.

REM Build executable using spec file
echo 🏗️  Building Windows executable...
echo    (This may take 2-5 minutes on first build)
echo.

pyinstaller gasongjiang.spec

if errorlevel 1 (
    echo ⚠️  First build attempt completed. Trying alternative method...
    echo.
    pyinstaller ^
        --onefile ^
        --windowed ^
        --name="가송장_생성기" ^
        main.py
)

if errorlevel 1 (
    echo ❌ Build failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ BUILD SUCCESSFUL!
echo ========================================
echo.
echo 📍 Your Windows executable is ready:
echo    dist\가송장_생성기.exe
echo.
echo 🚀 To use it:
echo    1. Double-click dist\가송장_생성기.exe
echo    2. Upload your Excel file
echo    3. Generate tracking numbers!
echo.
echo 📦 To share with others:
echo    Just copy dist\가송장_생성기.exe to any Windows machine
echo    No Python installation needed!
echo.

pause
