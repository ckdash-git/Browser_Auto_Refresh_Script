#!/usr/bin/env python3
"""
Naukri Profile Auto Activity Script - Session Aware Version
This version handles existing browser sessions and login states better.

Features:
1. Uses existing Chrome profile/session if available
2. Handles login redirects automatically
3. Waits for manual login if needed
4. More robust session management

Usage:
    python naukri_session_activity.py
"""

import time
import sys
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

class NaukriSessionActivity:
    def __init__(self, profile_url, activity_interval=300):
        """
        Initialize the Naukri session-aware auto activity script.
        
        Args:
            profile_url (str): Your Naukri profile URL
            activity_interval (int): Interval between activities in seconds
        """
        self.profile_url = profile_url
        self.activity_interval = activity_interval
        self.driver = None
        self.wait = None
        
    def setup_driver_with_profile(self):
        """Setup Chrome WebDriver using existing user profile."""
        try:
            chrome_options = Options()
            
            # Try to use existing Chrome user data directory
            user_data_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome")
            if os.path.exists(user_data_dir):
                chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
                chrome_options.add_argument("--profile-directory=Default")
                print("✓ Using existing Chrome profile for session continuity")
            
            # Add stability options
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Setup service
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Set up wait object
            self.wait = WebDriverWait(self.driver, 15)
            
            # Hide automation indicators
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print(f"✓ Chrome WebDriver initialized with session support")
            return True
            
        except Exception as e:
            print(f"⚠️  Could not use existing profile, trying fresh session: {e}")
            return self.setup_driver_fresh()
    
    def setup_driver_fresh(self):
        """Setup Chrome WebDriver with fresh session."""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 15)
            
            print(f"✓ Chrome WebDriver initialized with fresh session")
            return True
            
        except Exception as e:
            print(f"✗ Error setting up WebDriver: {e}")
            return False
    
    def handle_login_if_needed(self):
        """Handle login process if user is redirected to login page."""
        try:
            current_url = self.driver.current_url.lower()
            
            # Check if we're on a login page
            if 'login' in current_url or 'signin' in current_url or 'auth' in current_url:
                print("\n🔐 Detected login page. Please log in manually.")
                print("📋 Steps:")
                print("   1. Complete login in the browser window that opened")
                print("   2. Navigate to your profile page")
                print("   3. Come back to this terminal and press Enter")
                
                input("\n⏳ Press Enter after you've logged in and are on your profile page...")
                
                # Check if we're now on the profile page
                current_url = self.driver.current_url.lower()
                if 'profile' in current_url or 'mnjuser' in current_url:
                    print("✅ Great! You're now on your profile page.")
                    return True
                else:
                    print("⚠️  Please navigate to your profile page manually and try again.")
                    return False
            
            return True
            
        except Exception as e:
            print(f"⚠️  Error checking login status: {e}")
            return False
    
    def load_profile_with_session_handling(self):
        """Load profile page with smart session handling."""
        try:
            print(f"Loading Naukri profile: {self.profile_url}")
            self.driver.get(self.profile_url)
            time.sleep(3)
            
            # Handle login if redirected
            if not self.handle_login_if_needed():
                return False
            
            # Verify we're on the profile page
            try:
                # Look for profile indicators
                profile_indicators = [
                    (By.CLASS_NAME, "profile"),
                    (By.XPATH, "//div[contains(@class, 'profile')]"),
                    (By.XPATH, "//h1[contains(text(), 'Profile')]"),
                    (By.XPATH, "//span[contains(text(), 'Edit')]"),
                    (By.XPATH, "//button[contains(text(), 'Edit')]"),
                    (By.XPATH, "//a[contains(text(), 'Edit')]"),
                ]
                
                profile_found = False
                for by, selector in profile_indicators:
                    try:
                        element = self.wait.until(EC.presence_of_element_located((by, selector)))
                        if element:
                            profile_found = True
                            break
                    except TimeoutException:
                        continue
                
                if profile_found:
                    print(f"✅ Profile page loaded successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    return True
                else:
                    print("⚠️  Profile page elements not found. You might need to navigate manually.")
                    print("💡 Make sure you're on your profile page and try again.")
                    return False
                    
            except TimeoutException:
                print("⚠️  Profile page didn't load properly within timeout.")
                return False
                
        except WebDriverException as e:
            print(f"✗ Error loading profile page: {e}")
            return False
    
    def find_edit_button(self):
        """Find edit button with enhanced selectors."""
        edit_selectors = [
            # Text-based selectors
            "//button[contains(text(), 'Edit')]",
            "//a[contains(text(), 'Edit')]",
            "//span[contains(text(), 'Edit')]",
            "//div[contains(text(), 'Edit')]",
            
            # Class-based selectors
            "//button[contains(@class, 'edit')]",
            "//a[contains(@class, 'edit')]",
            "//span[contains(@class, 'edit')]",
            
            # Icon-based selectors
            "//i[contains(@class, 'edit')]/parent::*",
            "//i[contains(@class, 'pencil')]/parent::*",
            
            # Attribute-based selectors
            "//button[@title='Edit']",
            "//a[@title='Edit']",
            "//button[@aria-label='Edit']",
            "//a[@aria-label='Edit']",
            
            # Common Naukri-specific patterns
            "//button[contains(@class, 'naukri-button') and contains(text(), 'Edit')]",
            "//a[contains(@class, 'edit-link')]",
            "//span[contains(@class, 'edit-icon')]/parent::*",
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
        """Find save button with enhanced selectors."""
        save_selectors = [
            # Text-based selectors
            "//button[contains(text(), 'Save')]",
            "//a[contains(text(), 'Save')]",
            "//span[contains(text(), 'Save')]",
            "//button[contains(text(), 'Update')]",
            "//button[contains(text(), 'Submit')]",
            "//button[contains(text(), 'Done')]",
            
            # Class-based selectors
            "//button[contains(@class, 'save')]",
            "//a[contains(@class, 'save')]",
            "//button[contains(@class, 'submit')]",
            "//button[contains(@class, 'update')]",
            
            # Attribute-based selectors
            "//button[@title='Save']",
            "//a[@title='Save']",
            "//input[@type='submit'][contains(@value, 'Save')]",
            "//button[@type='submit']",
            
            # Common form patterns
            "//form//button[last()]",  # Often the last button in a form
            "//div[contains(@class, 'form-actions')]//button",
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
        """Perform edit and save activity with better error handling."""
        try:
            print(f"\n🔄 Starting activity at {datetime.now().strftime('%H:%M:%S')}")
            
            # Step 1: Find and click Edit button
            edit_button = self.find_edit_button()
            if edit_button:
                print("📝 Found Edit button, clicking...")
                # Try different click methods
                try:
                    edit_button.click()
                except:
                    self.driver.execute_script("arguments[0].click();", edit_button)
                
                time.sleep(3)  # Wait for edit mode to load
                
                # Step 2: Find and click Save button
                save_button = self.find_save_button()
                if save_button:
                    print("💾 Found Save button, clicking...")
                    try:
                        save_button.click()
                    except:
                        self.driver.execute_script("arguments[0].click();", save_button)
                    
                    time.sleep(3)  # Wait for save to complete
                    print("✅ Activity completed successfully!")
                    return True
                else:
                    print("⚠️  Save button not found after clicking Edit.")
                    print("💡 This might be normal if the profile doesn't have editable sections.")
                    # Try to cancel edit mode
                    try:
                        self.driver.find_element(By.TAG_NAME, "body").send_keys("\ue00c")  # Escape key
                    except:
                        pass
                    return False
            else:
                print("⚠️  Edit button not found.")
                print("💡 This could mean:")
                print("   - Profile is already in edit mode")
                print("   - Page structure has changed")
                print("   - Need to scroll to find the button")
                
                # Try scrolling and looking again
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                time.sleep(1)
                edit_button = self.find_edit_button()
                if edit_button:
                    print("📝 Found Edit button after scrolling, clicking...")
                    self.driver.execute_script("arguments[0].click();", edit_button)
                    time.sleep(2)
                    return True
                
                return False
                
        except Exception as e:
            print(f"✗ Error during activity: {e}")
            return False
    
    def start_auto_activity(self):
        """Start the session-aware auto-activity process."""
        if not self.setup_driver_with_profile():
            return
        
        if not self.load_profile_with_session_handling():
            self.cleanup()
            return
        
        print(f"\n🚀 Naukri Session-Aware Auto Activity started!")
        print(f"📍 Profile URL: {self.profile_url}")
        print(f"⏰ Activity interval: {self.activity_interval} seconds ({self.activity_interval//60} minutes)")
        print(f"\n📋 Enhanced features:")
        print(f"   ✅ Uses existing browser session when possible")
        print(f"   ✅ Handles login redirects automatically")
        print(f"   ✅ Smart button detection with multiple strategies")
        print(f"   ✅ Better error recovery")
        print(f"\nPress Ctrl+C to stop the auto-activity\n")
        
        try:
            activity_count = 0
            failed_attempts = 0
            max_failures = 3
            
            while True:
                # Perform the activity
                if self.perform_activity():
                    activity_count += 1
                    failed_attempts = 0  # Reset failure counter on success
                    print(f"📊 Total activities completed: {activity_count}")
                else:
                    failed_attempts += 1
                    print(f"⚠️  Activity failed (attempt {failed_attempts}/{max_failures})")
                    
                    if failed_attempts >= max_failures:
                        print(f"\n❌ Too many consecutive failures. Refreshing page...")
                        self.driver.refresh()
                        time.sleep(5)
                        failed_attempts = 0
                
                # Wait for the specified interval
                print(f"⏳ Waiting {self.activity_interval//60} minutes until next activity...\n")
                time.sleep(self.activity_interval)
                    
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
    print("🎯 Naukri Session-Aware Auto Activity Script")
    print("=" * 70)
    print("\n✨ Enhanced Features:")
    print("   🔐 Handles existing login sessions")
    print("   🔄 Smart login detection and handling")
    print("   🎯 Better button detection")
    print("   🛡️  Enhanced error recovery")
    
    # Get profile URL from user
    while True:
        url = input("\nEnter your Naukri profile URL: ").strip()
        if url and not url.startswith('#'):
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            break
        else:
            print("❌ Please enter a valid URL (not a comment)")
    
    # Get activity interval
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
        
        activity_bot = NaukriSessionActivity(url, interval)
        activity_bot.start_auto_activity()
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()