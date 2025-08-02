#!/usr/bin/env python3
"""
Auto Web Page Refresher
A Python script that automatically refreshes a specified web page every 5 minutes.

Usage:
    python auto_refresh.py

Requirements:
    - selenium
    - webdriver-manager
    - Chrome browser installed
"""

import time
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

class WebPageRefresher:
    def __init__(self, url, refresh_interval=300):
        """
        Initialize the web page refresher.
        
        Args:
            url (str): The URL to refresh
            refresh_interval (int): Refresh interval in seconds (default: 300 = 5 minutes)
        """
        self.url = url
        self.refresh_interval = refresh_interval
        self.driver = None
        
    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options."""
        try:
            chrome_options = Options()
            # Add options for better stability
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # Automatically download and setup ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            print(f"✓ Chrome WebDriver initialized successfully")
            return True
            
        except Exception as e:
            print(f"✗ Error setting up WebDriver: {e}")
            return False
    
    def load_page(self):
        """Load the specified web page."""
        try:
            print(f"Loading page: {self.url}")
            self.driver.get(self.url)
            print(f"✓ Page loaded successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return True
        except WebDriverException as e:
            print(f"✗ Error loading page: {e}")
            return False
    
    def refresh_page(self):
        """Refresh the current page."""
        try:
            self.driver.refresh()
            print(f"✓ Page refreshed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return True
        except WebDriverException as e:
            print(f"✗ Error refreshing page: {e}")
            return False
    
    def start_auto_refresh(self):
        """Start the auto-refresh process."""
        if not self.setup_driver():
            return
        
        if not self.load_page():
            self.cleanup()
            return
        
        print(f"\n🔄 Auto-refresh started!")
        print(f"📍 URL: {self.url}")
        print(f"⏰ Refresh interval: {self.refresh_interval} seconds ({self.refresh_interval//60} minutes)")
        print(f"\nPress Ctrl+C to stop the auto-refresh\n")
        
        try:
            refresh_count = 0
            while True:
                # Wait for the specified interval
                time.sleep(self.refresh_interval)
                
                # Refresh the page
                if self.refresh_page():
                    refresh_count += 1
                    print(f"📊 Total refreshes: {refresh_count}")
                else:
                    print("⚠️  Refresh failed, retrying...")
                    time.sleep(5)  # Wait 5 seconds before retry
                    
        except KeyboardInterrupt:
            print(f"\n\n🛑 Auto-refresh stopped by user")
            print(f"📊 Total refreshes performed: {refresh_count}")
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
    """Get URL and refresh interval from user."""
    print("=" * 60)
    print("🌐 Auto Web Page Refresher")
    print("=" * 60)
    
    # Get URL from user
    while True:
        url = input("\nEnter the URL to refresh: ").strip()
        if url:
            # Add http:// if no protocol specified
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            break
        else:
            print("❌ Please enter a valid URL")
    
    # Get refresh interval (optional)
    while True:
        interval_input = input("\nEnter refresh interval in minutes (default: 5): ").strip()
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
        
        refresher = WebPageRefresher(url, interval)
        refresher.start_auto_refresh()
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()