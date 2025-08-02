#!/usr/bin/env python3
"""
Naukri Profile Auto Activity Script
Automatically clicks Edit and Save buttons on Naukri profile to maintain activity.

This script:
1. Opens your Naukri profile page
2. Clicks the Edit button
3. Clicks the Save button
4. Repeats this process at specified intervals

Usage:
    python naukri_auto_activity.py

Requirements:
    - selenium
    - webdriver-manager
    - Chrome browser installed
    - Must be logged into Naukri.com
"""

import time
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

class NaukriAutoActivity:
    def __init__(self, profile_url, activity_interval=300):
        """
        Initialize the Naukri auto activity script.
        
        Args:
            profile_url (str): Your Naukri profile URL
            activity_interval (int): Interval between activities in seconds (default: 300 = 5 minutes)
        """
        self.profile_url = profile_url
        self.activity_interval = activity_interval
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options."""
        try:
            chrome_options = Options()
            # Add options for better stability
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Automatically download and setup ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Set up wait object for element waiting
            self.wait = WebDriverWait(self.driver, 10)
            
            # Execute script to hide automation indicators
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print(f"✓ Chrome WebDriver initialized successfully")
            return True
            
        except Exception as e:
            print(f"✗ Error setting up WebDriver: {e}")
            return False
    
    def load_profile(self):
        """Load the Naukri profile page."""
        try:
            print(f"Loading Naukri profile: {self.profile_url}")
            self.driver.get(self.profile_url)
            
            # Wait for page to load
            time.sleep(3)
            
            # Check if we're logged in by looking for profile elements
            try:
                self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "profile")))
                print(f"✓ Profile page loaded successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                return True
            except TimeoutException:
                print("⚠️  Profile page didn't load properly. Make sure you're logged into Naukri.com")
                return False
                
        except WebDriverException as e:
            print(f"✗ Error loading profile page: {e}")
            return False
    
    def find_edit_button(self):
        """Find and return the edit button element."""
        edit_selectors = [
            "//button[contains(text(), 'Edit')]",
            "//a[contains(text(), 'Edit')]",
            "//span[contains(text(), 'Edit')]",
            "//div[contains(text(), 'Edit')]",
            "//button[contains(@class, 'edit')]",
            "//a[contains(@class, 'edit')]",
            "//i[contains(@class, 'edit')]/parent::*",
            "//button[@title='Edit']",
            "//a[@title='Edit']"
        ]
        
        for selector in edit_selectors:
            try:
                elements = self.driver.find_elements(By.XPATH, selector)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        return element
            except:
                continue
        
        return None
    
    def find_save_button(self):
        """Find and return the save button element."""
        save_selectors = [
            "//button[contains(text(), 'Save')]",
            "//a[contains(text(), 'Save')]",
            "//span[contains(text(), 'Save')]",
            "//div[contains(text(), 'Save')]",
            "//button[contains(@class, 'save')]",
            "//a[contains(@class, 'save')]",
            "//button[@title='Save']",
            "//a[@title='Save']",
            "//input[@type='submit'][contains(@value, 'Save')]",
            "//button[contains(text(), 'Update')]",
            "//button[contains(text(), 'Submit')]"
        ]
        
        for selector in save_selectors:
            try:
                elements = self.driver.find_elements(By.XPATH, selector)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        return element
            except:
                continue
        
        return None
    
    def perform_activity(self):
        """Perform the edit and save activity."""
        try:
            print(f"\n🔄 Starting activity at {datetime.now().strftime('%H:%M:%S')}")
            
            # Step 1: Find and click Edit button
            edit_button = self.find_edit_button()
            if edit_button:
                print("📝 Found Edit button, clicking...")
                self.driver.execute_script("arguments[0].click();", edit_button)
                time.sleep(2)  # Wait for edit mode to load
                
                # Step 2: Find and click Save button
                save_button = self.find_save_button()
                if save_button:
                    print("💾 Found Save button, clicking...")
                    self.driver.execute_script("arguments[0].click();", save_button)
                    time.sleep(2)  # Wait for save to complete
                    print("✅ Activity completed successfully!")
                    return True
                else:
                    print("⚠️  Save button not found, trying alternative approach...")
                    # Try pressing Escape to cancel edit mode
                    self.driver.find_element(By.TAG_NAME, "body").send_keys("\ue00c")  # Escape key
                    return False
            else:
                print("⚠️  Edit button not found. Profile might already be in edit mode or page structure changed.")
                return False
                
        except Exception as e:
            print(f"✗ Error during activity: {e}")
            return False
    
    def start_auto_activity(self):
        """Start the auto-activity process."""
        if not self.setup_driver():
            return
        
        if not self.load_profile():
            self.cleanup()
            return
        
        print(f"\n🚀 Naukri Auto Activity started!")
        print(f"📍 Profile URL: {self.profile_url}")
        print(f"⏰ Activity interval: {self.activity_interval} seconds ({self.activity_interval//60} minutes)")
        print(f"\n📋 What this script does:")
        print(f"   1. Clicks Edit button on your profile")
        print(f"   2. Clicks Save button to complete the activity")
        print(f"   3. Repeats every {self.activity_interval//60} minutes")
        print(f"\nPress Ctrl+C to stop the auto-activity\n")
        
        try:
            activity_count = 0
            while True:
                # Perform the activity
                if self.perform_activity():
                    activity_count += 1
                    print(f"📊 Total activities completed: {activity_count}")
                else:
                    print("⚠️  Activity failed, will retry next cycle")
                
                # Wait for the specified interval
                print(f"⏳ Waiting {self.activity_interval//60} minutes until next activity...\n")
                time.sleep(self.activity_interval)
                
                # Refresh the page before next activity
                self.driver.refresh()
                time.sleep(3)
                    
        except KeyboardInterrupt:
            print(f"\n\n🛑 Auto-activity stopped by user")
            print(f"📊 Total activities performed: {activity_count}")
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        if self.driver:
            try:
                self.driver.quit()
                print("✓ Browser closed successfully")
            except Exception as e:
                print(f"⚠️  Error closing browser: {e}")

def get_user_input():
    """Get profile URL and activity interval from user."""
    print("=" * 70)
    print("🎯 Naukri Profile Auto Activity Script")
    print("=" * 70)
    print("\n⚠️  IMPORTANT: Make sure you're logged into Naukri.com before running this!")
    
    # Get profile URL from user
    while True:
        url = input("\nEnter your Naukri profile URL: ").strip()
        if url:
            # Add https:// if no protocol specified
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            break
        else:
            print("❌ Please enter a valid URL")
    
    # Get activity interval (optional)
    while True:
        interval_input = input("\nEnter activity interval in minutes (default: 5): ").strip()
        if not interval_input:
            interval_minutes = 5
            break
        try:
            interval_minutes = float(interval_input)
            if interval_minutes <= 0:
                print("❌ Please enter a positive number")
                continue
            break
        except ValueError:
            print("❌ Please enter a valid number")
    
    interval_seconds = int(interval_minutes * 60)
    return url, interval_seconds

def main():
    """Main function."""
    try:
        url, interval = get_user_input()
        
        activity_bot = NaukriAutoActivity(url, interval)
        activity_bot.start_auto_activity()
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()