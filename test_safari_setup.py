#!/usr/bin/env python3
"""
Safari WebDriver Setup Test
This script helps verify that Safari is properly configured for automation.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_safari_setup():
    print("🧪 Testing Safari WebDriver Setup")
    print("=" * 40)
    
    print("\n📋 Prerequisites Check:")
    print("   1. Safari → Preferences → Advanced → Show Develop menu ✓")
    print("   2. Develop → Allow Remote Automation ✓")
    print("   3. Safari should be closed before running this test")
    
    print("\n🚨 IMPORTANT: Safari Automation Alert")
    print("   When Safari opens, you'll see an automation alert.")
    print("   Click 'Continue Session' to proceed with the test.")
    
    input("\n⚠️  Press Enter after enabling Safari Developer features...")
    
    try:
        print("\n🚀 Step 1: Creating Safari WebDriver...")
        driver = webdriver.Safari()
        print("✅ Safari WebDriver created successfully!")
        
        print("\n🚀 Step 2: Setting window size...")
        driver.set_window_size(1200, 800)
        print("✅ Window size set successfully!")
        
        print("\n🚀 Step 3: Navigating to Google...")
        driver.get("https://www.google.com")
        print("✅ Navigation successful!")
        
        print("\n🚀 Step 4: Testing basic interaction...")
        wait = WebDriverWait(driver, 10)
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
        search_box.send_keys("Safari WebDriver Test")
        print("✅ Basic interaction successful!")
        
        print("\n🚀 Step 5: Testing Naukri.com access...")
        driver.get("https://www.naukri.com")
        time.sleep(3)
        print("✅ Naukri.com loaded successfully!")
        
        print("\n🎉 SUCCESS! Safari is properly configured for automation.")
        print("\n📝 You can now run: python3 naukri_job_apply_advanced.py")
        
        input("\n⏸️  Press Enter to close Safari...")
        driver.quit()
        print("✅ Safari closed successfully!")
        
    except Exception as e:
        print(f"\n❌ Safari setup failed: {e}")
        print("\n🔧 Troubleshooting Steps:")
        print("   1. Open Safari manually")
        print("   2. Go to Safari → Preferences → Advanced")
        print("   3. Check 'Show Develop menu in menu bar'")
        print("   4. Go to Develop → Allow Remote Automation")
        print("   5. Close Safari completely")
        print("   6. Run this test again")
        print("\n💡 Note: You may need to restart Safari after enabling these settings.")
        
        try:
            driver.quit()
        except:
            pass
        
        return False
    
    return True

if __name__ == "__main__":
    success = test_safari_setup()
    if success:
        print("\n🎯 Safari is ready for job applications!")
    else:
        print("\n⚠️  Please fix Safari setup before running the job application script.")