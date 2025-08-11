"""
Configuration settings for the Dive Job Scraper backend
"""

import os
from typing import List, Dict, Any

class Config:
    """Base configuration"""
    
    # Database settings
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dive_jobs.db")
    
    # API settings
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # CORS settings
    CORS_ORIGINS = [
        "http://localhost:4200",
        "http://localhost:50267",  # Angular dev server alternative port
        "http://127.0.0.1:4200",
        "http://127.0.0.1:50267",
    ]
    
    # Scraping settings
    SCRAPING_ENABLED = os.getenv("SCRAPING_ENABLED", "True").lower() == "true"
    DEFAULT_SCRAPE_LIMIT = int(os.getenv("DEFAULT_SCRAPE_LIMIT", "20"))
    MAX_SCRAPE_LIMIT = int(os.getenv("MAX_SCRAPE_LIMIT", "100"))
    
    # Rate limiting for scraping
    SCRAPE_DELAY_MIN = float(os.getenv("SCRAPE_DELAY_MIN", "1.0"))
    SCRAPE_DELAY_MAX = float(os.getenv("SCRAPE_DELAY_MAX", "3.0"))
    
    # Job sites configuration
    ENABLED_JOB_SITES = [
        "indeed_za",
        "careers24", 
        "pnet",
        "google_jobs",
        "spane4all"
    ]
    
    # South African locations for targeted scraping
    SA_LOCATIONS = [
        "Cape Town, Western Cape",
        "Johannesburg, Gauteng", 
        "Durban, KwaZulu-Natal",
        "Pretoria, Gauteng",
        "Port Elizabeth, Eastern Cape",
        "Bloemfontein, Free State",
        "East London, Eastern Cape",
        "Pietermaritzburg, KwaZulu-Natal",
        "Polokwane, Limpopo",
        "Nelspruit, Mpumalanga",
        "Kimberley, Northern Cape",
        "Mafikeng, North West"
    ]
    
    # Default scraping configurations
    DEFAULT_SCRAPING_CONFIGS = [
        {
            'query': 'software developer',
            'location': 'South Africa',
            'keywords': ['python', 'java', 'javascript', 'react', 'angular'],
            'max_jobs': 30
        },
        {
            'query': 'data scientist',
            'location': 'South Africa', 
            'keywords': ['python', 'machine learning', 'sql', 'analytics'],
            'max_jobs': 20
        },
        {
            'query': 'java developer',
            'location': 'Gauteng',
            'keywords': ['java', 'spring', 'hibernate', 'maven'],
            'max_jobs': 25
        },
        {
            'query': 'sales manager',
            'location': 'Johannesburg',
            'keywords': ['sales', 'business development', 'account management'],
            'max_jobs': 15
        },
        {
            'query': 'accountant',
            'location': 'Cape Town',
            'keywords': ['accounting', 'financial', 'bookkeeping', 'tax'],
            'max_jobs': 15
        },
        {
            'query': 'nurse',
            'location': 'Durban',
            'keywords': ['nursing', 'healthcare', 'medical', 'clinical'],
            'max_jobs': 20
        }
    ]
    
    # Scheduler settings
    SCHEDULER_ENABLED = os.getenv("SCHEDULER_ENABLED", "False").lower() == "true"
    SCRAPE_INTERVAL_HOURS = int(os.getenv("SCRAPE_INTERVAL_HOURS", "6"))
    DAILY_SCRAPE_TIME = os.getenv("DAILY_SCRAPE_TIME", "02:00")
    
    # Logging settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "dive_scraper.log")
    
    # Cache settings
    CACHE_DURATION_HOURS = int(os.getenv("CACHE_DURATION_HOURS", "6"))
    
    # User agent rotation
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    DATABASE_URL = "sqlite:///./dive_jobs_dev.db"

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dive_jobs")
    
    # More restrictive CORS for production
    CORS_ORIGINS = [
        "https://your-production-domain.com",
        "https://www.your-production-domain.com"
    ]
    
    # Production logging
    LOG_LEVEL = "WARNING"

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    DATABASE_URL = "sqlite:///:memory:"
    SCRAPING_ENABLED = False

# Configuration mapping
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name: str = None) -> Config:
    """Get configuration based on environment"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    
    return config_map.get(config_name, DevelopmentConfig)
