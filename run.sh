#!/bin/bash

# 가송장 생성기 Application Launcher
# Run this script to start the application

PROJ_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJ_DIR"

echo "🚀 Starting 가송장 생성기..."
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv --system-site-packages
    source venv/bin/activate
    echo "📥 Installing dependencies..."
    python3 -m pip install --upgrade pip -q
    python3 -m pip install PyQt5==5.15.10 pandas openpyxl xlrd pydantic python-dateutil -q
    echo "✅ Setup complete!"
else
    source venv/bin/activate
fi

echo ""
echo "════════════════════════════════════════════════════════════"
echo "   가송장 생성기 (Tracking Number Generator)"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "💡 QUICK GUIDE:"
echo "   1. Click '📂 파일 선택' to select your Excel file"
echo "   2. Click '🔄 송장 생성' to generate tracking numbers"
echo "   3. Click '💾 Excel 다운로드' to download the result"
echo ""
echo "   📁 Test file: $(pwd)/test_sample.xlsx"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""

# Launch the application
python3 main.py
