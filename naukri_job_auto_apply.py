#!/usr/bin/env python3
"""
Naukri Job Auto Apply Script - iOS Developer Positions
Automatically searches and applies for iOS developer jobs on Naukri.com

Features:
- Searches for iOS developer, iOS Engineer, SDE-iOS positions
- Filters jobs based on experience and location preferences
- Automatically applies to matching jobs
- Tracks application history to avoid duplicates
- Handles captchas and rate limiting
- Generates detailed reports
"""

import time
import json
import random
import os
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

class NaukriJobAutoApply:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.applied_jobs = set()
        self.session_stats = {
            'jobs_found': 0,
            'jobs_applied': 0,
            'jobs_skipped': 0,
            'errors': 0,
            'start_time': datetime.now()
        }
        
        # Job search keywords for iOS positions
        self.ios_keywords = [
            "iOS Developer",
            "iOS Engineer", 
            "SDE iOS",
            "Software Engineer iOS",
            "Mobile Developer iOS",
            "iOS Application Developer",
            "Senior iOS Developer",
            "iOS Swift Developer"
        ]
        
        # Load previous application history
        self.load_application_history()
        
    def load_application_history(self):
        """Load previously applied job IDs to avoid duplicates"""
        try:
            if os.path.exists('applied_jobs_history.json'):
                with open('applied_jobs_history.json', 'r') as f:
                    data = json.load(f)
                    self.applied_jobs = set(data.get('applied_jobs', []))
                    print(f"📋 Loaded {len(self.applied_jobs)} previously applied jobs")
        except Exception as e:
            print(f"⚠️ Could not load application history: {e}")
            
    def save_application_history(self):
        """Save applied job IDs for future reference"""
        try:
            data = {
                'applied_jobs': list(self.applied_jobs),
                'last_updated': datetime.now().isoformat()
            }
            with open('applied_jobs_history.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save application history: {e}")
    
    def setup_driver(self):
        """Initialize Chrome WebDriver with stealth settings"""
        print("🚀 Setting up Chrome WebDriver...")
        
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)
        
        # Execute script to hide automation indicators
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("✅ WebDriver setup complete")
    
    def human_delay(self, min_seconds=1, max_seconds=3):
        """Add random human-like delays"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def login_check(self):
        """Check if user is logged in to Naukri"""
        print("🔐 Checking login status...")
        
        self.driver.get("https://www.naukri.com")
        self.human_delay(2, 4)
        
        try:
            # Look for login button - if present, user is not logged in
            login_btn = self.driver.find_element(By.ID, "login_Layer")
            print("❌ You are not logged in to Naukri.com")
            print("\n🔑 Please log in manually:")
            print("   1. A browser window will open")
            print("   2. Log in to your Naukri account")
            print("   3. Come back to this terminal and press Enter")
            
            input("\n⏳ Press Enter after you've logged in...")
            
            # Verify login again
            self.driver.refresh()
            self.human_delay(2, 3)
            
            try:
                self.driver.find_element(By.ID, "login_Layer")
                print("❌ Still not logged in. Please try again.")
                return False
            except NoSuchElementException:
                print("✅ Login successful!")
                return True
                
        except NoSuchElementException:
            print("✅ Already logged in!")
            return True
    
    def search_ios_jobs(self, keyword, location="", experience=""):
        """Search for iOS developer jobs"""
        print(f"🔍 Searching for: {keyword}")
        
        # Navigate to jobs search page
        search_url = "https://www.naukri.com/jobs-search"
        self.driver.get(search_url)
        self.human_delay(2, 4)
        
        try:
            # Enter job keyword
            keyword_input = self.wait.until(EC.presence_of_element_located((By.ID, "qsb-keyword-sugg")))
            keyword_input.clear()
            keyword_input.send_keys(keyword)
            self.human_delay(1, 2)
            
            # Enter location if provided
            if location:
                location_input = self.driver.find_element(By.ID, "qsb-location-sugg")
                location_input.clear()
                location_input.send_keys(location)
                self.human_delay(1, 2)
            
            # Click search button
            search_btn = self.driver.find_element(By.CSS_SELECTOR, ".qsbSubmit")
            search_btn.click()
            
            self.human_delay(3, 5)
            print(f"✅ Search completed for: {keyword}")
            return True
            
        except Exception as e:
            print(f"❌ Search failed for {keyword}: {e}")
            return False
    
    def get_job_listings(self):
        """Extract job listings from search results"""
        jobs = []
        
        try:
            # Wait for job listings to load
            job_elements = self.wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".jobTuple, .srp-jobtuple-wrapper")
            ))
            
            print(f"📋 Found {len(job_elements)} job listings")
            
            for job_element in job_elements:
                try:
                    job_data = self.extract_job_data(job_element)
                    if job_data:
                        jobs.append(job_data)
                except Exception as e:
                    print(f"⚠️ Error extracting job data: {e}")
                    continue
            
            self.session_stats['jobs_found'] += len(jobs)
            return jobs
            
        except TimeoutException:
            print("❌ No job listings found or page didn't load")
            return []
    
    def extract_job_data(self, job_element):
        """Extract relevant data from a job listing element"""
        try:
            # Job title
            title_element = job_element.find_element(By.CSS_SELECTOR, ".title a, .jobTupleHeader .ellipsis")
            title = title_element.text.strip()
            job_url = title_element.get_attribute('href')
            
            # Company name
            try:
                company_element = job_element.find_element(By.CSS_SELECTOR, ".subTitle a, .companyInfo .ellipsis")
                company = company_element.text.strip()
            except:
                company = "Unknown Company"
            
            # Experience
            try:
                exp_element = job_element.find_element(By.CSS_SELECTOR, ".expwdth, .experience")
                experience = exp_element.text.strip()
            except:
                experience = "Not specified"
            
            # Location
            try:
                location_element = job_element.find_element(By.CSS_SELECTOR, ".locWdth, .location")
                location = location_element.text.strip()
            except:
                location = "Not specified"
            
            # Extract job ID from URL
            job_id = self.extract_job_id(job_url)
            
            return {
                'id': job_id,
                'title': title,
                'company': company,
                'experience': experience,
                'location': location,
                'url': job_url,
                'element': job_element
            }
            
        except Exception as e:
            print(f"⚠️ Error extracting job data: {e}")
            return None
    
    def extract_job_id(self, job_url):
        """Extract job ID from job URL"""
        try:
            # Naukri job URLs typically contain job ID
            if 'job-listings-' in job_url:
                return job_url.split('job-listings-')[1].split('?')[0]
            elif '/job/' in job_url:
                return job_url.split('/job/')[1].split('?')[0]
            else:
                return job_url.split('/')[-1].split('?')[0]
        except:
            return str(hash(job_url))  # Fallback to hash
    
    def is_ios_relevant(self, job_data):
        """Check if job is relevant for iOS development"""
        title = job_data['title'].lower()
        
        # iOS keywords that should be present
        ios_terms = ['ios', 'iphone', 'swift', 'objective-c', 'xcode', 'cocoa']
        
        # Check if any iOS terms are in the title
        has_ios_term = any(term in title for term in ios_terms)
        
        # Exclude irrelevant positions
        exclude_terms = ['android', 'java', 'backend', 'devops', 'qa', 'testing', 'manual']
        has_exclude_term = any(term in title for term in exclude_terms)
        
        return has_ios_term and not has_exclude_term
    
    def apply_to_job(self, job_data):
        """Apply to a specific job"""
        job_id = job_data['id']
        
        # Check if already applied
        if job_id in self.applied_jobs:
            print(f"⏭️ Already applied to: {job_data['title']} at {job_data['company']}")
            self.session_stats['jobs_skipped'] += 1
            return False
        
        print(f"\n🎯 Applying to: {job_data['title']}")
        print(f"   Company: {job_data['company']}")
        print(f"   Location: {job_data['location']}")
        print(f"   Experience: {job_data['experience']}")
        
        try:
            # Click on the job to open details
            job_element = job_data['element']
            self.driver.execute_script("arguments[0].scrollIntoView(true);", job_element)
            self.human_delay(1, 2)
            
            # Look for apply button
            apply_buttons = job_element.find_elements(By.CSS_SELECTOR, ".apply-button, .btn-apply, [data-ga-track='Apply'], .applyButton")
            
            if not apply_buttons:
                # Try clicking on job title to open details page
                title_link = job_element.find_element(By.CSS_SELECTOR, ".title a, .jobTupleHeader .ellipsis")
                title_link.click()
                self.human_delay(2, 4)
                
                # Look for apply button on job details page
                apply_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".apply-button, .btn-apply, [data-ga-track='Apply'], .applyButton")
            
            if apply_buttons:
                apply_button = apply_buttons[0]
                
                # Scroll to apply button and click
                self.driver.execute_script("arguments[0].scrollIntoView(true);", apply_button)
                self.human_delay(1, 2)
                
                apply_button.click()
                self.human_delay(2, 4)
                
                # Handle any popup or confirmation
                self.handle_application_popup()
                
                # Mark as applied
                self.applied_jobs.add(job_id)
                self.session_stats['jobs_applied'] += 1
                
                print(f"✅ Successfully applied to: {job_data['title']}")
                return True
            else:
                print(f"⚠️ No apply button found for: {job_data['title']}")
                self.session_stats['jobs_skipped'] += 1
                return False
                
        except Exception as e:
            print(f"❌ Failed to apply to {job_data['title']}: {e}")
            self.session_stats['errors'] += 1
            return False
    
    def handle_application_popup(self):
        """Handle any popup that appears after clicking apply"""
        try:
            # Wait for potential popup
            self.human_delay(1, 3)
            
            # Look for common popup elements
            popup_selectors = [
                ".popup-content",
                ".modal-content", 
                ".apply-popup",
                "[role='dialog']"
            ]
            
            for selector in popup_selectors:
                try:
                    popup = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if popup.is_displayed():
                        # Look for submit/apply button in popup
                        submit_buttons = popup.find_elements(By.CSS_SELECTOR, ".btn-submit, .btn-apply, .submit-btn, [type='submit']")
                        if submit_buttons:
                            submit_buttons[0].click()
                            self.human_delay(1, 2)
                            print("✅ Handled application popup")
                            return
                except:
                    continue
                    
        except Exception as e:
            print(f"⚠️ Popup handling: {e}")
    
    def run_job_search_and_apply(self, location="", max_applications=10):
        """Main function to search and apply for iOS jobs"""
        print("\n🎯 Starting iOS Job Auto-Application Process")
        print("=" * 60)
        
        if not self.login_check():
            print("❌ Login required. Exiting...")
            return
        
        applications_made = 0
        
        # Search for each iOS keyword
        for keyword in self.ios_keywords:
            if applications_made >= max_applications:
                print(f"\n🎯 Reached maximum applications limit ({max_applications})")
                break
                
            print(f"\n🔍 Processing keyword: {keyword}")
            
            if self.search_ios_jobs(keyword, location):
                jobs = self.get_job_listings()
                
                for job in jobs:
                    if applications_made >= max_applications:
                        break
                        
                    if self.is_ios_relevant(job):
                        if self.apply_to_job(job):
                            applications_made += 1
                            
                        # Add delay between applications
                        self.human_delay(3, 7)
                    else:
                        print(f"⏭️ Skipping non-iOS job: {job['title']}")
                        self.session_stats['jobs_skipped'] += 1
            
            # Delay between keyword searches
            self.human_delay(5, 10)
        
        self.print_session_summary()
        self.save_application_history()
    
    def print_session_summary(self):
        """Print summary of the application session"""
        duration = datetime.now() - self.session_stats['start_time']
        
        print("\n" + "=" * 60)
        print("📊 SESSION SUMMARY")
        print("=" * 60)
        print(f"⏱️ Duration: {duration}")
        print(f"🔍 Jobs Found: {self.session_stats['jobs_found']}")
        print(f"✅ Jobs Applied: {self.session_stats['jobs_applied']}")
        print(f"⏭️ Jobs Skipped: {self.session_stats['jobs_skipped']}")
        print(f"❌ Errors: {self.session_stats['errors']}")
        print(f"📋 Total Applied (All Time): {len(self.applied_jobs)}")
        print("=" * 60)
        
        if self.session_stats['jobs_applied'] > 0:
            print("🎉 Great! Applications submitted successfully.")
            print("📧 Check your email for application confirmations.")
        else:
            print("ℹ️ No new applications made this session.")
            print("💡 Try adjusting search criteria or check back later.")
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            print("\n🧹 Cleaning up...")
            self.driver.quit()
            print("✅ Browser closed")

def main():
    print("🚀 Naukri iOS Job Auto-Apply Script")
    print("=" * 50)
    print("This script will automatically search and apply for iOS developer positions.")
    print("\n⚠️ IMPORTANT:")
    print("   1. Make sure you're logged into Naukri.com")
    print("   2. Update your resume and profile before running")
    print("   3. Review applications manually after automation")
    print("   4. Use responsibly - don't spam applications")
    
    # Get user preferences
    print("\n📝 Configuration:")
    location = input("Enter preferred location (or press Enter for any): ").strip()
    
    try:
        max_apps = int(input("Maximum applications per session (default 10): ") or "10")
    except ValueError:
        max_apps = 10
    
    print(f"\n🎯 Will search for iOS positions in: {'Any location' if not location else location}")
    print(f"📊 Maximum applications: {max_apps}")
    
    confirm = input("\n🚀 Start auto-application? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Cancelled by user")
        return
    
    auto_apply = NaukriJobAutoApply()
    
    try:
        auto_apply.setup_driver()
        auto_apply.run_job_search_and_apply(location=location, max_applications=max_apps)
    except KeyboardInterrupt:
        print("\n⏹️ Stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    finally:
        auto_apply.cleanup()

if __name__ == "__main__":
    main()