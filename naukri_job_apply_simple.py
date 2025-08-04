#!/usr/bin/env python3
"""
Simplified Naukri Job Auto Apply Script - iOS Developer Positions
A streamlined version that focuses on core functionality
"""

import time
import json
import random
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class SimpleJobApply:
    def __init__(self):
        self.driver = None
        self.applied_count = 0
        self.found_count = 0
        
    def setup_browser(self):
        """Setup Chrome browser"""
        print("🚀 Setting up browser...")
        
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        
        try:
            self.driver = webdriver.Chrome(options=options)
            print("✅ Browser ready!")
            return True
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            return False
    
    def wait_for_login(self):
        """Wait for user to login manually"""
        print("\n🔐 Please log in to Naukri.com")
        self.driver.get("https://www.naukri.com")
        
        input("\n⏳ Press Enter after you've logged in...")
        print("✅ Proceeding with job search...")
    
    def search_ios_jobs(self):
        """Search for iOS developer jobs"""
        print("\n🔍 Searching for iOS developer jobs...")
        
        # Navigate to jobs page
        search_url = "https://www.naukri.com/ios-developer-jobs"
        self.driver.get(search_url)
        time.sleep(3)
        
        print("✅ Search page loaded")
    
    def find_and_apply_jobs(self, max_applications=5):
        """Find jobs and apply to them"""
        print(f"\n🎯 Looking for jobs to apply (max: {max_applications})...")
        
        try:
            # Wait for job listings
            time.sleep(5)
            
            # Find job cards
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, ".jobTuple, .srp-jobtuple-wrapper, .job-tuple")
            
            if not job_cards:
                print("❌ No job listings found")
                return
            
            print(f"📋 Found {len(job_cards)} job listings")
            self.found_count = len(job_cards)
            
            for i, job_card in enumerate(job_cards[:max_applications]):
                if self.applied_count >= max_applications:
                    break
                    
                print(f"\n📝 Processing job {i+1}/{min(len(job_cards), max_applications)}...")
                
                try:
                    # Scroll to job card
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", job_card)
                    time.sleep(2)
                    
                    # Get job title
                    try:
                        title_element = job_card.find_element(By.CSS_SELECTOR, ".title a, .jobTupleHeader a, .job-title a")
                        job_title = title_element.text.strip()
                        print(f"   📌 Job: {job_title}")
                    except:
                        job_title = "Unknown Job"
                        print("   📌 Job: Unknown Title")
                    
                    # Look for apply button
                    apply_selectors = [
                        ".apply-button",
                        ".btn-apply", 
                        "[data-ga-track='Apply']",
                        ".applyButton",
                        "button[title*='Apply']",
                        "a[title*='Apply']"
                    ]
                    
                    apply_button = None
                    for selector in apply_selectors:
                        try:
                            apply_button = job_card.find_element(By.CSS_SELECTOR, selector)
                            if apply_button.is_displayed():
                                break
                        except:
                            continue
                    
                    if apply_button:
                        try:
                            # Click apply button
                            self.driver.execute_script("arguments[0].click();", apply_button)
                            time.sleep(3)
                            
                            # Handle any popup or confirmation
                            self.handle_apply_popup()
                            
                            self.applied_count += 1
                            print(f"   ✅ Applied successfully! ({self.applied_count}/{max_applications})")
                            
                        except Exception as e:
                            print(f"   ❌ Apply failed: {e}")
                    else:
                        print("   ⏭️ No apply button found, skipping...")
                    
                    # Random delay between applications
                    time.sleep(random.uniform(2, 5))
                    
                except Exception as e:
                    print(f"   ❌ Error processing job: {e}")
                    continue
            
        except Exception as e:
            print(f"❌ Error in job search: {e}")
    
    def handle_apply_popup(self):
        """Handle application popup if it appears"""
        try:
            time.sleep(2)
            
            # Look for submit buttons in popups
            submit_selectors = [
                "button[type='submit']",
                ".btn-submit",
                ".submit-btn",
                "input[type='submit']"
            ]
            
            for selector in submit_selectors:
                try:
                    submit_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if submit_btn.is_displayed():
                        submit_btn.click()
                        time.sleep(2)
                        print("   ✅ Popup handled")
                        return
                except:
                    continue
                    
        except Exception as e:
            print(f"   ⚠️ Popup handling: {e}")
    
    def print_summary(self):
        """Print session summary"""
        print("\n" + "=" * 50)
        print("📊 APPLICATION SUMMARY")
        print("=" * 50)
        print(f"🔍 Jobs Found: {self.found_count}")
        print(f"✅ Applications Sent: {self.applied_count}")
        print("=" * 50)
        
        if self.applied_count > 0:
            print("🎉 Applications submitted successfully!")
            print("📧 Check your email for confirmations.")
            print("💼 Monitor your Naukri dashboard for responses.")
        else:
            print("ℹ️ No applications were sent.")
            print("💡 Try refreshing the page or checking different job categories.")
    
    def cleanup(self):
        """Close browser"""
        if self.driver:
            print("\n🧹 Closing browser...")
            self.driver.quit()
            print("✅ Done!")

def main():
    print("🎯 Naukri iOS Job Auto-Apply (Simple Version)")
    print("=" * 50)
    print("This will automatically apply to iOS developer jobs on Naukri.")
    print("\n⚠️ IMPORTANT:")
    print("   • Make sure your Naukri profile is complete")
    print("   • You'll need to log in manually when browser opens")
    print("   • Review applications after automation")
    
    try:
        max_apps = int(input("\nHow many jobs to apply to? (default 5): ") or "5")
    except ValueError:
        max_apps = 5
    
    confirm = input(f"\n🚀 Apply to {max_apps} iOS jobs automatically? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Cancelled")
        return
    
    job_apply = SimpleJobApply()
    
    try:
        if job_apply.setup_browser():
            job_apply.wait_for_login()
            job_apply.search_ios_jobs()
            job_apply.find_and_apply_jobs(max_apps)
            job_apply.print_summary()
        else:
            print("❌ Could not start browser")
            
    except KeyboardInterrupt:
        print("\n⏹️ Stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        job_apply.cleanup()

if __name__ == "__main__":
    main()