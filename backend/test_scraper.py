#!/usr/bin/env python3
"""
Quick test script for job scraper
"""

from job_scraper import JobScraper
from db_utils import JobDatabase
import time

def test_scraper():
    print("🧪 Testing Job Scraper...")
    print("=" * 50)
    
    # Initialize scraper
    scraper = JobScraper()
    
    # Test with minimal data
    test_keywords = ["python developer"]
    test_locations = ["Cape Town"]
    
    print(f"Testing with keywords: {test_keywords}")
    print(f"Testing with locations: {test_locations}")
    print()
    
    # Test Spane4all scraper (quick test)
    print("📊 Testing Spane4all scraper...")
    start_time = time.time()
    try:
        spane4all_jobs = scraper.scrape_spane4all_jobs()
        spane4all_time = time.time() - start_time
        print(f"✅ Spane4all: Found {len(spane4all_jobs)} jobs in {spane4all_time:.2f} seconds")
        
        if spane4all_jobs:
            print("Sample job:")
            job = spane4all_jobs[0]
            print(f"  Title: {job.title}")
            print(f"  Company: {job.company}")
            print(f"  Location: {job.location}")
            print(f"  URL: {job.job_url}")
    except Exception as e:
        print(f"❌ Spane4all failed: {e}")
    
    print()
    
    # Test Indeed scraper (quick test)
    print("📊 Testing Indeed scraper...")
    start_time = time.time()
    try:
        indeed_jobs = scraper.scrape_indeed_jobs(test_keywords, test_locations)
        indeed_time = time.time() - start_time
        print(f"✅ Indeed: Found {len(indeed_jobs)} jobs in {indeed_time:.2f} seconds")
        
        if indeed_jobs:
            print("Sample job:")
            job = indeed_jobs[0]
            print(f"  Title: {job.title}")
            print(f"  Company: {job.company}")
            print(f"  Location: {job.location}")
            print(f"  URL: {job.job_url}")
    except Exception as e:
        print(f"❌ Indeed failed: {e}")
    
    print()
    
    # Test database
    print("🗄️ Testing database...")
    db = JobDatabase()
    stats = db.get_stats()
    print(f"✅ Database stats: {stats}")
    
    # Test saving jobs
    all_jobs = []
    if spane4all_jobs:
        all_jobs.extend(spane4all_jobs)
    if indeed_jobs:
        all_jobs.extend(indeed_jobs)
        
    if all_jobs:
        print("💾 Testing job saving...")
        saved_count = scraper.save_job_listings(all_jobs)
        print(f"✅ Saved {saved_count} jobs to database")
        
        # Check updated stats
        updated_stats = db.get_stats()
        print(f"✅ Updated stats: {updated_stats}")
    
    print()
    print("🎉 Test completed!")
    print("=" * 50)

if __name__ == "__main__":
    test_scraper() 