@echo off
REM Installation script for Naukri Profile Activity Booster Browser Extension
REM This script helps Windows users set up the extension quickly

echo.
echo 🚀 Naukri Profile Activity Booster - Browser Extension Installer
echo ================================================================
echo.

REM Check if we're in the right directory
if not exist "manifest.json" (
    echo ❌ Error: manifest.json not found!
    echo Please run this script from the browser_extension directory.
    pause
    exit /b 1
)

echo ✅ Extension files found!
echo.

REM Check Chrome installation
set CHROME_FOUND=0
set CHROME_PATH=""

REM Check common Chrome installation paths
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH="%ProgramFiles%\Google\Chrome\Application\chrome.exe"
    set CHROME_FOUND=1
) else if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH="%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
    set CHROME_FOUND=1
) else if exist "%LocalAppData%\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH="%LocalAppData%\Google\Chrome\Application\chrome.exe"
    set CHROME_FOUND=1
)

if %CHROME_FOUND%==1 (
    echo ✅ Chrome found: %CHROME_PATH%
) else (
    echo ❌ Chrome not detected automatically
    echo Please make sure Google Chrome is installed.
)

echo.
echo 📋 Installation Instructions:
echo ============================
echo.
echo 1. Open Google Chrome
echo 2. Go to: chrome://extensions/
echo 3. Enable 'Developer mode' (toggle in top-right)
echo 4. Click 'Load unpacked'
echo 5. Select this folder: %CD%
echo 6. Pin the extension to your toolbar
echo.

echo 🎯 Quick Setup:
echo ===============
echo.
echo Option 1 - Manual Setup:
echo   • Follow the instructions above
echo.
echo Option 2 - Auto-open Chrome Extensions:
if %CHROME_FOUND%==1 (
    set /p "choice=  Would you like to open Chrome Extensions page now? (y/n): "
    if /i "!choice!"=="y" (
        echo   Opening Chrome Extensions page...
        start "" %CHROME_PATH% "chrome://extensions/"
        echo   ✅ Chrome Extensions page opened!
        echo   Now enable Developer mode and click 'Load unpacked'
    )
) else (
    echo   Chrome not detected - please open manually
)

echo.
echo 📁 Extension Directory:
echo ======================
echo Current directory: %CD%
echo Select this folder when clicking 'Load unpacked'
echo.

echo 📚 Files included:
echo ==================
dir /b *.json *.js *.html *.md 2>nul
echo.

echo 🔧 After Installation:
echo ======================
echo 1. Navigate to: https://www.naukri.com/mnjuser/profile
echo 2. Click the extension icon in Chrome toolbar
echo 3. Configure your settings:
echo    • Activity Interval: 5 minutes (recommended)
echo    • Activity Mode: Stealth (recommended)
echo 4. Click 'Start Activity Booster'
echo 5. Monitor the statistics and enjoy!
echo.

echo 📖 For detailed instructions, see README.md
echo.
echo 🎉 Happy job hunting!
echo Keep your Naukri profile active and visible to recruiters!
echo.

pause