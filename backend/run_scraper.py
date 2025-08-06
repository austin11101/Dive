#!/usr/bin/env python3
"""
Simple script to run the job scraper

This script can be used for:
- Manual execution: python run_scraper.py
- Cron jobs: 0 6 * * * /usr/bin/python3 /path/to/run_scraper.py
- Docker containers
- CI/CD pipelines

Exit codes:
- 0: Success
- 1: General error
- 2: Database error
- 3: Network error
"""

import sys
import os
import traceback
from job_scraper import JobScraper
from scraper_config import DEFAULT_KEYWORDS, DEFAULT_LOCATIONS

def main():
    """Main function with proper error handling"""
    try:
        print("Starting job scraper...")
        
        # Initialize scraper
        scraper = JobScraper()
        
        # Run all scrapers
        results = scraper.run_all_scrapers(DEFAULT_KEYWORDS, DEFAULT_LOCATIONS)
        
        # Print summary
        print("\n" + "="*50)
        print("JOB SCRAPING SUMMARY")
        print("="*50)
        print(f"Indeed jobs found: {results.get('Indeed_found', 0)}")
        print(f"LinkedIn jobs found: {results.get('LinkedIn_found', 0)}")
        print(f"Spane4all jobs found: {results.get('Spane4all_found', 0)}")
        print(f"Total jobs found: {results.get('total_found', 0)}")
        print(f"New jobs saved: {results.get('total_saved', 0)}")
        print(f"Duration: {results.get('duration_seconds', 0):.2f} seconds")
        print("="*50)
        
        # Exit with success
        sys.exit(0)
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        traceback.print_exc()
        sys.exit(2)
        
    except requests.RequestException as e:
        print(f"Network error: {e}")
        traceback.print_exc()
        sys.exit(3)
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 