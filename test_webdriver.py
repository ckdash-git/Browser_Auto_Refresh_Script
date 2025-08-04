#!/usr/bin/env python3
"""
WebDriver Test Script - Diagnose Chrome/Selenium Issues
This script tests each step of WebDriver setup to identify where it's failing.
"""

import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def test_webdriver_setup():
    print("🔧 WebDriver Diagnostic Test")
    print("=" * 50)
    
    try:
        print("Step 1: Testing imports...")
        print("✅ Selenium imported successfully")
        
        print("\nStep 2: Setting up Chrome options...")
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        print("✅ Chrome options configured")
        
        print("\nStep 3: Installing/updating ChromeDriver...")
        try:
            driver_path = ChromeDriverManager().install()
            print(f"✅ ChromeDriver installed at: {driver_path}")
        except Exception as e:
            print(f"❌ ChromeDriver installation failed: {e}")
            return False
        
        print("\nStep 4: Creating WebDriver service...")
        try:
            service = Service(driver_path)
            print("✅ WebDriver service created")
        except Exception as e:
            print(f"❌ Service creation failed: {e}")
            return False
        
        print("\nStep 5: Launching Chrome browser...")
        print("⏳ This may take 10-30 seconds...")
        try:
            driver = webdriver.Chrome(service=service, options=chrome_options)
            print("✅ Chrome browser launched successfully!")
            
            print("\nStep 6: Testing basic navigation...")
            driver.get("https://www.google.com")
            print(f"✅ Navigated to: {driver.current_url}")
            print(f"✅ Page title: {driver.title}")
            
            print("\nStep 7: Testing Naukri access...")
            driver.get("https://www.naukri.com")
            print(f"✅ Navigated to: {driver.current_url}")
            print(f"✅ Page title: {driver.title}")
            
            print("\n🎉 All tests passed! WebDriver is working correctly.")
            print("\nClosing browser in 5 seconds...")
            time.sleep(5)
            driver.quit()
            print("✅ Browser closed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Browser launch failed: {e}")
            print("\n🔍 Possible solutions:")
            print("   1. Update Chrome to latest version")
            print("   2. Restart your computer")
            print("   3. Check if Chrome is already running")
            print("   4. Try running with sudo (admin privileges)")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\n🔧 Fix: Install missing packages:")
        print("   pip3 install selenium webdriver-manager")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    print("🚀 Starting WebDriver diagnostic...")
    print("This will help identify why the Naukri script is hanging.\n")
    
    success = test_webdriver_setup()
    
    if success:
        print("\n✅ DIAGNOSIS: WebDriver is working fine!")
        print("The issue might be with the Naukri script logic.")
        print("\n🎯 Next steps:")
        print("   1. Try running naukri_auto_activity.py again")
        print("   2. Make sure you're logged into Naukri first")
        print("   3. Check your internet connection")
    else:
        print("\n❌ DIAGNOSIS: WebDriver setup is failing!")
        print("This explains why the Naukri script hangs.")
        print("\n🔧 Recommended fixes:")
        print("   1. Update Chrome: chrome://settings/help")
        print("   2. Reinstall dependencies: pip3 install --upgrade selenium webdriver-manager")
        print("   3. Restart your computer")
        print("   4. Try running as administrator")

if __name__ == "__main__":
    main()