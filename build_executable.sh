#!/bin/bash
# Build script for 가송장 생성기
# This script creates standalone executables for macOS and Windows

cd "$(dirname "$0")" || exit

echo "🔨 Building 가송장 생성기 Executable..."
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install pyinstaller

# Build executable
echo ""
echo "🏗️  Building executable (this may take 2-3 minutes)..."
echo ""

pyinstaller \
    --onefile \
    --windowed \
    --name="가송장_생성기" \
    --icon=resources/icon.icns \
    --add-data="resources:resources" \
    --add-data="src:src" \
    --osx-bundle-identifier="com.tracking.generator" \
    main.py

# Check if build was successful
if [ -d "dist/가송장_생성기.app" ]; then
    echo ""
    echo "✅ BUILD SUCCESSFUL!"
    echo ""
    echo "📍 Your application is ready at:"
    echo "   dist/가송장_생성기.app"
    echo ""
    echo "🚀 To run it, double-click:"
    echo "   dist/가송장_생성기.app"
    echo ""
else
    echo ""
    echo "❌ BUILD FAILED"
    echo "Please check the error messages above"
    exit 1
fi

# Deactivate virtual environment
deactivate

echo "✨ Done!"
