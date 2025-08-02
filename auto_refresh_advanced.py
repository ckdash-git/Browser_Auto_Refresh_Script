#!/usr/bin/env python3
"""
Advanced Auto Web Page Refresher
An enhanced version with configuration support and additional features.

Usage:
    python auto_refresh_advanced.py

Features:
    - Configuration file support
    - Quick URL selection
    - Enhanced error handling
    - Retry mechanism
    - Better logging
"""

import time
import sys
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# Import configuration
try:
    from config import CONFIG, QUICK_URLS, FAVORITE_URLS
except ImportError:
    # Fallback configuration if config.py is not found
    CONFIG = {
        'default_refresh_interval': 5,
        'default_url': '',
        'window_width': 1920,
        'window_height': 1080,
        'chrome_options': {
            'headless': False,
            'disable_gpu': True,
            'no_sandbox': True,
            'disable_dev_shm_usage': True,
        },
        'retry_delay': 5,
        'max_retries': 3,
        'show_timestamps': True,
        'show_refresh_counter': True,
        'page_load_timeout': 30,
        'implicit_wait': 10,
    }
    QUICK_URLS = {}
    FAVORITE_URLS = {}

class AdvancedWebPageRefresher:
    def __init__(self, url, refresh_interval=None):
        """
        Initialize the advanced web page refresher.
        
        Args:
            url (str): The URL to refresh
            refresh_interval (int): Refresh interval in seconds
        """
        self.url = url
        self.refresh_interval = refresh_interval or (CONFIG['default_refresh_interval'] * 60)
        self.driver = None
        self.retry_count = 0
        self.max_retries = CONFIG['max_retries']
        
    def setup_driver(self):
        """Setup Chrome WebDriver with configuration options."""
        try:
            chrome_options = Options()
            
            # Apply configuration options
            if CONFIG['chrome_options']['headless']:
                chrome_options.add_argument("--headless")
            if CONFIG['chrome_options']['no_sandbox']:
                chrome_options.add_argument("--no-sandbox")
            if CONFIG['chrome_options']['disable_dev_shm_usage']:
                chrome_options.add_argument("--disable-dev-shm-usage")
            if CONFIG['chrome_options']['disable_gpu']:
                chrome_options.add_argument("--disable-gpu")
            
            # Set window size
            chrome_options.add_argument(f"--window-size={CONFIG['window_width']},{CONFIG['window_height']}")
            
            # Additional stability options
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Setup service
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Set timeouts
            self.driver.set_page_load_timeout(CONFIG['page_load_timeout'])
            self.driver.implicitly_wait(CONFIG['implicit_wait'])
            
            # Execute script to hide automation indicators
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.log("✓ Chrome WebDriver initialized successfully")
            return True
            
        except Exception as e:
            self.log(f"✗ Error setting up WebDriver: {e}")
            return False
    
    def log(self, message):
        """Log message with optional timestamp."""
        if CONFIG['show_timestamps']:
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"[{timestamp}] {message}")
        else:
            print(message)
    
    def load_page(self):
        """Load the specified web page with retry mechanism."""
        for attempt in range(self.max_retries + 1):
            try:
                self.log(f"Loading page: {self.url}")
                self.driver.get(self.url)
                self.log("✓ Page loaded successfully")
                return True
                
            except TimeoutException:
                self.log(f"⚠️  Page load timeout (attempt {attempt + 1}/{self.max_retries + 1})")
                if attempt < self.max_retries:
                    time.sleep(CONFIG['retry_delay'])
                    continue
                    
            except WebDriverException as e:
                self.log(f"✗ Error loading page (attempt {attempt + 1}/{self.max_retries + 1}): {e}")
                if attempt < self.max_retries:
                    time.sleep(CONFIG['retry_delay'])
                    continue
                    
        return False
    
    def refresh_page(self):
        """Refresh the current page with retry mechanism."""
        for attempt in range(self.max_retries + 1):
            try:
                self.driver.refresh()
                self.log("✓ Page refreshed successfully")
                return True
                
            except WebDriverException as e:
                self.log(f"✗ Error refreshing page (attempt {attempt + 1}/{self.max_retries + 1}): {e}")
                if attempt < self.max_retries:
                    time.sleep(CONFIG['retry_delay'])
                    continue
                    
        return False
    
    def start_auto_refresh(self):
        """Start the auto-refresh process."""
        if not self.setup_driver():
            return
        
        if not self.load_page():
            self.cleanup()
            return
        
        self.log("\n🔄 Auto-refresh started!")
        self.log(f"📍 URL: {self.url}")
        self.log(f"⏰ Refresh interval: {self.refresh_interval} seconds ({self.refresh_interval//60} minutes)")
        self.log(f"\nPress Ctrl+C to stop the auto-refresh\n")
        
        try:
            refresh_count = 0
            while True:
                # Wait for the specified interval
                time.sleep(self.refresh_interval)
                
                # Refresh the page
                if self.refresh_page():
                    refresh_count += 1
                    if CONFIG['show_refresh_counter']:
                        self.log(f"📊 Total refreshes: {refresh_count}")
                else:
                    self.log("⚠️  All refresh attempts failed, continuing...")
                    
        except KeyboardInterrupt:
            self.log(f"\n\n🛑 Auto-refresh stopped by user")
            if CONFIG['show_refresh_counter']:
                self.log(f"📊 Total refreshes performed: {refresh_count}")
        except Exception as e:
            self.log(f"\n✗ Unexpected error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        if self.driver:
            try:
                self.driver.quit()
                self.log("✓ Browser closed successfully")
            except Exception as e:
                self.log(f"⚠️  Error closing browser: {e}")

def show_quick_urls():
    """Display available quick URLs."""
    all_urls = {**QUICK_URLS, **FAVORITE_URLS}
    
    if not all_urls:
        return None
    
    print("\n📋 Quick URL Selection:")
    print("-" * 40)
    
    for key, url in all_urls.items():
        print(f"{key}: {url}")
    
    print("-" * 40)
    choice = input("Select a number/key or press Enter to enter custom URL: ").strip()
    
    if choice in all_urls:
        return all_urls[choice]
    
    return None

def get_user_input():
    """Get URL and refresh interval from user with enhanced options."""
    print("=" * 60)
    print("🌐 Advanced Auto Web Page Refresher")
    print("=" * 60)
    
    # Check for default URL in config
    if CONFIG['default_url']:
        use_default = input(f"\nUse default URL ({CONFIG['default_url']})? (y/n): ").strip().lower()
        if use_default in ['y', 'yes', '']:
            url = CONFIG['default_url']
        else:
            url = None
    else:
        url = None
    
    # Get URL from user if not using default
    if not url:
        # Show quick URLs if available
        quick_url = show_quick_urls()
        if quick_url:
            url = quick_url
            print(f"Selected URL: {url}")
        else:
            while True:
                url = input("\nEnter the URL to refresh: ").strip()
                if url:
                    # Add https:// if no protocol specified
                    if not url.startswith(('http://', 'https://')):
                        url = 'https://' + url
                    break
                else:
                    print("❌ Please enter a valid URL")
    
    # Get refresh interval
    while True:
        default_interval = CONFIG['default_refresh_interval']
        interval_input = input(f"\nEnter refresh interval in minutes (default: {default_interval}): ").strip()
        
        if not interval_input:
            interval_minutes = default_interval
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
        # Check if config file exists
        if not os.path.exists('config.py'):
            print("ℹ️  Note: config.py not found, using default settings")
        
        url, interval = get_user_input()
        
        refresher = AdvancedWebPageRefresher(url, interval)
        refresher.start_auto_refresh()
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()