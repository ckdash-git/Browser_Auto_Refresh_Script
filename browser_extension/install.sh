#!/bin/bash

# Installation script for Naukri Profile Activity Booster Browser Extension
# This script helps users set up the extension quickly

echo "🚀 Naukri Profile Activity Booster - Browser Extension Installer"
echo "================================================================"
echo ""

# Check if we're in the right directory
if [ ! -f "manifest.json" ]; then
    echo "❌ Error: manifest.json not found!"
    echo "Please run this script from the browser_extension directory."
    exit 1
fi

echo "✅ Extension files found!"
echo ""

# Check Chrome installation
if command -v google-chrome >/dev/null 2>&1; then
    CHROME_CMD="google-chrome"
elif command -v chromium >/dev/null 2>&1; then
    CHROME_CMD="chromium"
elif command -v "Google Chrome" >/dev/null 2>&1; then
    CHROME_CMD="Google Chrome"
elif [ -d "/Applications/Google Chrome.app" ]; then
    CHROME_CMD="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
else
    echo "⚠️  Chrome not found in PATH"
    echo "Please make sure Google Chrome is installed."
    CHROME_CMD=""
fi

if [ -n "$CHROME_CMD" ]; then
    echo "✅ Chrome found: $CHROME_CMD"
else
    echo "❌ Chrome not detected automatically"
fi

echo ""
echo "📋 Installation Instructions:"
echo "============================"
echo ""
echo "1. Open Google Chrome"
echo "2. Go to: chrome://extensions/"
echo "3. Enable 'Developer mode' (toggle in top-right)"
echo "4. Click 'Load unpacked'"
echo "5. Select this folder: $(pwd)"
echo "6. Pin the extension to your toolbar"
echo ""

echo "🎯 Quick Setup:"
echo "==============="
echo ""
echo "Option 1 - Manual Setup:"
echo "  • Follow the instructions above"
echo ""
echo "Option 2 - Auto-open Chrome Extensions (if Chrome detected):"
if [ -n "$CHROME_CMD" ]; then
    read -p "  Would you like to open Chrome Extensions page now? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "  Opening Chrome Extensions page..."
        "$CHROME_CMD" "chrome://extensions/" 2>/dev/null &
        echo "  ✅ Chrome Extensions page opened!"
        echo "  Now enable Developer mode and click 'Load unpacked'"
    fi
else
    echo "  Chrome not detected - please open manually"
fi

echo ""
echo "📁 Extension Directory:"
echo "======================"
echo "Current directory: $(pwd)"
echo "Select this folder when clicking 'Load unpacked'"
echo ""

echo "📚 Files included:"
echo "=================="
ls -la *.json *.js *.html *.md 2>/dev/null | while read line; do
    echo "  $line"
done

echo ""
echo "🔧 After Installation:"
echo "======================"
echo "1. Navigate to: https://www.naukri.com/mnjuser/profile"
echo "2. Click the extension icon in Chrome toolbar"
echo "3. Configure your settings:"
echo "   • Activity Interval: 5 minutes (recommended)"
echo "   • Activity Mode: Stealth (recommended)"
echo "4. Click 'Start Activity Booster'"
echo "5. Monitor the statistics and enjoy!"
echo ""

echo "📖 For detailed instructions, see README.md"
echo ""
echo "🎉 Happy job hunting!"
echo "Keep your Naukri profile active and visible to recruiters!"
echo ""