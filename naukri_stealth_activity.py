#!/usr/bin/env python3
"""
Naukri Profile Auto Activity Script - Stealth Version
This version is designed to be undetectable by automation detection systems.

Features:
1. Advanced stealth techniques to bypass automation detection
2. Human-like behavior simulation
3. Random timing and mouse movements
4. Undetectable browser fingerprinting

Usage:
    python naukri_stealth_activity.py
"""

import time
import sys
import os
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

class NaukriStealthActivity:
    def __init__(self, profile_url, activity_interval=300):
        """
        Initialize the stealth Naukri auto activity script.
        
        Args:
            profile_url (str): Your Naukri profile URL
            activity_interval (int): Interval between activities in seconds
        """
        self.profile_url = profile_url
        self.activity_interval = activity_interval
        self.driver = None
        self.wait = None
        self.actions = None
        
    def setup_stealth_driver(self):
        """Setup Chrome WebDriver with advanced stealth options."""
        try:
            chrome_options = Options()
            
            # Advanced stealth options
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # Anti-detection measures
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Additional stealth options
            chrome_options.add_argument("--disable-extensions-file-access-check")
            chrome_options.add_argument("--disable-extensions-http-throttling")
            chrome_options.add_argument("--disable-extensions-except")
            chrome_options.add_argument("--disable-component-extensions-with-background-pages")
            chrome_options.add_argument("--disable-default-apps")
            chrome_options.add_argument("--disable-background-timer-throttling")
            chrome_options.add_argument("--disable-renderer-backgrounding")
            chrome_options.add_argument("--disable-backgrounding-occluded-windows")
            chrome_options.add_argument("--disable-client-side-phishing-detection")
            chrome_options.add_argument("--disable-sync")
            chrome_options.add_argument("--metrics-recording-only")
            chrome_options.add_argument("--no-report-upload")
            
            # User agent randomization
            user_agents = [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ]
            chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
            
            # Setup service
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Advanced stealth JavaScript execution
            stealth_js = """
            // Remove webdriver property
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            // Mock chrome runtime
            window.chrome = {
                runtime: {},
            };
            
            // Mock permissions
            Object.defineProperty(navigator, 'permissions', {
                get: () => ({
                    query: () => Promise.resolve({ state: 'granted' }),
                }),
            });
            
            // Mock plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            // Mock languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
            
            // Override the `plugins` property to use a custom getter.
            Object.defineProperty(navigator, 'plugins', {
                get: function() {
                    return [
                        {
                            0: {
                                type: "application/x-google-chrome-pdf",
                                suffixes: "pdf",
                                description: "Portable Document Format",
                                enabledPlugin: Plugin
                            },
                            description: "Portable Document Format",
                            filename: "internal-pdf-viewer",
                            length: 1,
                            name: "Chrome PDF Plugin"
                        }
                    ];
                }
            });
            """
            
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': stealth_js
            })
            
            # Set up wait and actions
            self.wait = WebDriverWait(self.driver, 15)
            self.actions = ActionChains(self.driver)
            
            print(f"✓ Stealth Chrome WebDriver initialized successfully")
            return True
            
        except Exception as e:
            print(f"✗ Error setting up stealth WebDriver: {e}")
            return False
    
    def human_like_delay(self, min_seconds=1, max_seconds=3):
        """Add human-like random delays."""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def human_like_mouse_movement(self, element):
        """Simulate human-like mouse movement to element."""
        try:
            # Get element location
            location = element.location
            size = element.size
            
            # Calculate random point within element
            x_offset = random.randint(5, size['width'] - 5)
            y_offset = random.randint(5, size['height'] - 5)
            
            # Move to element with human-like curve
            self.actions.move_to_element_with_offset(element, x_offset, y_offset)
            self.human_like_delay(0.5, 1.5)
            
        except Exception:
            # Fallback to simple move
            self.actions.move_to_element(element)
    
    def stealth_click(self, element):
        """Perform a human-like click with random timing."""
        try:
            # Human-like mouse movement
            self.human_like_mouse_movement(element)
            
            # Random delay before click
            self.human_like_delay(0.3, 0.8)
            
            # Perform click
            self.actions.click(element).perform()
            
            # Random delay after click
            self.human_like_delay(0.5, 1.2)
            
            return True
            
        except Exception as e:
            # Fallback to JavaScript click
            try:
                self.driver.execute_script("arguments[0].click();", element)
                self.human_like_delay(0.5, 1.0)
                return True
            except:
                return False
    
    def random_scroll(self):
        """Perform random scrolling to simulate human behavior."""
        try:
            # Random scroll direction and amount
            scroll_directions = ['up', 'down']
            direction = random.choice(scroll_directions)
            amount = random.randint(100, 500)
            
            if direction == 'down':
                self.driver.execute_script(f"window.scrollBy(0, {amount});")
            else:
                self.driver.execute_script(f"window.scrollBy(0, -{amount});")
            
            self.human_like_delay(0.5, 1.5)
            
        except Exception:
            pass
    
    def load_profile_stealthily(self):
        """Load profile page with stealth techniques."""
        try:
            print(f"Loading Naukri profile stealthily: {self.profile_url}")
            
            # Navigate to page
            self.driver.get(self.profile_url)
            
            # Random delay to simulate reading
            self.human_like_delay(3, 6)
            
            # Random scroll to simulate browsing
            self.random_scroll()
            
            # Check if profile loaded
            profile_indicators = [
                (By.XPATH, "//span[contains(text(), 'Edit')]"),
                (By.XPATH, "//button[contains(text(), 'Edit')]"),
                (By.XPATH, "//a[contains(text(), 'Edit')]"),
                (By.CLASS_NAME, "profile"),
            ]
            
            for by, selector in profile_indicators:
                try:
                    element = self.wait.until(EC.presence_of_element_located((by, selector)))
                    if element:
                        print(f"✅ Profile page loaded stealthily at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        return True
                except TimeoutException:
                    continue
            
            print("⚠️  Profile elements not detected, but continuing...")
            return True
            
        except Exception as e:
            print(f"✗ Error loading profile page: {e}")
            return False
    
    def find_edit_button_stealthily(self):
        """Find edit button with stealth techniques."""
        # Simulate browsing behavior
        self.random_scroll()
        self.human_like_delay(1, 2)
        
        edit_selectors = [
            "//button[contains(text(), 'Edit')]",
            "//a[contains(text(), 'Edit')]",
            "//span[contains(text(), 'Edit')]",
            "//div[contains(text(), 'Edit')]",
            "//button[contains(@class, 'edit')]",
            "//a[contains(@class, 'edit')]",
            "//i[contains(@class, 'edit')]/parent::*",
            "//button[@title='Edit']",
            "//a[@title='Edit']",
        ]
        
        for selector in edit_selectors:
            try:
                elements = self.driver.find_elements(By.XPATH, selector)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        # Simulate looking at the element
                        self.human_like_mouse_movement(element)
                        self.human_like_delay(0.5, 1.0)
                        return element
            except:
                continue
        
        return None
    
    def find_save_button_stealthily(self):
        """Find save button with stealth techniques."""
        self.human_like_delay(1, 2)
        
        save_selectors = [
            "//button[contains(text(), 'Save')]",
            "//a[contains(text(), 'Save')]",
            "//button[contains(text(), 'Update')]",
            "//button[contains(text(), 'Submit')]",
            "//button[contains(@class, 'save')]",
            "//button[@type='submit']",
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
    
    def perform_stealth_activity(self):
        """Perform edit and save activity with stealth techniques."""
        try:
            print(f"\n🥷 Starting stealth activity at {datetime.now().strftime('%H:%M:%S')}")
            
            # Simulate browsing behavior before action
            self.random_scroll()
            self.human_like_delay(2, 4)
            
            # Find edit button
            edit_button = self.find_edit_button_stealthily()
            if edit_button:
                print("📝 Found Edit button, performing stealth click...")
                
                if self.stealth_click(edit_button):
                    # Wait for edit mode with human-like delay
                    self.human_like_delay(2, 4)
                    
                    # Find save button
                    save_button = self.find_save_button_stealthily()
                    if save_button:
                        print("💾 Found Save button, performing stealth click...")
                        
                        if self.stealth_click(save_button):
                            # Wait for save completion
                            self.human_like_delay(2, 4)
                            print("✅ Stealth activity completed successfully!")
                            return True
                        else:
                            print("⚠️  Failed to click Save button")
                    else:
                        print("⚠️  Save button not found")
                        # Try to escape edit mode
                        self.driver.find_element(By.TAG_NAME, "body").send_keys("\ue00c")
                else:
                    print("⚠️  Failed to click Edit button")
            else:
                print("⚠️  Edit button not found")
                # Simulate continued browsing
                self.random_scroll()
            
            return False
            
        except Exception as e:
            print(f"✗ Error during stealth activity: {e}")
            return False
    
    def start_stealth_auto_activity(self):
        """Start the stealth auto-activity process."""
        if not self.setup_stealth_driver():
            return
        
        if not self.load_profile_stealthily():
            self.cleanup()
            return
        
        print(f"\n🥷 Naukri Stealth Auto Activity started!")
        print(f"📍 Profile URL: {self.profile_url}")
        print(f"⏰ Activity interval: {self.activity_interval} seconds ({self.activity_interval//60} minutes)")
        print(f"\n🛡️  Stealth features enabled:")
        print(f"   ✅ Anti-detection measures")
        print(f"   ✅ Human-like behavior simulation")
        print(f"   ✅ Random timing and movements")
        print(f"   ✅ Undetectable browser fingerprinting")
        print(f"\nPress Ctrl+C to stop the stealth auto-activity\n")
        
        try:
            activity_count = 0
            
            while True:
                # Add random variation to interval (±20%)
                variation = random.uniform(0.8, 1.2)
                actual_interval = int(self.activity_interval * variation)
                
                # Perform stealth activity
                if self.perform_stealth_activity():
                    activity_count += 1
                    print(f"📊 Total stealth activities completed: {activity_count}")
                else:
                    print("⚠️  Stealth activity cycle completed (may not have found buttons)")
                
                # Human-like waiting with random activities
                print(f"⏳ Waiting ~{actual_interval//60} minutes until next activity...")
                
                # Break waiting into smaller chunks with random activities
                chunks = actual_interval // 30  # 30-second chunks
                for i in range(chunks):
                    time.sleep(30)
                    
                    # Occasionally perform random browsing actions
                    if random.random() < 0.3:  # 30% chance
                        self.random_scroll()
                        self.human_like_delay(1, 3)
                
                # Sleep remaining time
                remaining = actual_interval % 30
                if remaining > 0:
                    time.sleep(remaining)
                    
        except KeyboardInterrupt:
            print(f"\n\n🛑 Stealth auto-activity stopped by user")
            print(f"📊 Total stealth activities performed: {activity_count}")
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
    print("🥷 Naukri Stealth Auto Activity Script")
    print("=" * 70)
    print("\n🛡️  Advanced Stealth Features:")
    print("   🚫 Bypasses automation detection")
    print("   🤖 Simulates human behavior")
    print("   🎭 Randomized timing and actions")
    print("   👻 Undetectable browser fingerprint")
    
    # Get profile URL
    while True:
        url = input("\nEnter your Naukri profile URL: ").strip()
        if url and not url.startswith('#'):
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            break
        else:
            print("❌ Please enter a valid URL")
    
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
        
        stealth_bot = NaukriStealthActivity(url, interval)
        stealth_bot.start_stealth_auto_activity()
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()