# Naukri Automation Suite 🚀

A comprehensive collection of automation tools for Naukri.com profile activity and job applications.

## 📋 Available Tools

### 1. Profile Activity Scripts
Keep your Naukri profile active and visible to recruiters:

- **`naukri_auto_activity.py`** - Reliable profile activity automation
- **`naukri_session_activity.py`** - Uses existing Chrome session
- **`naukri_stealth_activity.py`** - Advanced stealth features

### 2. Job Application Scripts
Automatically search and apply for iOS developer positions:

- **`naukri_job_apply_advanced.py`** - 🆕 Advanced form-filling with intelligent automation
- **`naukri_job_auto_apply.py`** - Full-featured job application automation
- **`naukri_job_apply_simple.py`** - Simplified version for quick setup

### 3. Browser Extension
Manual control extension for profile activity:

- **`browser_extension/`** - Chrome extension for manual profile updates

### 4. Diagnostic Tools
- **`test_webdriver.py`** - Test WebDriver setup and diagnose issues

## 📁 Files Overview

### 1. `naukri_job_apply_advanced.py` - 🆕 Advanced Form-Filling Script
The most comprehensive job application tool with intelligent form filling:

- **Automatic Form Filling**: Fills application forms with your personal details
- **Dynamic Experience Calculation**: Calculates experience from your start date (March 11, 2024)
- **Dual Application Support**: Handles both "Apply" and "Apply on Company website" buttons
- **Recent Jobs Priority**: Focuses on recently posted positions
- **Smart Field Detection**: Automatically detects and fills salary, location, notice period fields
- **External Site Handling**: Can fill forms on company websites too

### 2. `naukri_job_auto_apply.py` - Main Application Script
The comprehensive job application automation tool with advanced features:

- **Smart Job Filtering**: Automatically filters iOS-related positions
- **Human-like Behavior**: Random delays and natural browsing patterns
- **Safety Features**: Application limits and confirmation prompts
- **Detailed Logging**: Real-time progress updates and session summaries
- **Error Handling**: Robust error recovery and graceful failures

### 3. `naukri_job_apply_simple.py` - Lightweight Version
A streamlined version for quick job applications:

- **Fast Execution**: Minimal delays for quick results
- **Simple Interface**: Easy to use with basic configuration
- **Essential Features**: Core functionality without advanced options

### 4. `test_webdriver.py` - Diagnostic Tool
Troubleshooting utility to verify your setup:

- **Browser Testing**: Verifies Chrome/ChromeDriver installation
- **Naukri Access**: Tests website connectivity
- **Setup Validation**: Confirms all dependencies are working

## 🎯 Job Auto-Application Features

### 🆕 Advanced Form Filling (naukri_job_apply_advanced.py)
✅ **Personal Details Auto-Fill**: Automatically fills your information:
- Experience: Dynamically calculated from March 11, 2024 (currently 1 year 5 months)
- Current Location: Bangalore
- Current Company: CACHATTO India Pvt Limited
- Current Salary: ₹240,000
- Expected Salary: ₹450,000
- Notice Period: 30 days
- Willing to Relocate: Yes

✅ **Dual Application Support**: Handles both "Apply" and "Apply on Company website" buttons

✅ **External Site Forms**: Can fill forms on company websites too

✅ **Recent Jobs Priority**: Focuses on recently posted positions

### What It Does
✅ **Searches for iOS-related positions:**
- iOS Developer
- iOS Engineer
- SDE-iOS
- Software Engineer iOS
- Mobile Developer iOS
- iOS Swift Developer
- Senior iOS Developer

✅ **Smart filtering:**
- Filters out non-iOS positions (Android, Backend, etc.)
- Checks job relevance using keywords
- Avoids duplicate applications

✅ **Automated application process:**
- Finds and clicks apply buttons
- Handles application popups
- Tracks application history
- Provides detailed reports

✅ **Human-like behavior:**
- Random delays between actions
- Scrolling and natural interactions
- Stealth browser settings

## 🚀 Quick Start - Job Auto-Application

### Option 1: Advanced Form-Filling Script (🆕 Recommended)
```bash
# Install additional dependency for date calculations
pip3 install -r requirements_advanced.txt

# Run the advanced script with form filling
python3 naukri_job_apply_advanced.py
```

### Option 2: Full-Featured Version
```bash
python3 naukri_job_auto_apply.py
```

### Option 3: Simple Version (For beginners)
```bash
python3 naukri_job_apply_simple.py
```

### Option 4: Test Setup First
```bash
python3 test_webdriver.py
```

## 📖 Step-by-Step Guide

### Prerequisites
1. **Install dependencies:**
   ```bash
   pip3 install selenium webdriver-manager
   ```

2. **Update your Naukri profile:**
   - Complete all profile sections
   - Upload latest resume
   - Add relevant skills and experience

3. **Have Chrome browser installed**

### Running the Job Auto-Application

1. **Start the script:**
   ```bash
   python3 naukri_job_apply_simple.py
   ```

2. **Configure settings:**
   - Enter number of jobs to apply to (default: 5)
   - Confirm to start automation

3. **Manual login:**
   - Browser will open to Naukri.com
   - Log in to your account manually
   - Return to terminal and press Enter

4. **Automation begins:**
   - Script searches for iOS developer jobs
   - Automatically applies to relevant positions
   - Shows progress in terminal

5. **Review results:**
   - Check application summary
   - Monitor email for confirmations
   - Review applications in Naukri dashboard

## ⚙️ Configuration Options

### Simple Version Settings
- **Max Applications:** Number of jobs to apply to per session
- **Manual Login:** Ensures account security
- **Real-time Progress:** See applications as they happen

### Full Version Settings
- **Location Preferences:** Filter by city/region
- **Experience Level:** Match your experience
- **Application History:** Tracks all applications
- **Advanced Filtering:** More precise job matching

## 📊 What to Expect

### Terminal Output
```
🎯 Naukri iOS Job Auto-Apply (Simple Version)
==================================================
🚀 Setting up browser...
✅ Browser ready!

🔐 Please log in to Naukri.com
⏳ Press Enter after you've logged in...
✅ Proceeding with job search...

🔍 Searching for iOS developer jobs...
✅ Search page loaded

🎯 Looking for jobs to apply (max: 5)...
📋 Found 15 job listings

📝 Processing job 1/5...
   📌 Job: iOS Developer - Swift
   ✅ Applied successfully! (1/5)

📝 Processing job 2/5...
   📌 Job: Senior iOS Engineer
   ✅ Applied successfully! (2/5)

==================================================
📊 APPLICATION SUMMARY
==================================================
🔍 Jobs Found: 15
✅ Applications Sent: 5
==================================================
🎉 Applications submitted successfully!
📧 Check your email for confirmations.
💼 Monitor your Naukri dashboard for responses.
```

### Browser Behavior
- Opens Chrome browser
- Navigates to Naukri job search
- Scrolls through job listings
- Clicks apply buttons automatically
- Handles application forms and popups

## 🛡️ Safety Features

### Built-in Protections
- **Rate Limiting:** Delays between applications
- **Duplicate Prevention:** Tracks applied jobs
- **Manual Login:** Keeps your credentials secure
- **Error Handling:** Graceful failure recovery
- **User Control:** Easy to stop anytime (Ctrl+C)

### Best Practices
- **Start Small:** Begin with 3-5 applications
- **Review Profile:** Ensure it's complete and updated
- **Monitor Results:** Check email and dashboard
- **Use Responsibly:** Don't spam applications
- **Regular Updates:** Keep scripts updated

## 🔧 Troubleshooting

### Common Issues

**Browser doesn't open:**
```bash
# Test WebDriver setup
python3 test_webdriver.py

# Update Chrome browser
# Restart computer
```

**No jobs found:**
- Check if logged in properly
- Try different search terms
- Verify internet connection

**Applications not working:**
- Ensure profile is complete
- Check for Naukri site changes
- Try manual application first

**Script hangs:**
- Press Ctrl+C to stop
- Check internet connection
- Restart and try again

## 📈 Success Tips

### Maximize Application Success
1. **Profile Optimization:**
   - Complete all sections
   - Use relevant keywords
   - Upload recent photo
   - Add portfolio links

2. **Resume Quality:**
   - Highlight iOS experience
   - Include Swift/Objective-C skills
   - Mention published apps
   - Add relevant certifications

3. **Strategic Application:**
   - Apply during business hours
   - Target companies in your preferred location
   - Follow up on applications
   - Customize applications when possible

## 🆚 Comparison: Simple vs Full Version

| Feature | Simple Version | Full Version |
|---------|----------------|---------------|
| Setup Difficulty | Easy | Moderate |
| Job Search | Basic iOS search | Multiple keywords |
| Filtering | Basic relevance | Advanced filtering |
| History Tracking | Session only | Persistent storage |
| Location Filter | No | Yes |
| Experience Filter | No | Yes |
| Application Limit | Per session | Configurable |
| Error Recovery | Basic | Advanced |
| Reporting | Simple summary | Detailed analytics |

## 📞 Support

If you encounter issues:
1. Run the diagnostic script: `python3 test_webdriver.py`
2. Check the troubleshooting section above
3. Ensure all dependencies are installed
4. Verify Chrome browser is updated

## ⚖️ Legal & Ethical Use

- Use responsibly and ethically
- Respect Naukri.com's terms of service
- Don't spam applications
- Review applications manually
- Keep your profile and resume updated
- Use for legitimate job searching only

## 🎉 Success Stories

This automation suite helps you:
- **Save Time:** Apply to multiple jobs quickly
- **Stay Consistent:** Regular profile activity
- **Increase Visibility:** More applications = more opportunities
- **Track Progress:** Monitor application history
- **Focus on Quality:** Spend time on interview prep instead of manual applications

---

**Happy Job Hunting! 🎯**

Remember: Automation is a tool to help you apply more efficiently, but the quality of your profile, resume, and interview skills ultimately determine your success. Use this time saved to improve your technical skills and prepare for interviews!