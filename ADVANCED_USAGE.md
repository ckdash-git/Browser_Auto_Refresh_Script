# 🚀 Advanced Naukri Job Auto-Apply with Form Filling

## 🎯 What's New in the Advanced Script

The `naukri_job_apply_advanced.py` script is the most sophisticated version that can:

✅ **Automatically fill application forms** with your personal details  
✅ **Handle both Naukri and company website applications**  
✅ **Calculate your experience dynamically** from your start date  
✅ **Prioritize recently posted jobs**  
✅ **Fill complex form fields** like salary, location, notice period  

## 🔍 SEARCH CRITERIA:

| Criteria | Value |
|----------|-------|
| **Experience Range** | 1-4 years (flexible matching) |
| **Location** | All over India (no restrictions) |
| **Posted Date** | Few minutes to last 7 days |
| **Job Type** | iOS/Mobile development roles |
| **Salary Filter** | None (applies to all positions) |

## 📋 Your Pre-configured Details:

| Field | Value |
|-------|---------|
| **Job Start Date** | March 11, 2024 |
| **Current Experience** | Dynamically calculated (currently ~1 year 4 months) |
| **Current Location** | Bangalore |
| **Current Company** | CACHATTO India Pvt Limited |
| **Current Salary** | ₹240,000 |
| **Expected Salary** | ₹450,000 |
| **Notice Period** | 30 days |
| **Willing to Relocate** | Yes |

## 🛠️ Installation

### Step 1: Install Dependencies
```bash
pip3 install -r requirements_advanced.txt
```

### Step 2: Enable Safari Developer Features
**Important**: Safari requires special setup for automation:

1. **Enable Develop Menu**:
   - Safari → Preferences → Advanced
   - Check "Show Develop menu in menu bar"

2. **Enable Remote Automation**:
   - Develop → Allow Remote Automation

### Step 3: Test Safari Setup
```bash
python3 test_safari_setup.py
```
This will verify that Safari is properly configured for automation.

## 🚀 Usage

### Step 1: Safari Setup
**Important**: Ensure Safari Developer features are enabled (see installation step 2).

### Step 2: Run the Script
```bash
python3 naukri_job_apply_advanced.py
```

### Step 3: Provide Contact Information
The script will ask for:
- Your phone number
- Your email address

### Step 4: Safari Browser & Login
- Script opens Safari browser with automation
- Uses your system login sessions if available
- If not logged in to Naukri, you'll be prompted to log in manually
- Login session will be maintained during the script run

### Step 5: Automated Application
The script will:
1. Search for iOS developer jobs (1-4 years exp, All India, Last 7 days)
2. Filter suitable positions based on experience and relevance
3. Apply to jobs automatically with intelligent form filling
4. Handle both Naukri forms and external company websites
5. Skip salary filtering - applies to all suitable positions

## 🎛️ How It Works

### Form Field Detection
The script automatically detects and fills:

- **Experience fields**: Uses calculated experience from March 11, 2024
- **Salary fields**: Current (₹240,000) and Expected (₹450,000)
- **Location fields**: Bangalore
- **Notice period**: 30 days
- **Relocation**: Yes
- **Contact info**: Phone and email you provide

### Application Types Handled

1. **"Apply" Button**: Standard Naukri applications
   - Fills popup forms
   - Handles dropdown selections
   - Submits automatically

2. **"Apply on Company Website" Button**: External applications
   - Redirects to company website
   - Detects and fills external forms
   - Attempts automatic submission

### Recent Jobs Priority
The script prioritizes jobs posted:
- Today
- Last 3 days
- Last 7 days

## 📊 What You'll See

### Real-time Progress
```
🔍 Searching for recent iOS developer jobs...
📋 Found 15 job listings
📝 Processing job 1...
   📌 Job: iOS Developer
   🏢 Company: Tech Solutions
   📍 Location: Bangalore
   📅 Posted: 2 days ago
   🔘 Found button: Apply
   📝 Naukri application form
   ✏️ Filling application form...
   ✅ Filled experience: 1
   ✅ Filled current_salary: 240000
   ✅ Filled expected_salary: 450000
   ✅ Selected willing to relocate: Yes
   ✅ Application submitted!
   ✅ Applied successfully! (1/5)
```

### Session Summary
```
============================================================
📊 APPLICATION SESSION SUMMARY
============================================================
🔍 Jobs Found: 15
✅ Applications Sent: 5
⏭️ Jobs Skipped: 10
👤 Experience: 1 years 5 months
📍 Location: Bangalore
💰 Expected Salary: ₹450000
============================================================
🎉 Applications submitted successfully!
📧 Check your email for confirmations.
💼 Monitor your Naukri dashboard for responses.
📱 Follow up with companies if needed.
```

## ⚙️ Customization

To modify your details, edit the `personal_info` dictionary in the script:

```python
self.personal_info = {
    'job_start_date': datetime(2024, 3, 11),  # Your start date
    'current_location': 'Bangalore',          # Your city
    'current_company': 'CACHATTO India Pvt Limited',
    'current_salary': '240000',               # Current salary
    'expected_salary': '450000',              # Expected salary
    'notice_period': '30',                    # Notice period in days
    'willing_to_relocate': True,              # True/False
}
```

## 🔧 Troubleshooting

### Safari Browser Issues

1. **"Safari cannot be automated" or permission errors**
   - Enable Develop menu: Safari → Preferences → Advanced → Show Develop menu
   - Enable Remote Automation: Develop → Allow Remote Automation
   - Restart Safari after enabling these settings

2. **Safari Automation Alert ("This Safari window is remotely controlled")**
   - **Option 1 (Recommended)**: Click "Continue Session" and proceed with manual login
   - **Option 2**: Click "Stop Session", log in to Naukri normally, then run script again
   - **Option 3**: Use the Chrome version (`naukri_job_apply_simple.py`) instead

3. **Browser won't open or automation fails**
   - Ensure Safari Developer features are enabled
   - Check that Safari is updated to latest version
   - Try manually opening Safari first to ensure it works

4. **Login blocked during automation**
   - Safari may block manual login during automation
   - Choose "Continue Session" when prompted by the script
   - Follow the on-screen instructions for login options

5. **Login not detected**
   - Manually log in to Naukri when prompted
   - Script will detect login status automatically
   - Your session will be maintained during the script run

### Application Issues

1. **Form not filled**: Some company websites have unique forms
   - Script will attempt basic filling
   - Manual completion may be needed

2. **External redirects**: Company websites vary
   - Script handles common patterns
   - Some sites may require manual intervention

3. **Captcha/Security**: Some sites have protection
   - Complete manually when prompted
   - Script will continue after

4. **Experience range mismatch**: Jobs requiring 5+ years
   - Script filters for 1-4 years experience
   - Manually apply to higher experience roles if interested

### Tips for Best Results

1. **Use during business hours** (9 AM - 6 PM) for better response
2. **Start with 3-5 applications** to test
3. **Monitor your email** for application confirmations
4. **Check Naukri dashboard** for application status
5. **Follow up** with companies after 2-3 days

## 📈 Success Tips

1. **Keep your Naukri profile updated** before running
2. **Upload latest resume** to your profile
3. **Add relevant skills** (Swift, iOS, Xcode, etc.)
4. **Set profile to "Actively looking"**
5. **Run script during peak posting times** (Monday-Wednesday mornings)

## 🚨 Important Notes

- **Respect rate limits**: Don't apply to too many jobs at once
- **Quality over quantity**: Better to apply to fewer, relevant jobs
- **Monitor responses**: Follow up on applications
- **Keep learning**: Improve skills based on job requirements
- **Be patient**: Job hunting takes time

## 📞 Support

If you encounter issues:
1. Run `python3 test_safari_setup.py` to verify Safari configuration
2. Verify Safari Developer features are enabled
3. Check Safari version and update if needed
4. Ensure stable internet connection
5. Try with fewer applications first

Happy job hunting! 🎉