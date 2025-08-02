// Background service worker for Naukri Activity Booster extension

let isActive = false;
let currentTabId = null;
let activityInterval = 5; // minutes
let activityMode = 'stealth';
let nextActivityTime = null;

// Initialize extension
chrome.runtime.onInstalled.addListener(() => {
    console.log('Naukri Activity Booster installed');
    
    // Initialize storage
    chrome.storage.local.set({
        isActive: false,
        totalActivities: 0,
        successfulActivities: 0,
        failedActivities: 0,
        lastActivity: 'Never'
    });
    
    chrome.storage.sync.set({
        interval: 5,
        mode: 'stealth'
    });
});

// Handle messages from popup and content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    switch (request.action) {
        case 'start':
            startActivityBooster(request.tabId)
                .then(() => sendResponse({success: true}))
                .catch(() => sendResponse({success: false}));
            return true; // Keep message channel open for async response
            
        case 'stop':
            stopActivityBooster()
                .then(() => sendResponse({success: true}))
                .catch(() => sendResponse({success: false}));
            return true;
            
        case 'updateSettings':
            updateSettings(request.settings);
            sendResponse({success: true});
            break;
            
        case 'performActivity':
            handleActivityResult(request.success, request.message);
            sendResponse({success: true});
            break;
            
        case 'getStatus':
            sendResponse({
                isActive: isActive,
                nextActivityTime: nextActivityTime,
                interval: activityInterval,
                mode: activityMode
            });
            break;
            
        case 'testActivity':
            // Immediate test without waiting for alarm
            if (currentTabId) {
                chrome.tabs.sendMessage(currentTabId, {
                    action: 'performActivity',
                    mode: activityMode || 'normal'
                }).then(() => {
                    sendResponse({success: true, message: 'Test activity sent'});
                }).catch((error) => {
                    sendResponse({success: false, message: error.message});
                });
            } else {
                sendResponse({success: false, message: 'No active tab'});
            }
            return true;
            break;
    }
});

// Handle alarm events for scheduled activities
chrome.alarms.onAlarm.addListener((alarm) => {
    if (alarm.name === 'naukriActivity') {
        performScheduledActivity();
    }
});

async function startActivityBooster(tabId) {
    try {
        // Load settings
        const settings = await chrome.storage.sync.get(['interval', 'mode']);
        activityInterval = settings.interval || 5;
        activityMode = settings.mode || 'stealth';
        
        isActive = true;
        currentTabId = tabId;
        
        // Update storage
        await chrome.storage.local.set({
            isActive: true,
            currentTabId: tabId
        });
        
        // Schedule first activity
        scheduleNextActivity();
        
        console.log('Activity Booster started');
        return true;
    } catch (error) {
        console.error('Failed to start Activity Booster:', error);
        throw error;
    }
}

async function stopActivityBooster() {
    try {
        isActive = false;
        currentTabId = null;
        nextActivityTime = null;
        
        // Clear any scheduled alarms
        await chrome.alarms.clear('naukriActivity');
        
        // Update storage
        await chrome.storage.local.set({
            isActive: false,
            currentTabId: null,
            nextActivityTime: null
        });
        
        console.log('Activity Booster stopped');
        return true;
    } catch (error) {
        console.error('Failed to stop Activity Booster:', error);
        throw error;
    }
}

function updateSettings(settings) {
    activityInterval = settings.interval;
    activityMode = settings.mode;
    
    // If active, reschedule with new interval
    if (isActive) {
        scheduleNextActivity();
    }
}

function scheduleNextActivity() {
    if (!isActive) return;
    
    // Add random variation (±20%) to make it more human-like
    const variation = 0.8 + (Math.random() * 0.4); // 0.8 to 1.2
    const actualInterval = Math.round(activityInterval * variation);
    
    // Calculate next activity time
    nextActivityTime = new Date(Date.now() + (actualInterval * 60 * 1000));
    
    // Clear existing alarm and create new one
    chrome.alarms.clear('naukriActivity').then(() => {
        chrome.alarms.create('naukriActivity', {
            delayInMinutes: actualInterval
        });
    });
    
    // Update storage
    chrome.storage.local.set({
        nextActivityTime: nextActivityTime.toISOString()
    });
    
    console.log(`Next activity scheduled for ${nextActivityTime.toLocaleTimeString()}`);
}

async function performScheduledActivity() {
    if (!isActive || !currentTabId) {
        console.log('Activity cancelled - booster not active');
        return;
    }
    
    try {
        // Check if tab still exists and is on Naukri
        const tab = await chrome.tabs.get(currentTabId);
        
        if (!tab.url.includes('naukri.com')) {
            console.log('Tab is no longer on Naukri - stopping booster');
            await stopActivityBooster();
            return;
        }
        
        // Send message to content script to perform activity
        chrome.tabs.sendMessage(currentTabId, {
            action: 'performActivity',
            mode: activityMode
        }).catch((error) => {
            console.log('Failed to send message to content script:', error);
            // Try to inject content script if it's not loaded
            injectContentScript();
        });
        
    } catch (error) {
        console.error('Error performing scheduled activity:', error);
        
        // If tab doesn't exist, stop the booster
        if (error.message.includes('No tab with id')) {
            await stopActivityBooster();
        }
    }
}

async function injectContentScript() {
    try {
        await chrome.scripting.executeScript({
            target: { tabId: currentTabId },
            files: ['content.js']
        });
        
        // Retry the activity after a short delay
        setTimeout(() => {
            chrome.tabs.sendMessage(currentTabId, {
                action: 'performActivity',
                mode: activityMode
            });
        }, 1000);
        
    } catch (error) {
        console.error('Failed to inject content script:', error);
    }
}

async function handleActivityResult(success, message) {
    try {
        // Update statistics
        const stats = await chrome.storage.local.get([
            'totalActivities',
            'successfulActivities',
            'failedActivities'
        ]);
        
        const newStats = {
            totalActivities: (stats.totalActivities || 0) + 1,
            lastActivity: new Date().toLocaleString()
        };
        
        if (success) {
            newStats.successfulActivities = (stats.successfulActivities || 0) + 1;
        } else {
            newStats.failedActivities = (stats.failedActivities || 0) + 1;
        }
        
        await chrome.storage.local.set(newStats);
        
        console.log(`Activity completed: ${success ? 'Success' : 'Failed'} - ${message}`);
        
        // Schedule next activity
        scheduleNextActivity();
        
        // Notify popup if it's open
        chrome.runtime.sendMessage({
            action: 'updateStats'
        }).catch(() => {
            // Popup might not be open, ignore error
        });
        
    } catch (error) {
        console.error('Error handling activity result:', error);
    }
}

// Handle tab updates to check if user navigated away from Naukri
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (tabId === currentTabId && changeInfo.url && !changeInfo.url.includes('naukri.com')) {
        console.log('User navigated away from Naukri - stopping booster');
        stopActivityBooster();
    }
});

// Handle tab removal
chrome.tabs.onRemoved.addListener((tabId) => {
    if (tabId === currentTabId) {
        console.log('Naukri tab closed - stopping booster');
        stopActivityBooster();
    }
});

// Restore state on startup
chrome.runtime.onStartup.addListener(async () => {
    try {
        const state = await chrome.storage.local.get([
            'isActive',
            'currentTabId',
            'nextActivityTime'
        ]);
        
        if (state.isActive && state.currentTabId) {
            isActive = state.isActive;
            currentTabId = state.currentTabId;
            
            // Check if the scheduled time has passed
            if (state.nextActivityTime) {
                const scheduledTime = new Date(state.nextActivityTime);
                const now = new Date();
                
                if (now >= scheduledTime) {
                    // Perform activity immediately
                    performScheduledActivity();
                } else {
                    // Reschedule for the remaining time
                    const remainingMinutes = Math.ceil((scheduledTime - now) / 60000);
                    chrome.alarms.create('naukriActivity', {
                        delayInMinutes: remainingMinutes
                    });
                }
            }
        }
    } catch (error) {
        console.error('Error restoring state:', error);
    }
});