@echo off
REM Auto Web Page Refresher Setup Script for Windows
REM This script helps you set up and run the auto-refresh tool

echo 🌐 Auto Web Page Refresher Setup
echo ====================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH.
    echo    Please install Python 3.7 or higher from: https://www.python.org/downloads/
    echo    Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo ✓ Python found:
python --version

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not installed or not in PATH.
    echo    pip should come with Python. Please reinstall Python.
    pause
    exit /b 1
)

echo ✓ pip found

REM Install requirements
echo.
echo 📦 Installing required packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install packages. Please check your internet connection and try again.
    pause
    exit /b 1
)

echo ✓ All packages installed successfully!

REM Check if Chrome is installed (basic check)
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    echo ✓ Google Chrome found
) else if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    echo ✓ Google Chrome found
) else (
    echo ⚠️  Google Chrome not found in standard locations
    echo    Please install Chrome from: https://www.google.com/chrome/
)

echo.
echo 🎉 Setup complete!
echo.
echo You can now run:
echo   python auto_refresh.py          (Basic version)
echo   python auto_refresh_advanced.py (Advanced version)
echo   python demo.py                  (Demo/info)
echo.
echo 📖 For detailed instructions, see README.md

REM Ask if user wants to run the script now
echo.
set /p response="❓ Would you like to run the auto-refresh script now? (y/n): "
if /i "%response%"=="y" (
    echo.
    echo 🚀 Starting auto-refresh script...
    python auto_refresh.py
) else if /i "%response%"=="yes" (
    echo.
    echo 🚀 Starting auto-refresh script...
    python auto_refresh.py
)

pause