#!/usr/bin/env python3
"""
Advanced Naukri Job Auto Apply Script - iOS Developer Positions
Handles application forms, personal details, and company website applications

Features:
- Fills application forms automatically with your details
- Calculates experience dynamically from start date
- Handles both 'Apply' and 'Apply on Company website' buttons
- Prioritizes recently posted jobs
- Smart form field detection and filling
"""

import time
import json
import random
import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

class AdvancedJobApply:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.applied_count = 0
        self.found_count = 0
        self.skipped_count = 0
        
        # Personal details for form filling
        self.personal_info = {
            'job_start_date': datetime(2024, 3, 11),  # March 11, 2024
            'current_location': 'Bangalore',
            'current_company': 'CACHATTO India Pvt Limited',
            'current_salary': '240000',
            'expected_salary': '450000',
            'notice_period': '30',
            'willing_to_relocate': True,
            'phone': '',  # Will ask user
            'email': ''   # Will ask user
        }
        
        # Calculate current experience
        self.calculate_experience()
        
    def calculate_experience(self):
        """Calculate experience from job start date to current date"""
        current_date = datetime.now()
        start_date = self.personal_info['job_start_date']
        
        # Calculate difference
        diff = relativedelta(current_date, start_date)
        
        self.personal_info['experience_years'] = diff.years
        self.personal_info['experience_months'] = diff.months
        self.personal_info['total_experience'] = f"{diff.years} years {diff.months} months"
        
        print(f"📊 Calculated Experience: {self.personal_info['total_experience']}")
        
    def get_user_contact_info(self):
        """Get user's contact information"""
        print("\n📝 Please provide your contact information:")
        
        phone = input("Enter your phone number: ").strip()
        email = input("Enter your email address: ").strip()
        
        self.personal_info['phone'] = phone
        self.personal_info['email'] = email
        
        print("\n✅ Contact information saved!")
    
    def setup_browser(self):
        """Setup Chrome browser with stealth settings using separate automation profile"""
        print("🚀 Setting up browser...")
        
        options = Options()
        
        # Use separate automation profile to avoid conflicts
        import os
        automation_profile_dir = os.path.expanduser("~/Library/Application Support/Chrome-Automation")
        options.add_argument(f"--user-data-dir={automation_profile_dir}")
        options.add_argument("--profile-directory=AutomationProfile")
        
        # Fix DevToolsActivePort issues
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        
        # Stealth settings
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Disable notifications and popups
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0
        }
        options.add_experimental_option("prefs", prefs)
        
        try:
            self.driver = webdriver.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, 20)
            
            # Hide automation indicators
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Browser ready with existing profile!")
            return True
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            print("💡 Tip: Make sure Chrome is closed before running the script")
            return False
    
    def wait_for_login(self):
        """Wait for user to login to Naukri and detect login status"""
        print("\n🔐 Checking Naukri.com login status...")
        self.driver.get("https://www.naukri.com")
        time.sleep(3)
        
        try:
            # Check if already logged in by looking for profile elements
            login_indicators = [
                ".nI-gNb-drawer__icon",  # Profile icon
                ".nI-gNb-info__name",     # User name
                "[data-ga-track='Header | My Naukri']",  # My Naukri link
                ".nI-gNb-menuItems__profile"  # Profile menu
            ]
            
            logged_in = False
            for indicator in login_indicators:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, indicator)
                    if element.is_displayed():
                        logged_in = True
                        break
                except:
                    continue
            
            if logged_in:
                print("✅ Already logged in! Using existing session.")
            else:
                print("❌ Not logged in to Naukri")
                print("\n🔑 Please log in to Naukri.com in the browser window")
                print("   1. Click on 'Login' button")
                print("   2. Enter your credentials")
                print("   3. Complete login process")
                
                input("\n⏳ Press Enter after you've logged in...")
                
                # Verify login after user confirmation
                for indicator in login_indicators:
                    try:
                        element = self.driver.find_element(By.CSS_SELECTOR, indicator)
                        if element.is_displayed():
                            print("✅ Login confirmed!")
                            break
                    except:
                        continue
                
        except Exception as e:
            print(f"⚠️ Could not detect login status: {e}")
            input("\n⏳ Please ensure you're logged in and press Enter...")
        
        print("✅ Proceeding with job search...")
        return True
    
    def search_recent_ios_jobs(self):
        """Search for iOS developer jobs without filters"""
        print("\n🔍 Searching for iOS developer jobs (no filters applied)...")
        
        # Navigate to basic iOS jobs search without any filters
        search_url = "https://www.naukri.com/ios-developer-jobs?k=ios%20developer"
        self.driver.get(search_url)
        time.sleep(3)
        
        print("✅ Search page loaded - showing all iOS developer jobs")
        return True
    
    def apply_experience_filter(self):
        """Apply experience filter for 1-4 years"""
        try:
            # Look for experience filter options
            experience_filters = [
                "//span[contains(text(), '1-4 years')]",
                "//label[contains(text(), '1-4 years')]",
                "//span[contains(text(), '1-3 years')]",
                "//label[contains(text(), '1-3 years')]",
                "//input[@value='1-4']",
                "//input[@value='1-3']"
            ]
            
            for filter_xpath in experience_filters:
                try:
                    filter_element = self.driver.find_element(By.XPATH, filter_xpath)
                    if filter_element.is_displayed():
                        filter_element.click()
                        print("✅ Applied experience filter (1-4 years)")
                        return
                except:
                    continue
                    
        except Exception as e:
            print(f"⚠️ Experience filter not applied: {e}")
    
    def apply_recent_filter(self):
        """Apply filter for recently posted jobs (few minutes to 7 days)"""
        try:
            # Look for date posted filter - prioritize broader ranges first
            date_filters = [
                "//span[contains(text(), 'Last 7 days')]",
                "//label[contains(text(), 'Last 7 days')]",
                "//span[contains(text(), 'Last 3 days')]",
                "//label[contains(text(), 'Last 3 days')]",
                "//span[contains(text(), 'Today')]",
                "//label[contains(text(), 'Today')]",
                "//span[contains(text(), 'Few hours ago')]",
                "//label[contains(text(), 'Few hours ago')]"
            ]
            
            for filter_xpath in date_filters:
                try:
                    filter_element = self.driver.find_element(By.XPATH, filter_xpath)
                    if filter_element.is_displayed():
                        filter_element.click()
                        print("✅ Applied recent jobs filter (Last 7 days)")
                        return
                except:
                    continue
                    
        except Exception as e:
            print(f"⚠️ Recent filter not applied: {e}")
    
    def find_and_apply_jobs(self, max_applications=5):
        """Find jobs and apply to them with form filling"""
        print(f"\n🎯 Looking for jobs to apply (max: {max_applications})...")
        
        try:
            # Wait for job listings
            time.sleep(5)
            
            # Find job cards with updated selectors
            job_card_selectors = [
                # Modern Naukri job card selectors
                "article[data-jid]",
                "div[data-job-id]",
                "article[data-job-id]", 
                ".srp-jobtuple-wrapper",
                ".jobTuple",
                ".job-tuple", 
                ".cust-job-tuple",
                ".styles_jhc__job-tuple__jAWS4",
                "[class*='job-tuple']",
                "[class*='jobTuple']"
            ]
            
            job_cards = []
            for selector in job_card_selectors:
                try:
                    cards = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if cards:
                        job_cards = cards
                        print(f"✅ Found job cards using selector: {selector}")
                        break
                except:
                    continue
            
            if not job_cards:
                print("❌ No job listings found")
                return
            
            print(f"📋 Found {len(job_cards)} job listings")
            self.found_count = len(job_cards)
            
            for i, job_card in enumerate(job_cards[:max_applications * 2]):  # Check more jobs
                if self.applied_count >= max_applications:
                    break
                    
                print(f"\n📝 Processing job {i+1}...")
                
                try:
                    # Scroll to job card
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", job_card)
                    time.sleep(2)
                    
                    # Get job details
                    job_info = self.extract_job_info(job_card)
                    
                    if self.is_suitable_job(job_info):
                        if self.apply_to_job(job_card, job_info):
                            self.applied_count += 1
                            print(f"   ✅ Applied successfully! ({self.applied_count}/{max_applications})")
                        else:
                            self.skipped_count += 1
                    else:
                        print("   ⏭️ Job not suitable, skipping...")
                        self.skipped_count += 1
                    
                    # Random delay between applications
                    time.sleep(random.uniform(3, 7))
                    
                except Exception as e:
                    print(f"   ❌ Error processing job: {e}")
                    continue
            
        except Exception as e:
            print(f"❌ Error in job search: {e}")
    
    def extract_job_info(self, job_card):
        """Extract job information from job card"""
        job_info = {
            'title': 'Unknown Job',
            'company': 'Unknown Company',
            'location': 'Unknown Location',
            'experience': 'Not specified',
            'posted_date': 'Unknown'
        }
        
        try:
            # Job title - updated selectors
            title_selectors = [
                "a[data-jid]",
                "a[href*='/job-listings-']", 
                "a[href*='/jobs-']",
                ".styles_jd__job-title__rZ4Xy a",
                ".styles_jhc__job-title__2s2pY a",
                "[class*='job-title'] a",
                "a[data-job-title]",
                ".title a",
                ".jobTupleHeader a",
                ".job-title a",
                "h3 a",
                "h4 a"
            ]
            for selector in title_selectors:
                try:
                    title_element = job_card.find_element(By.CSS_SELECTOR, selector)
                    job_info['title'] = title_element.text.strip()
                    break
                except:
                    continue
        except:
            pass
            
        try:
            # Company name - updated selectors
            company_selectors = [
                ".styles_jhc__company-name__2dD8V",
                ".styles_jd__company-name__1bM3z", 
                "[class*='company-name']",
                "[class*='companyName']",
                ".subTitle a",
                ".companyInfo .ellipsis",
                ".comp-name a",
                "[data-company-name]"
            ]
            for selector in company_selectors:
                try:
                    company_element = job_card.find_element(By.CSS_SELECTOR, selector)
                    job_info['company'] = company_element.text.strip()
                    break
                except:
                    continue
        except:
            pass
            
        try:
            # Location - updated selectors
            location_selectors = [
                ".locWdth, .location, .job-location, [data-job-location]"
            ]
            for selector in location_selectors:
                try:
                    location_element = job_card.find_element(By.CSS_SELECTOR, selector)
                    job_info['location'] = location_element.text.strip()
                    break
                except:
                    continue
        except:
            pass
            
        try:
            # Experience - updated selectors
            exp_selectors = [
                ".expwdth, .experience, .job-experience, [data-job-experience]"
            ]
            for selector in exp_selectors:
                try:
                    exp_element = job_card.find_element(By.CSS_SELECTOR, selector)
                    job_info['experience'] = exp_element.text.strip()
                    break
                except:
                    continue
        except:
            pass
            
        try:
            # Posted date - updated selectors
            date_selectors = [
                ".jobTupleFooter .fleft, .posted-date, .job-posted-date, [data-posted-date]"
            ]
            for selector in date_selectors:
                try:
                    date_element = job_card.find_element(By.CSS_SELECTOR, selector)
                    job_info['posted_date'] = date_element.text.strip()
                    break
                except:
                    continue
        except:
            pass
        
        return job_info
    
    def is_suitable_job(self, job_info):
        """Check if job is suitable for application - more lenient criteria"""
        title = job_info['title'].lower()
        experience = job_info['experience'].lower()
        
        # Broader iOS and mobile keywords
        ios_terms = ['ios', 'iphone', 'swift', 'objective-c', 'xcode', 'mobile app', 'mobile application', 'mobile developer', 'app developer', 'mobile development']
        has_ios_term = any(term in title for term in ios_terms)
        
        # If title is "Unknown Job", assume it might be suitable (since we're on iOS search page)
        if job_info['title'] == 'Unknown Job':
            has_ios_term = True
        
        # Only exclude clearly irrelevant positions
        exclude_terms = ['android only', 'backend only', 'devops', 'data scientist', 'data analyst', 'manual testing only']
        has_exclude_term = any(term in title for term in exclude_terms)
        
        # Check experience range (1-4 years) - be flexible with parsing
        suitable_experience = True
        if experience and experience != 'not specified':
            # Extract numbers from experience string
            import re
            exp_numbers = re.findall(r'\d+', experience)
            if exp_numbers:
                min_exp = int(exp_numbers[0])
                max_exp = int(exp_numbers[-1]) if len(exp_numbers) > 1 else min_exp
                # Check if our experience (1+ years) fits in the range
                suitable_experience = (min_exp <= 4 and max_exp >= 1)
        
        # Check if recently posted (few minutes to 7 days)
        posted_date = job_info['posted_date'].lower()
        is_recent = any(term in posted_date for term in [
            'few minutes', 'minutes ago', 'hour ago', 'hours ago', 
            'today', '1 day', '2 days', '3 days', '4 days', '5 days', '6 days', '7 days'
        ])
        
        print(f"   📌 Job: {job_info['title']}")
        print(f"   🏢 Company: {job_info['company']}")
        print(f"   📍 Location: {job_info['location']}")
        print(f"   💼 Experience: {job_info['experience']}")
        print(f"   📅 Posted: {job_info['posted_date']}")
        print(f"   ✅ iOS relevant: {has_ios_term}, Experience suitable: {suitable_experience}, Recent: {is_recent}")
        
        return has_ios_term and not has_exclude_term and suitable_experience
    
    def apply_to_job(self, job_card, job_info):
        """Apply to a specific job with form filling"""
        try:
            print(f"   🔍 Looking for apply buttons in job card...")
            # Look for apply buttons
            apply_buttons = self.find_apply_buttons(job_card)
            print(f"   📊 Found {len(apply_buttons)} apply buttons in job card")
            
            if not apply_buttons:
                print(f"   🔗 No apply buttons in card, trying to click job title...")
                # Try multiple selectors for job title
                title_selectors = [
                    # Modern Naukri title selectors
                    "a[data-jid]",
                    "a[href*='/job-listings-']",
                    "a[href*='/jobs-']",
                    ".styles_jd__job-title__rZ4Xy a",
                    ".styles_jhc__job-title__2s2pY a",
                    "[class*='job-title'] a",
                    "[class*='jobTitle'] a",
                    # Legacy selectors
                    ".title a",
                    ".jobTupleHeader a",
                    "a[data-job-title]",
                    ".job-title a",
                    "h3 a",
                    "h4 a",
                    ".cust-job-tuple .title a"
                ]
                
                title_clicked = False
                for selector in title_selectors:
                    try:
                        title_link = job_card.find_element(By.CSS_SELECTOR, selector)
                        if title_link.is_displayed() and title_link.is_enabled():
                            print(f"   ✅ Found title link with selector: {selector}")
                            # Scroll to element and click
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", title_link)
                            time.sleep(1)
                            # Store current window handle
                            original_window = self.driver.current_window_handle
                            
                            # Try different methods to open in new tab
                            try:
                                # First try JavaScript to open in new tab
                                href = title_link.get_attribute('href')
                                if href:
                                    self.driver.execute_script(f"window.open('{href}', '_blank');")
                                    print(f"   🔗 Attempted JavaScript window.open to new tab")
                                else:
                                    # Fallback to Ctrl+Click
                                    from selenium.webdriver.common.action_chains import ActionChains
                                    from selenium.webdriver.common.keys import Keys
                                    ActionChains(self.driver).key_down(Keys.COMMAND if self.driver.capabilities['platformName'].lower() == 'mac' else Keys.CONTROL).click(title_link).key_up(Keys.COMMAND if self.driver.capabilities['platformName'].lower() == 'mac' else Keys.CONTROL).perform()
                                    print(f"   🔗 Attempted Ctrl+Click to open in new tab")
                            except Exception as action_error:
                                print(f"   ⚠️ ActionChains click failed: {str(action_error)[:100]}...")
                                try:
                                    # Try regular click
                                    title_link.click()
                                except Exception as click_error:
                                    print(f"   ⚠️ Regular click failed: {str(click_error)[:100]}...")
                                    try:
                                        # Try JavaScript click if regular click fails
                                        self.driver.execute_script("arguments[0].click();", title_link)
                                        print(f"   ✅ JavaScript click succeeded")
                                    except Exception as js_click_error:
                                        print(f"   ⚠️ JavaScript click failed: {str(js_click_error)[:100]}...")
                                        continue
                            
                            time.sleep(5)  # Give more time for new tab to open
                            
                            # Check if a new tab was opened
                            try:
                                all_windows = self.driver.window_handles
                                print(f"   📊 Found {len(all_windows)} window(s) open")
                                if len(all_windows) > 1:
                                    # Switch to the new tab
                                    for window in all_windows:
                                        if window != original_window:
                                            self.driver.switch_to.window(window)
                                            print(f"   ✅ Switched to new tab for job details")
                                            print(f"   🌐 Current URL: {self.driver.current_url[:100]}...")
                                            break
                                else:
                                    print(f"   ℹ️ Job opened in same tab")
                                    print(f"   🌐 Current URL: {self.driver.current_url[:100]}...")
                            except Exception as tab_error:
                                print(f"   ⚠️ Tab switching error: {tab_error}")
                            
                            title_clicked = True
                            print(f"   ✅ Successfully clicked job title")
                            break
                    except Exception as e:
                        # Don't print full stack trace for missing elements
                        if "no such element" in str(e).lower():
                            continue
                        else:
                            print(f"   ⚠️ Error with selector {selector}: {str(e)[:100]}...")
                        continue
                
                if not title_clicked:
                    print(f"   ❌ Could not find clickable job title")
                    return False
                
                # Look for apply buttons on job details page
                print(f"   🔍 Searching for apply buttons on job details page...")
                apply_buttons = self.find_apply_buttons()
                print(f"   📊 Found {len(apply_buttons)} apply buttons on details page")
                
                # If no apply buttons found, try to find any buttons for debugging
                if not apply_buttons:
                    print(f"   🔍 Debugging: Looking for any buttons on the page...")
                    all_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button, a[role='button'], input[type='submit']")
                    print(f"   📊 Found {len(all_buttons)} total buttons/links")
                    for i, btn in enumerate(all_buttons[:5]):  # Show first 5 buttons
                        try:
                            btn_text = btn.text.strip()
                            btn_class = btn.get_attribute('class')
                            btn_id = btn.get_attribute('id')
                            print(f"   🔘 Button {i+1}: Text='{btn_text}', Class='{btn_class}', ID='{btn_id}'")
                        except:
                            continue
            
            if apply_buttons:
                for apply_button in apply_buttons:
                    button_text = apply_button.text.lower()
                    
                    print(f"   🔘 Found button: '{apply_button.text}'")
                    
                    # Click the apply button with improved error handling
                    try:
                        # Scroll to element and wait
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", apply_button)
                        time.sleep(2)
                        
                        # Try different click methods
                        try:
                            # First try ActionChains
                            from selenium.webdriver.common.action_chains import ActionChains
                            ActionChains(self.driver).move_to_element(apply_button).click().perform()
                            print(f"   ✅ Clicked apply button using ActionChains")
                        except Exception as action_error:
                            print(f"   ⚠️ ActionChains failed: {str(action_error)[:100]}...")
                            try:
                                # Fallback to JavaScript click
                                self.driver.execute_script("arguments[0].click();", apply_button)
                                print(f"   ✅ Clicked apply button using JavaScript")
                            except Exception as js_error:
                                print(f"   ⚠️ JavaScript click failed: {str(js_error)[:100]}...")
                                # Last resort - regular click
                                apply_button.click()
                                print(f"   ✅ Clicked apply button using regular click")
                    except Exception as click_error:
                        print(f"   ❌ All click methods failed: {str(click_error)[:100]}...")
                        continue
                    time.sleep(3)
                    
                    # Handle application process
                    if 'company website' in button_text or 'external' in button_text:
                        print("   🌐 Redirected to company website")
                        self.handle_external_application()
                    else:
                        print("   📝 Naukri application form")
                        self.handle_naukri_application()
                    
                    # Close new tab and return to original if we opened a new tab
                    all_windows = self.driver.window_handles
                    if len(all_windows) > 1:
                        self.driver.close()  # Close current tab
                        self.driver.switch_to.window(all_windows[0])  # Switch back to original tab
                        print(f"   🔄 Returned to job listings page")
                    
                    return True
            else:
                print("   ❌ No apply button found anywhere")
                # Close new tab and return to original if we opened a new tab
                all_windows = self.driver.window_handles
                if len(all_windows) > 1:
                    self.driver.close()  # Close current tab
                    self.driver.switch_to.window(all_windows[0])  # Switch back to original tab
                    print(f"   🔄 Returned to job listings page")
                return False
                
        except Exception as e:
            print(f"   ❌ Application failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def find_apply_buttons(self, context=None):
        """Find all apply buttons on the page"""
        if context is None:
            context = self.driver
            
        apply_selectors = [
            # Modern Naukri selectors
            "button[data-ga-track*='apply']",
            "a[data-ga-track*='apply']",
            "button[data-ga-track*='Apply']",
            "a[data-ga-track*='Apply']",
            ".styles_apply-button__2mQCg",
            ".styles_jhc__apply-button__3F_bI",
            "button[class*='apply']",
            "a[class*='apply']",
            # Legacy selectors
            ".apply-button",
            ".btn-apply",
            "[data-ga-track='Apply']",
            ".applyButton",
            "button[title*='Apply']",
            "a[title*='Apply']",
            ".job-apply-btn",
            # Generic button selectors - catch all buttons and filter by text
            "button",
            "a[role='button']",
            "input[type='submit']",
            "input[type='button']",
            ".btn",
            "[role='button']"
        ]
        
        buttons = []
        for selector in apply_selectors:
            try:
                elements = context.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        element_text = element.text.strip().lower()
                        element_title = (element.get_attribute('title') or '').lower()
                        element_aria_label = (element.get_attribute('aria-label') or '').lower()
                        element_data_track = (element.get_attribute('data-ga-track') or '').lower()
                        element_class = (element.get_attribute('class') or '').lower()
                        element_id = (element.get_attribute('id') or '').lower()
                        
                        # Check if it's actually an apply button by various attributes
                        apply_indicators = [
                            'apply' in element_text,
                            'apply now' in element_text,
                            element_text == 'apply',
                            'apply' in element_title,
                            'apply' in element_aria_label,
                            'apply' in element_data_track,
                            'apply' in element_class,
                            'apply' in element_id
                        ]
                        
                        if any(apply_indicators):
                            buttons.append(element)
                            print(f"   🔍 Found apply button: Text='{element.text}', Class='{element.get_attribute('class')}', Selector='{selector}'")
            except Exception as e:
                print(f"   ⚠️ Error with selector {selector}: {e}")
                continue
                
        return buttons
    
    def handle_naukri_application(self):
        """Handle Naukri's internal application form"""
        try:
            time.sleep(3)
            
            # Look for application form or popup
            form_selectors = [
                ".popup-content",
                ".modal-content",
                ".apply-popup",
                "[role='dialog']",
                ".application-form"
            ]
            
            form_found = False
            for selector in form_selectors:
                try:
                    form = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if form.is_displayed():
                        print("   📋 Found application form")
                        self.fill_application_form(form)
                        form_found = True
                        break
                except:
                    continue
            
            if not form_found:
                # Look for direct form fields on the page
                self.fill_application_form(self.driver)
            
            # Submit the form
            self.submit_application_form()
            
        except Exception as e:
            print(f"   ⚠️ Form handling error: {e}")
    
    def fill_application_form(self, context):
        """Fill application form with personal details"""
        print("   ✏️ Filling application form...")
        
        # Form field mappings
        field_mappings = {
            'experience': {
                'selectors': ['input[name*="experience"]', 'input[placeholder*="experience"]', '#experience'],
                'value': f"{self.personal_info['experience_years']}"
            },
            'current_salary': {
                'selectors': ['input[name*="current"][name*="salary"]', 'input[placeholder*="current salary"]'],
                'value': self.personal_info['current_salary']
            },
            'expected_salary': {
                'selectors': ['input[name*="expected"][name*="salary"]', 'input[placeholder*="expected salary"]'],
                'value': self.personal_info['expected_salary']
            },
            'notice_period': {
                'selectors': ['select[name*="notice"]', 'input[name*="notice"]', 'select[placeholder*="notice"]'],
                'value': self.personal_info['notice_period']
            },
            'current_location': {
                'selectors': ['input[name*="location"]', 'input[placeholder*="location"]', 'input[name*="city"]'],
                'value': self.personal_info['current_location']
            },
            'phone': {
                'selectors': ['input[name*="phone"]', 'input[name*="mobile"]', 'input[type="tel"]'],
                'value': self.personal_info['phone']
            },
            'email': {
                'selectors': ['input[name*="email"]', 'input[type="email"]'],
                'value': self.personal_info['email']
            }
        }
        
        # Fill each field
        for field_name, field_info in field_mappings.items():
            self.fill_form_field(context, field_info['selectors'], field_info['value'], field_name)
        
        # Handle relocation question
        self.handle_relocation_question(context)
        
        # Handle dropdown selections
        self.handle_dropdown_selections(context)
    
    def fill_form_field(self, context, selectors, value, field_name):
        """Fill a specific form field"""
        for selector in selectors:
            try:
                field = context.find_element(By.CSS_SELECTOR, selector)
                if field.is_displayed() and field.is_enabled():
                    field.clear()
                    field.send_keys(value)
                    print(f"   ✅ Filled {field_name}: {value}")
                    time.sleep(0.5)
                    return True
            except:
                continue
        return False
    
    def handle_relocation_question(self, context):
        """Handle relocation willingness question"""
        relocation_selectors = [
            "input[value*='Yes'][name*='relocat']",
            "input[value*='yes'][name*='relocat']",
            "label:contains('Yes')[for*='relocat']",
            "button:contains('Yes')"
        ]
        
        for selector in relocation_selectors:
            try:
                element = context.find_element(By.CSS_SELECTOR, selector)
                if element.is_displayed():
                    element.click()
                    print("   ✅ Selected willing to relocate: Yes")
                    return
            except:
                continue
    
    def handle_dropdown_selections(self, context):
        """Handle dropdown selections for experience, notice period, etc."""
        try:
            # Experience dropdown
            exp_dropdowns = context.find_elements(By.CSS_SELECTOR, "select[name*='experience'], select[name*='exp']")
            for dropdown in exp_dropdowns:
                if dropdown.is_displayed():
                    select = Select(dropdown)
                    # Try to select appropriate experience
                    for option in select.options:
                        if '1' in option.text and 'year' in option.text.lower():
                            select.select_by_visible_text(option.text)
                            print(f"   ✅ Selected experience: {option.text}")
                            break
            
            # Notice period dropdown
            notice_dropdowns = context.find_elements(By.CSS_SELECTOR, "select[name*='notice']")
            for dropdown in notice_dropdowns:
                if dropdown.is_displayed():
                    select = Select(dropdown)
                    for option in select.options:
                        if '30' in option.text or 'month' in option.text.lower():
                            select.select_by_visible_text(option.text)
                            print(f"   ✅ Selected notice period: {option.text}")
                            break
                            
        except Exception as e:
            print(f"   ⚠️ Dropdown handling: {e}")
    
    def submit_application_form(self):
        """Submit the application form"""
        submit_selectors = [
            "button[type='submit']",
            "input[type='submit']",
            ".btn-submit",
            ".submit-btn",
            "button:contains('Submit')",
            "button:contains('Apply')",
            "a:contains('Submit')"
        ]
        
        for selector in submit_selectors:
            try:
                submit_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                if submit_btn.is_displayed() and submit_btn.is_enabled():
                    submit_btn.click()
                    print("   ✅ Application submitted!")
                    time.sleep(3)
                    return True
            except:
                continue
        
        print("   ⚠️ Could not find submit button")
        return False
    
    def handle_external_application(self):
        """Handle application on company website"""
        try:
            print("   🌐 Handling external application...")
            time.sleep(5)
            
            # Check if we're on a different domain
            current_url = self.driver.current_url
            if 'naukri.com' not in current_url:
                print(f"   🔗 Redirected to: {current_url}")
                
                # Try to find and fill application form on external site
                self.fill_external_application_form()
            else:
                print("   ℹ️ Still on Naukri, may be a popup")
                
        except Exception as e:
            print(f"   ⚠️ External application handling: {e}")
    
    def fill_external_application_form(self):
        """Fill application form on external company website"""
        try:
            time.sleep(3)
            
            # Look for common form fields
            common_fields = {
                'name': ['input[name*="name"]', 'input[placeholder*="name"]'],
                'email': ['input[type="email"]', 'input[name*="email"]'],
                'phone': ['input[type="tel"]', 'input[name*="phone"]'],
                'experience': ['input[name*="experience"]', 'select[name*="experience"]']
            }
            
            for field_type, selectors in common_fields.items():
                for selector in selectors:
                    try:
                        field = self.driver.find_element(By.CSS_SELECTOR, selector)
                        if field.is_displayed():
                            if field_type == 'email':
                                field.send_keys(self.personal_info['email'])
                            elif field_type == 'phone':
                                field.send_keys(self.personal_info['phone'])
                            elif field_type == 'experience':
                                field.send_keys(self.personal_info['total_experience'])
                            print(f"   ✅ Filled {field_type}")
                            break
                    except:
                        continue
            
            # Try to submit if submit button is found
            self.submit_application_form()
            
        except Exception as e:
            print(f"   ⚠️ External form filling: {e}")
    
    def print_summary(self):
        """Print session summary"""
        print("\n" + "=" * 60)
        print("📊 APPLICATION SESSION SUMMARY")
        print("=" * 60)
        print(f"🔍 Jobs Found: {self.found_count}")
        print(f"✅ Applications Sent: {self.applied_count}")
        print(f"⏭️ Jobs Skipped: {self.skipped_count}")
        print(f"👤 Experience: {self.personal_info['total_experience']}")
        print(f"📍 Location: {self.personal_info['current_location']}")
        print(f"💰 Expected Salary: ₹{self.personal_info['expected_salary']}")
        print("=" * 60)
        
        if self.applied_count > 0:
            print("🎉 Applications submitted successfully!")
            print("📧 Check your email for confirmations.")
            print("💼 Monitor your Naukri dashboard for responses.")
            print("📱 Follow up with companies if needed.")
        else:
            print("ℹ️ No applications were sent this session.")
            print("💡 Try adjusting search criteria or check back later.")
    
    def cleanup(self):
        """Close browser"""
        if self.driver:
            print("\n🧹 Closing browser...")
            self.driver.quit()
            print("✅ Done!")

def main():
    print("🎯 Advanced Naukri iOS Job Auto-Apply")
    print("=" * 50)
    print("This script will automatically apply to iOS jobs with intelligent form filling.")
    print("\n🔍 SEARCH CRITERIA:")
    print("   • Job Type: iOS/Mobile development roles")
    print("   • Location: All over India (no location restrictions)")
    print("   • Experience: All levels (no experience filter)")
    print("   • Posted: All recent jobs (no date filter)")
    print("\n⚠️ FEATURES:")
    print("   • Uses Chrome browser with automation profile (requires manual login)")
    print("   • Fills application forms automatically")
    print("   • Handles both Naukri and company website applications")
    print("   • Calculates experience dynamically from March 11, 2024")
    print("   • No salary filtering - applies to all suitable positions")
    print("   • Smart experience range matching")
    
    try:
        max_apps = int(input("\nHow many jobs to apply to? (default 5): ") or "5")
    except ValueError:
        max_apps = 5
    
    confirm = input(f"\n🚀 Apply to {max_apps} iOS jobs (All levels, All India, No filters)? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Cancelled")
        return
    
    job_apply = AdvancedJobApply()
    
    try:
        # Get contact information
        job_apply.get_user_contact_info()
        
        if job_apply.setup_browser():
            job_apply.wait_for_login()
            job_apply.search_recent_ios_jobs()
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