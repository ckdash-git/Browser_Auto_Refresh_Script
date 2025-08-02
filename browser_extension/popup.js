// Popup script for Naukri Activity Booster extension

document.addEventListener('DOMContentLoaded', function() {
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    const testBtn = document.getElementById('testBtn');
    const statusIndicator = document.getElementById('statusIndicator');
    const statusText = document.getElementById('statusText');
    const intervalSelect = document.getElementById('interval');
    const modeSelect = document.getElementById('mode');
    const notification = document.getElementById('notification');
    const totalActivities = document.getElementById('totalActivities');
    const lastActivity = document.getElementById('lastActivity');
    const nextActivity = document.getElementById('nextActivity');
    const successRate = document.getElementById('successRate');
    
    // Load saved settings and stats
    loadSettings();
    loadStats();
    updateStatus();
    
    // Event listeners
    startBtn.addEventListener('click', startActivityBooster);
    stopBtn.addEventListener('click', stopActivityBooster);
    testBtn.addEventListener('click', testActivity);
    intervalSelect.addEventListener('change', saveSettings);
    modeSelect.addEventListener('change', saveSettings);
    
    // Update stats every second
    setInterval(updateStats, 1000);
    
    function loadSettings() {
        chrome.storage.sync.get(['interval', 'mode'], function(result) {
            if (result.interval) {
                intervalSelect.value = result.interval;
            }
            if (result.mode) {
                modeSelect.value = result.mode;
            }
        });
    }
    
    function saveSettings() {
        const settings = {
            interval: parseInt(intervalSelect.value),
            mode: modeSelect.value
        };
        
        chrome.storage.sync.set(settings, function() {
            showNotification('Settings saved!');
            
            // Update background script with new settings
            chrome.runtime.sendMessage({
                action: 'updateSettings',
                settings: settings
            });
        });
    }
    
    function loadStats() {
        chrome.storage.local.get([
            'totalActivities',
            'lastActivity',
            'successfulActivities',
            'failedActivities'
        ], function(result) {
            totalActivities.textContent = result.totalActivities || 0;
            lastActivity.textContent = result.lastActivity || 'Never';
            
            const total = (result.successfulActivities || 0) + (result.failedActivities || 0);
            if (total > 0) {
                const rate = Math.round((result.successfulActivities || 0) / total * 100);
                successRate.textContent = rate + '%';
            } else {
                successRate.textContent = '-';
            }
        });
    }
    
    function updateStatus() {
        chrome.storage.local.get(['isActive', 'nextActivityTime'], function(result) {
            const isActive = result.isActive || false;
            
            if (isActive) {
                statusIndicator.className = 'status-indicator status-active';
                statusText.textContent = 'Active';
                startBtn.classList.add('hidden');
                stopBtn.classList.remove('hidden');
                
                // Update next activity time
                if (result.nextActivityTime) {
                    const nextTime = new Date(result.nextActivityTime);
                    const now = new Date();
                    const diff = nextTime - now;
                    
                    if (diff > 0) {
                        const minutes = Math.floor(diff / 60000);
                        const seconds = Math.floor((diff % 60000) / 1000);
                        nextActivity.textContent = `${minutes}m ${seconds}s`;
                    } else {
                        nextActivity.textContent = 'Soon';
                    }
                } else {
                    nextActivity.textContent = 'Calculating...';
                }
            } else {
                statusIndicator.className = 'status-indicator status-inactive';
                statusText.textContent = 'Inactive';
                startBtn.classList.remove('hidden');
                stopBtn.classList.add('hidden');
                nextActivity.textContent = '-';
            }
        });
    }
    
    function updateStats() {
        loadStats();
        updateStatus();
    }
    
    function startActivityBooster() {
        // Check if we're on a Naukri page
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            const currentTab = tabs[0];
            
            if (!currentTab.url.includes('naukri.com')) {
                showNotification('Please navigate to your Naukri profile page first!', 'error');
                return;
            }
            
            // Save settings first
            saveSettings();
            
            // Start the activity booster
            chrome.runtime.sendMessage({
                action: 'start',
                tabId: currentTab.id
            }, function(response) {
                if (response && response.success) {
                    showNotification('Activity Booster started successfully!');
                    updateStatus();
                } else {
                    showNotification('Failed to start Activity Booster', 'error');
                }
            });
        });
    }
    
    function stopActivityBooster() {
        chrome.runtime.sendMessage({
            action: 'stop'
        }, function(response) {
            if (response && response.success) {
                showNotification('Activity Booster stopped');
                updateStatus();
            } else {
                showNotification('Failed to stop Activity Booster', 'error');
            }
        });
    }
    
    function testActivity() {
        // Check if we're on a Naukri page
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            const currentTab = tabs[0];
            
            if (!currentTab.url.includes('naukri.com')) {
                showNotification('Please navigate to your Naukri profile page first!', 'error');
                return;
            }
            
            showNotification('Testing activity... Check console for details');
            
            // Send test message to background script
            chrome.runtime.sendMessage({
                action: 'testActivity'
            }, function(response) {
                if (response && response.success) {
                    showNotification('Test activity completed! Check console for results');
                } else {
                    showNotification('Test failed: ' + (response ? response.message : 'Unknown error'), 'error');
                }
            });
        });
    }
    
    function showNotification(message, type = 'success') {
        notification.textContent = message;
        notification.className = `notification ${type === 'error' ? 'error' : ''}`;
        notification.classList.remove('hidden');
        
        setTimeout(() => {
            notification.classList.add('hidden');
        }, 3000);
    }
    
    // Listen for messages from background script
    chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
        if (request.action === 'updateStats') {
            loadStats();
        } else if (request.action === 'showNotification') {
            showNotification(request.message, request.type);
        }
    });
});