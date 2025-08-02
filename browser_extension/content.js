// Content script for Naukri Activity Booster extension
// This script runs on Naukri pages and performs the actual activities

(function() {
    'use strict';
    
    // Configuration
    const config = {
        stealth: {
            minDelay: 1000,
            maxDelay: 3000,
            scrollProbability: 0.3,
            mouseMoveDelay: 500
        },
        normal: {
            minDelay: 500,
            maxDelay: 1500,
            scrollProbability: 0.1,
            mouseMoveDelay: 200
        },
        aggressive: {
            minDelay: 100,
            maxDelay: 500,
            scrollProbability: 0.05,
            mouseMoveDelay: 100
        }
    };
    
    // Utility functions
    function randomDelay(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }
    
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    function simulateHumanMouseMove(element) {
        return new Promise((resolve) => {
            const rect = element.getBoundingClientRect();
            const x = rect.left + (rect.width / 2) + (Math.random() - 0.5) * 20;
            const y = rect.top + (rect.height / 2) + (Math.random() - 0.5) * 10;
            
            // Create mouse events
            const mouseMoveEvent = new MouseEvent('mousemove', {
                bubbles: true,
                cancelable: true,
                clientX: x,
                clientY: y
            });
            
            const mouseOverEvent = new MouseEvent('mouseover', {
                bubbles: true,
                cancelable: true,
                clientX: x,
                clientY: y
            });
            
            element.dispatchEvent(mouseMoveEvent);
            element.dispatchEvent(mouseOverEvent);
            
            setTimeout(resolve, randomDelay(100, 300));
        });
    }
    
    function simulateHumanClick(element) {
        return new Promise(async (resolve) => {
            try {
                // Simulate mouse movement first
                await simulateHumanMouseMove(element);
                
                // Add small delay
                await sleep(randomDelay(200, 500));
                
                // Scroll element into view if needed
                element.scrollIntoView({ behavior: 'smooth', block: 'center' });
                await sleep(300);
                
                // Try different click methods
                let clicked = false;
                
                // Method 1: Native click
                try {
                    element.click();
                    clicked = true;
                } catch (e) {
                    console.log('Native click failed, trying alternatives');
                }
                
                // Method 2: Mouse events
                if (!clicked) {
                    try {
                        const rect = element.getBoundingClientRect();
                        const x = rect.left + (rect.width / 2);
                        const y = rect.top + (rect.height / 2);
                        
                        ['mousedown', 'mouseup', 'click'].forEach(eventType => {
                            const event = new MouseEvent(eventType, {
                                bubbles: true,
                                cancelable: true,
                                clientX: x,
                                clientY: y
                            });
                            element.dispatchEvent(event);
                        });
                        clicked = true;
                    } catch (e) {
                        console.log('Mouse events failed, trying JavaScript click');
                    }
                }
                
                // Method 3: JavaScript click
                if (!clicked) {
                    try {
                        if (element.onclick) {
                            element.onclick();
                        } else {
                            const event = new Event('click', { bubbles: true });
                            element.dispatchEvent(event);
                        }
                        clicked = true;
                    } catch (e) {
                        console.log('JavaScript click failed');
                    }
                }
                
                resolve(clicked);
            } catch (error) {
                console.error('Error in simulateHumanClick:', error);
                resolve(false);
            }
        });
    }
    
    function randomScroll() {
        return new Promise((resolve) => {
            const scrollAmount = randomDelay(100, 300);
            const direction = Math.random() > 0.5 ? 1 : -1;
            
            window.scrollBy({
                top: scrollAmount * direction,
                behavior: 'smooth'
            });
            
            setTimeout(resolve, randomDelay(500, 1000));
        });
    }
    
    // Element finding functions with multiple strategies
    function findEditButtons() {
        const selectors = [
            // Text-based selectors
            'button:contains("Edit")',
            'a:contains("Edit")',
            'span:contains("Edit")',
            
            // Attribute-based selectors
            'button[title*="Edit"]',
            'a[title*="Edit"]',
            'button[aria-label*="Edit"]',
            'a[aria-label*="Edit"]',
            
            // Class-based selectors
            'button[class*="edit"]',
            'a[class*="edit"]',
            'span[class*="edit"]',
            
            // Icon-based selectors
            'i[class*="edit"]',
            'i[class*="pencil"]',
            'svg[class*="edit"]',
            
            // Common patterns
            '.edit-btn',
            '.edit-link',
            '.edit-icon',
            '[data-action="edit"]',
            '[data-testid*="edit"]'
        ];
        
        const elements = [];
        
        // Try CSS selectors first
        selectors.forEach(selector => {
            try {
                if (selector.includes(':contains')) {
                    // Handle :contains pseudo-selector manually
                    const baseSelector = selector.split(':contains')[0];
                    const text = selector.match(/"([^"]*)"/)[1];
                    
                    document.querySelectorAll(baseSelector).forEach(el => {
                        if (el.textContent.toLowerCase().includes(text.toLowerCase())) {
                            elements.push(el);
                        }
                    });
                } else {
                    document.querySelectorAll(selector).forEach(el => {
                        elements.push(el);
                    });
                }
            } catch (e) {
                // Ignore invalid selectors
            }
        });
        
        // Also try XPath selectors
        const xpathSelectors = [
            '//button[contains(text(), "Edit")]',
            '//a[contains(text(), "Edit")]',
            '//span[contains(text(), "Edit")]',
            '//button[contains(@title, "Edit")]',
            '//a[contains(@title, "Edit")]',
            '//button[contains(@class, "edit")]',
            '//a[contains(@class, "edit")]'
        ];
        
        xpathSelectors.forEach(xpath => {
            try {
                const result = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
                for (let i = 0; i < result.snapshotLength; i++) {
                    elements.push(result.snapshotItem(i));
                }
            } catch (e) {
                // Ignore XPath errors
            }
        });
        
        // Filter for visible and enabled elements
        return elements.filter(el => {
            const rect = el.getBoundingClientRect();
            return rect.width > 0 && rect.height > 0 && 
                   !el.disabled && 
                   getComputedStyle(el).display !== 'none' &&
                   getComputedStyle(el).visibility !== 'hidden';
        });
    }
    
    function findSaveButtons() {
        const selectors = [
            // Text-based
            'button:contains("Save")',
            'button:contains("Update")',
            'button:contains("Submit")',
            'a:contains("Save")',
            
            // Attribute-based
            'button[type="submit"]',
            'input[type="submit"]',
            'button[title*="Save"]',
            'button[aria-label*="Save"]',
            
            // Class-based
            'button[class*="save"]',
            'button[class*="submit"]',
            'button[class*="update"]',
            
            // Common patterns
            '.save-btn',
            '.submit-btn',
            '.update-btn',
            '[data-action="save"]',
            '[data-testid*="save"]'
        ];
        
        const elements = [];
        
        selectors.forEach(selector => {
            try {
                if (selector.includes(':contains')) {
                    const baseSelector = selector.split(':contains')[0];
                    const text = selector.match(/"([^"]*)"/)[1];
                    
                    document.querySelectorAll(baseSelector).forEach(el => {
                        if (el.textContent.toLowerCase().includes(text.toLowerCase())) {
                            elements.push(el);
                        }
                    });
                } else {
                    document.querySelectorAll(selector).forEach(el => {
                        elements.push(el);
                    });
                }
            } catch (e) {
                // Ignore invalid selectors
            }
        });
        
        // XPath selectors for save buttons
        const xpathSelectors = [
            '//button[contains(text(), "Save")]',
            '//button[contains(text(), "Update")]',
            '//button[contains(text(), "Submit")]',
            '//input[@type="submit"]',
            '//button[@type="submit"]'
        ];
        
        xpathSelectors.forEach(xpath => {
            try {
                const result = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
                for (let i = 0; i < result.snapshotLength; i++) {
                    elements.push(result.snapshotItem(i));
                }
            } catch (e) {
                // Ignore XPath errors
            }
        });
        
        return elements.filter(el => {
            const rect = el.getBoundingClientRect();
            return rect.width > 0 && rect.height > 0 && 
                   !el.disabled && 
                   getComputedStyle(el).display !== 'none' &&
                   getComputedStyle(el).visibility !== 'hidden';
        });
    }
    
    // Main activity function
    async function performActivity(mode = 'stealth') {
        try {
            console.log(`Starting ${mode} activity on Naukri profile`);
            
            const modeConfig = config[mode] || config.stealth;
            
            // Random initial delay
            await sleep(randomDelay(modeConfig.minDelay, modeConfig.maxDelay));
            
            // Random scroll if configured
            if (Math.random() < modeConfig.scrollProbability) {
                await randomScroll();
            }
            
            // Find edit buttons
            const editButtons = findEditButtons();
            
            if (editButtons.length === 0) {
                console.log('No edit buttons found');
                return { success: false, message: 'No edit buttons found on page' };
            }
            
            // Select a random edit button (more human-like)
            const editButton = editButtons[Math.floor(Math.random() * editButtons.length)];
            console.log('Found edit button:', editButton);
            
            // Click edit button
            const editClicked = await simulateHumanClick(editButton);
            
            if (!editClicked) {
                return { success: false, message: 'Failed to click edit button' };
            }
            
            console.log('Edit button clicked successfully');
            
            // Wait for edit mode to load
            await sleep(randomDelay(modeConfig.minDelay * 2, modeConfig.maxDelay * 2));
            
            // Find save buttons
            const saveButtons = findSaveButtons();
            
            if (saveButtons.length === 0) {
                console.log('No save buttons found after clicking edit');
                
                // Try to escape edit mode
                try {
                    document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
                } catch (e) {
                    // Ignore escape errors
                }
                
                return { success: false, message: 'No save buttons found after edit' };
            }
            
            // Select a save button
            const saveButton = saveButtons[0]; // Usually take the first/primary save button
            console.log('Found save button:', saveButton);
            
            // Click save button
            const saveClicked = await simulateHumanClick(saveButton);
            
            if (!saveClicked) {
                return { success: false, message: 'Failed to click save button' };
            }
            
            console.log('Save button clicked successfully');
            
            // Wait for save to complete
            await sleep(randomDelay(modeConfig.minDelay, modeConfig.maxDelay));
            
            // Optional: Random scroll after activity
            if (Math.random() < modeConfig.scrollProbability) {
                await randomScroll();
            }
            
            return { success: true, message: 'Edit and save completed successfully' };
            
        } catch (error) {
            console.error('Error performing activity:', error);
            return { success: false, message: `Error: ${error.message}` };
        }
    }
    
    // Listen for messages from background script
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
        if (request.action === 'performActivity') {
            console.log('Received activity request with mode:', request.mode);
            
            performActivity(request.mode).then(result => {
                console.log('Activity result:', result);
                
                // Send result back to background script
                chrome.runtime.sendMessage({
                    action: 'performActivity',
                    success: result.success,
                    message: result.message
                });
                
                sendResponse(result);
            }).catch(error => {
                console.error('Activity error:', error);
                
                const errorResult = { success: false, message: error.message };
                
                chrome.runtime.sendMessage({
                    action: 'performActivity',
                    success: false,
                    message: error.message
                });
                
                sendResponse(errorResult);
            });
            
            return true; // Keep message channel open for async response
        }
    });
    
    // Test function to verify extension is working
    function testExtension() {
        console.log('Testing extension functionality...');
        const editButtons = findEditButtons();
        console.log('Found', editButtons.length, 'edit buttons');
        
        if (editButtons.length > 0) {
            console.log('Edit buttons found:', editButtons.map(btn => btn.textContent || btn.title || btn.className));
        } else {
            console.log('No edit buttons found. Checking all buttons on page...');
            const allButtons = document.querySelectorAll('button, a[href], span[onclick], div[onclick]');
            console.log('Total clickable elements:', allButtons.length);
        }
    }
    
    // Initialize content script
    console.log('Naukri Activity Booster content script loaded');
    
    // Test the extension after a short delay
    setTimeout(testExtension, 2000);
    
    // Also test when user manually triggers
    window.testNaukriExtension = testExtension;
    
})();