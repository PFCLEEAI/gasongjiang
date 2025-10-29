#!/bin/bash
# Build Windows executable using Docker

echo "🐳 Building Windows .exe using Docker..."
echo ""

# Check if Docker is running
if ! docker ps > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Build Docker image
echo "🔨 Building Docker image..."
docker build -f Dockerfile.windows -t gasongjiang-builder .

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed"
    exit 1
fi

echo ""
echo "✅ Docker image built successfully"
echo ""

# Create container and copy files
echo "📦 Creating container and building .exe..."
docker run --name gasongjiang-temp -v $(pwd)/dist:/app/dist gasongjiang-builder true

# Copy the dist folder
if [ -d "dist" ]; then
    echo "✅ Windows .exe created successfully!"
    ls -lh dist/

    echo ""
    echo "📍 Your Windows executable:"
    echo "   dist/가송장_생성기.exe"

    echo ""
    echo "🚀 To use on Windows:"
    echo "   1. Copy dist/가송장_생성기.exe to a Windows machine"
    echo "   2. Double-click it to run!"
    echo "   3. No Python or dependencies needed!"
else
    echo "❌ dist folder not found"
    exit 1
fi

# Cleanup
docker rm gasongjiang-temp 2>/dev/null

echo ""
echo "✨ Done!"
