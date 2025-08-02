# Naukri Profile Activity Booster - Browser Extension

A completely undetectable browser extension that automatically maintains activity on your Naukri.com profile by intelligently clicking "Edit" and "Save" buttons at customizable intervals.

## 🚀 Features

### ✅ **100% Undetectable**
- No automation detection alerts
- Human-like behavior simulation
- Random timing variations
- Natural mouse movements
- Smart scrolling patterns

### 🎯 **Intelligent Activity**
- Automatically finds Edit buttons using multiple strategies
- Clicks Edit → Save in sequence
- Handles different page layouts
- Error recovery and retry logic
- Activity statistics tracking

### ⚙️ **Customizable Settings**
- **Interval**: 1-60 minutes between activities
- **Mode**: Stealth, Normal, or Aggressive
- **Statistics**: Track successful/failed activities
- **Auto-stop**: When navigating away from Naukri

### 🛡️ **Safe & Reliable**
- Only works on Naukri.com pages
- Automatically stops if tab is closed
- No data collection or tracking
- Lightweight and efficient

## 📦 Installation

### Method 1: Load as Unpacked Extension (Recommended)

1. **Download the Extension**
   - Download all files to a folder named `naukri-activity-booster`
   - Or clone this repository

2. **Open Chrome Extensions**
   - Go to `chrome://extensions/`
   - Or Menu → More Tools → Extensions

3. **Enable Developer Mode**
   - Toggle "Developer mode" in the top-right corner

4. **Load Extension**
   - Click "Load unpacked"
   - Select the `browser_extension` folder
   - Extension will appear in your extensions list

5. **Pin Extension**
   - Click the puzzle piece icon in Chrome toolbar
   - Pin "Naukri Profile Activity Booster" for easy access

### Method 2: Create Extension Package

1. **Zip the Extension**
   ```bash
   cd browser_extension
   zip -r naukri-activity-booster.zip .
   ```

2. **Load in Developer Mode**
   - Follow steps 2-4 from Method 1
   - Select the zip file instead of folder

## 🎮 Usage

### Quick Start

1. **Navigate to Your Naukri Profile**
   - Go to `https://www.naukri.com/mnjuser/profile`
   - Make sure you're logged in

2. **Open Extension**
   - Click the extension icon in Chrome toolbar
   - Or use the keyboard shortcut `Ctrl+Shift+N` (Windows) / `Cmd+Shift+N` (Mac)

3. **Configure Settings**
   - **Activity Interval**: Choose 3-10 minutes (recommended: 5 minutes)
   - **Activity Mode**: 
     - **Stealth** (recommended): Maximum human-like behavior
     - **Normal**: Balanced speed and stealth
     - **Aggressive**: Fastest execution

4. **Start Activity Booster**
   - Click "Start Activity Booster"
   - Extension will show "Active" status
   - First activity will occur after the set interval

5. **Monitor Progress**
   - View next activity time
   - Check activity statistics
   - Monitor success/failure rates

### Advanced Usage

#### Activity Modes Explained

| Mode | Delay Range | Scroll Chance | Best For |
|------|-------------|---------------|----------|
| **Stealth** | 1-3 seconds | 30% | Maximum undetectability |
| **Normal** | 0.5-1.5 seconds | 10% | Balanced performance |
| **Aggressive** | 0.1-0.5 seconds | 5% | Quick testing |

#### Optimal Settings

**For Job Seekers (Active Search):**
- Interval: 3-5 minutes
- Mode: Stealth
- Duration: During business hours

**For Passive Candidates:**
- Interval: 5-10 minutes
- Mode: Stealth
- Duration: Throughout the day

**For Testing:**
- Interval: 1-2 minutes
- Mode: Normal
- Duration: Short periods

## 📊 Understanding Statistics

### Activity Metrics
- **Total Activities**: Number of edit-save cycles attempted
- **Successful**: Activities completed without errors
- **Failed**: Activities that encountered issues
- **Success Rate**: Percentage of successful activities
- **Last Activity**: Timestamp of most recent activity

### Common Success Rates
- **95-100%**: Excellent - Extension working perfectly
- **85-94%**: Good - Minor page loading issues
- **70-84%**: Fair - May need different mode or interval
- **Below 70%**: Poor - Check page compatibility

## 🔧 Troubleshooting

### Extension Not Working

**Problem**: Extension icon is grayed out
- **Solution**: Make sure you're on a Naukri.com page
- **Check**: URL should contain "naukri.com"

**Problem**: "Start" button is disabled
- **Solution**: Refresh the Naukri page and try again
- **Check**: Make sure you're logged into Naukri

### Low Success Rate

**Problem**: Many failed activities
- **Try**: Switch to "Stealth" mode
- **Try**: Increase interval to 5-10 minutes
- **Check**: Ensure profile page has editable sections

**Problem**: No Edit buttons found
- **Solution**: Navigate to your complete profile page
- **URL**: `https://www.naukri.com/mnjuser/profile`
- **Check**: Make sure profile sections are visible

### Browser Issues

**Problem**: Extension disappeared
- **Solution**: Check `chrome://extensions/` and re-enable
- **Check**: Make sure Developer Mode is still enabled

**Problem**: Chrome shows automation warning
- **This shouldn't happen**: Extension is designed to be undetectable
- **If it does**: Try "Stealth" mode with longer intervals

## 🎯 Best Practices

### ✅ Do's
- Use "Stealth" mode for maximum safety
- Set intervals between 3-10 minutes
- Monitor statistics regularly
- Keep Chrome updated
- Use during active job searching

### ❌ Don'ts
- Don't use intervals shorter than 1 minute
- Don't run on multiple Naukri tabs simultaneously
- Don't use "Aggressive" mode for extended periods
- Don't leave running 24/7 unnecessarily

### 🔒 Privacy & Security
- Extension only works on Naukri.com
- No data is collected or transmitted
- No login credentials are accessed
- All activity happens locally in your browser

## 🆚 Extension vs Python Script Comparison

| Feature | Browser Extension | Python Script |
|---------|------------------|---------------|
| **Detection Risk** | None | High (automation alerts) |
| **Installation** | Simple (few clicks) | Complex (dependencies) |
| **User Experience** | Native browser UI | Command line |
| **Resource Usage** | Minimal | Higher (separate browser) |
| **Reliability** | High | Medium |
| **Customization** | GUI settings | Code modification |
| **Cross-platform** | Chrome only | Windows/Mac/Linux |

## 🔄 Updates & Maintenance

### Automatic Updates
- Extension updates automatically when published to Chrome Web Store
- For unpacked extensions, manually replace files and reload

### Manual Updates
1. Download new version
2. Replace old files
3. Go to `chrome://extensions/`
4. Click reload button for the extension

## 🐛 Known Issues & Limitations

### Current Limitations
- Only works with Chrome browser
- Requires manual installation (not on Chrome Web Store)
- May need updates if Naukri changes their page structure

### Planned Improvements
- Firefox support
- Chrome Web Store publication
- Enhanced button detection
- Activity scheduling

## 📞 Support

### Getting Help
1. Check this README for common solutions
2. Verify you're using the latest version
3. Test with different settings (mode/interval)
4. Check browser console for error messages

### Reporting Issues
When reporting issues, please include:
- Chrome version
- Extension version
- Naukri page URL
- Error messages (if any)
- Steps to reproduce

## 📄 License

This extension is provided as-is for educational and personal use. Use responsibly and in accordance with Naukri.com's terms of service.

---

**🎉 Enjoy your enhanced Naukri profile visibility!**

*Keep your profile active, increase your visibility, and never miss opportunities!*