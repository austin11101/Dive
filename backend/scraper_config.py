#!/usr/bin/env python3
"""
Configuration file for Job Scraper

Modify these settings to customize the scraper behavior
"""

# Database Configuration
DATABASE_PATH = "job_listings.db"

# Rate Limiting (in seconds)
MIN_DELAY = 2
MAX_DELAY = 5

# Search Configuration
DEFAULT_KEYWORDS = [
    "software developer",
    "web developer", 
    "full stack developer",
    "frontend developer",
    "backend developer",
    "python developer",
    "javascript developer",
    "angular developer",
    "react developer",
    "devops engineer",
    "data scientist",
    "machine learning engineer",
    "mobile developer",
    "ios developer",
    "android developer",
    "ui/ux designer",
    "product manager",
    "scrum master",
    "project manager",
    "business analyst"
]

DEFAULT_LOCATIONS = [
    "South Africa",
    "Cape Town",
    "Johannesburg", 
    "Durban",
    "Pretoria",
    "Port Elizabeth",
    "Bloemfontein",
    "Nelspruit",
    "Polokwane",
    "Kimberley",
    "East London",
    "Pietermaritzburg",
    "Rustenburg",
    "Welkom",
    "Vereeniging"
]

# Scraper Limits
MAX_JOBS_PER_SEARCH = 20
MAX_PAGES_PER_SEARCH = 3

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = "job_scraper.log"

# Selenium Configuration
SELENIUM_HEADLESS = True
SELENIUM_TIMEOUT = 30
SELENIUM_WINDOW_SIZE = "1920,1080"

# User Agent Rotation (optional)
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
]

# Proxy Configuration (optional)
USE_PROXIES = False
PROXY_LIST = [
    # Add your proxy servers here if needed
    # "http://proxy1:port",
    # "http://proxy2:port",
]

# Notification Configuration (optional)
ENABLE_NOTIFICATIONS = False
NOTIFICATION_WEBHOOK = ""  # Slack/Discord webhook URL

# Cleanup Configuration
CLEANUP_OLD_JOBS_DAYS = 30  # Remove jobs older than this many days

# Site-specific configurations
SITE_CONFIGS = {
    "indeed": {
        "enabled": True,
        "base_url": "https://za.indeed.com",
        "search_path": "/jobs",
        "max_jobs": 20,
        "delay_multiplier": 1.0
    },
    "linkedin": {
        "enabled": True,
        "base_url": "https://www.linkedin.com",
        "search_path": "/jobs/search",
        "max_jobs": 20,
        "delay_multiplier": 1.5  # LinkedIn is more sensitive
    },
    "spane4all": {
        "enabled": True,
        "base_url": "https://www.spane4all.com",
        "search_path": "/jobs",
        "max_jobs": 20,
        "delay_multiplier": 1.0
    }
} 