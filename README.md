# Auto Web Page Refresher 🔄

A Python script that automatically refreshes any web page at specified intervals using Selenium WebDriver. Perfect for monitoring dashboards, live feeds, or any web content that needs regular updates.

## Features ✨

- 🌐 Works with any website
- ⏰ Customizable refresh intervals (default: 5 minutes)
- 🖥️ Real-time status updates and refresh counter
- 🛡️ Error handling and automatic retry
- 🚀 Easy to use interactive interface
- 🔧 Automatic ChromeDriver management

## Prerequisites 📋

- Python 3.7 or higher
- Google Chrome browser installed
- Internet connection

## Installation 🚀

1. **Clone or download the files** to your desired directory

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install selenium webdriver-manager
   ```

## Usage 💻

1. **Run the script:**
   ```bash
   python auto_refresh.py
   ```

2. **Enter the website URL** when prompted:
   ```
   Enter the URL to refresh: https://example.com
   ```
   
   Note: You can enter URLs with or without `https://` - the script will add it automatically.

3. **Set refresh interval** (optional):
   ```
   Enter refresh interval in minutes (default: 5): 3
   ```
   
   - Press Enter to use default (5 minutes)
   - Enter any positive number for custom interval

4. **Monitor the refreshing:**
   - The script will open Chrome and navigate to your specified URL
   - It will refresh the page automatically at your specified interval
   - Real-time status updates will be shown in the terminal

5. **Stop the script:**
   - Press `Ctrl+C` in the terminal to stop auto-refreshing
   - The browser will close automatically

## Example Output 📊

```
============================================================
🌐 Auto Web Page Refresher
============================================================

Enter the URL to refresh: github.com
Enter refresh interval in minutes (default: 5): 2

✓ Chrome WebDriver initialized successfully
Loading page: https://github.com
✓ Page loaded successfully at 2024-01-15 14:30:00

🔄 Auto-refresh started!
📍 URL: https://github.com
⏰ Refresh interval: 120 seconds (2 minutes)

Press Ctrl+C to stop the auto-refresh

✓ Page refreshed at 2024-01-15 14:32:00
📊 Total refreshes: 1
✓ Page refreshed at 2024-01-15 14:34:00
📊 Total refreshes: 2

🛑 Auto-refresh stopped by user
📊 Total refreshes performed: 2
✓ Browser closed successfully
```

## Use Cases 🎯

- **Dashboard Monitoring:** Keep live dashboards updated
- **Social Media Feeds:** Monitor real-time social media updates
- **News Websites:** Stay updated with breaking news
- **Stock Prices:** Monitor financial markets
- **Server Status Pages:** Keep track of system status
- **Live Sports Scores:** Follow game updates
- **Auction Sites:** Monitor bidding activity

## Troubleshooting 🔧

### Common Issues:

1. **"ChromeDriver not found" error:**
   - The script automatically downloads ChromeDriver
   - Ensure you have a stable internet connection
   - Make sure Chrome browser is installed

2. **"Permission denied" error:**
   - Run the terminal as administrator (Windows) or use `sudo` (Mac/Linux)
   - Check if antivirus is blocking the script

3. **Page won't load:**
   - Check your internet connection
   - Verify the URL is correct and accessible
   - Some websites may block automated access

4. **Script stops unexpectedly:**
   - Check the terminal for error messages
   - Ensure Chrome browser isn't manually closed
   - Restart the script if needed

### Performance Tips:

- **For long-running sessions:** Consider using longer refresh intervals to reduce resource usage
- **Multiple pages:** Run separate instances of the script for different URLs
- **Background running:** The script keeps the browser window open - minimize it to save screen space

## Customization 🛠️

You can modify the script to:
- Add headless mode (browser runs in background)
- Support multiple URLs simultaneously
- Add email notifications on page changes
- Log refresh activities to a file
- Add specific element monitoring instead of full page refresh

## Security Notes 🔒

- The script only refreshes pages and doesn't collect or store any data
- It uses official Selenium WebDriver - no malicious code
- ChromeDriver is downloaded from official Google sources
- Always verify URLs before running to avoid malicious websites

## License 📄

This project is open source and available under the MIT License.

## Support 💬

If you encounter any issues or have suggestions for improvements, feel free to create an issue or contribute to the project!

---

**Happy Refreshing! 🎉**