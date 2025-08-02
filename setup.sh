#!/bin/bash

# Auto Web Page Refresher Setup Script
# This script helps you set up and run the auto-refresh tool

echo "🌐 Auto Web Page Refresher Setup"
echo "===================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    echo "   Download from: https://www.python.org/downloads/"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✓ pip3 found"

# Install requirements
echo "\n📦 Installing required packages..."
if pip3 install -r requirements.txt; then
    echo "✓ All packages installed successfully!"
else
    echo "❌ Failed to install packages. Please check your internet connection and try again."
    exit 1
fi

# Check if Chrome is installed (basic check)
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if [ -d "/Applications/Google Chrome.app" ]; then
        echo "✓ Google Chrome found"
    else
        echo "⚠️  Google Chrome not found in /Applications/"
        echo "   Please install Chrome from: https://www.google.com/chrome/"
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v google-chrome &> /dev/null || command -v chromium-browser &> /dev/null; then
        echo "✓ Chrome/Chromium found"
    else
        echo "⚠️  Chrome/Chromium not found"
        echo "   Please install Chrome or Chromium browser"
    fi
fi

echo "\n🎉 Setup complete!"
echo "\nYou can now run:"
echo "  python3 auto_refresh.py          (Basic version)"
echo "  python3 auto_refresh_advanced.py (Advanced version)"
echo "  python3 demo.py                  (Demo/info)"

echo "\n📖 For detailed instructions, see README.md"

# Ask if user wants to run the script now
echo "\n❓ Would you like to run the auto-refresh script now? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "\n🚀 Starting auto-refresh script..."
    python3 auto_refresh.py
fi