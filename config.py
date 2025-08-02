#!/usr/bin/env python3
"""
Configuration file for Auto Web Page Refresher

You can modify these default values to customize the behavior of the script.
"""

# Default configuration settings
CONFIG = {
    # Default refresh interval in minutes
    'default_refresh_interval': 5,
    
    # Default URL (leave empty to always prompt user)
    'default_url': '',
    
    # Browser window settings
    'window_width': 1920,
    'window_height': 1080,
    
    # Chrome browser options
    'chrome_options': {
        'headless': False,  # Set to True to run browser in background
        'disable_gpu': True,
        'no_sandbox': True,
        'disable_dev_shm_usage': True,
    },
    
    # Retry settings
    'retry_delay': 5,  # seconds to wait before retrying failed refresh
    'max_retries': 3,  # maximum number of retry attempts
    
    # Logging settings
    'show_timestamps': True,
    'show_refresh_counter': True,
    
    # Advanced settings
    'page_load_timeout': 30,  # seconds to wait for page to load
    'implicit_wait': 10,      # seconds for element finding timeout
}

# Predefined URLs for quick access (optional)
QUICK_URLS = {
    '1': 'https://github.com',
    '2': 'https://stackoverflow.com',
    '3': 'https://news.ycombinator.com',
    '4': 'https://reddit.com',
    '5': 'https://twitter.com',
}

# You can add your frequently used URLs here
FAVORITE_URLS = {
    # Example:
    # 'dashboard': 'https://your-dashboard.com',
    # 'monitoring': 'https://your-monitoring-site.com',
}