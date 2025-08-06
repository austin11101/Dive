#!/usr/bin/env python3
"""
View scraped jobs from database
"""

from db_utils import JobDatabase

def view_jobs():
    db = JobDatabase()
    jobs = db.search_jobs(limit=10)
    
    print("📋 Scraped Jobs from Database:")
    print("=" * 60)
    
    for i, job in enumerate(jobs, 1):
        print(f"{i}. {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   Source: {job['source_site']}")
        print(f"   Date: {job['posting_date']}")
        print(f"   URL: {job['job_url']}")
        print("-" * 60)
    
    # Show stats
    stats = db.get_stats()
    print(f"\n📊 Database Stats:")
    print(f"Total jobs: {stats['total_jobs']}")
    print(f"Jobs by source: {stats['jobs_by_source']}")
    print(f"Recent jobs (24h): {stats['recent_jobs_24h']}")

if __name__ == "__main__":
    view_jobs() 