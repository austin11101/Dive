#!/usr/bin/env python3
"""
Database utilities for job scraper

Provides functions to query, analyze, and manage scraped job data
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import pandas as pd


class JobDatabase:
    """Database utility class for job listings"""
    
    def __init__(self, db_path: str = "job_listings.db"):
        self.db_path = db_path
    
    def get_connection(self):
        """Get database connection with row factory"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total jobs
            cursor.execute("SELECT COUNT(*) FROM job_listings")
            total_jobs = cursor.fetchone()[0]
            
            # Jobs by source
            cursor.execute("""
                SELECT source_site, COUNT(*) as count 
                FROM job_listings 
                GROUP BY source_site
            """)
            jobs_by_source = dict(cursor.fetchall())
            
            # Recent jobs (last 24 hours)
            cursor.execute("""
                SELECT COUNT(*) FROM job_listings 
                WHERE created_at >= datetime('now', '-24 hours')
            """)
            recent_jobs = cursor.fetchone()[0]
            
            # Jobs by location
            cursor.execute("""
                SELECT location, COUNT(*) as count 
                FROM job_listings 
                GROUP BY location 
                ORDER BY count DESC 
                LIMIT 10
            """)
            top_locations = dict(cursor.fetchall())
            
            return {
                "total_jobs": total_jobs,
                "jobs_by_source": jobs_by_source,
                "recent_jobs_24h": recent_jobs,
                "top_locations": top_locations
            }
    
    def search_jobs(self, 
                   keywords: List[str] = None,
                   locations: List[str] = None,
                   sources: List[str] = None,
                   limit: int = 100,
                   days: int = 30) -> List[Dict]:
        """Search jobs with filters"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            query = """
                SELECT * FROM job_listings 
                WHERE created_at >= datetime('now', '-{} days')
            """.format(days)
            
            params = []
            
            if keywords:
                keyword_conditions = []
                for keyword in keywords:
                    keyword_conditions.append("(title LIKE ? OR description LIKE ?)")
                    params.extend([f"%{keyword}%", f"%{keyword}%"])
                query += f" AND ({' OR '.join(keyword_conditions)})"
            
            if locations:
                location_conditions = []
                for location in locations:
                    location_conditions.append("location LIKE ?")
                    params.append(f"%{location}%")
                query += f" AND ({' OR '.join(location_conditions)})"
            
            if sources:
                source_conditions = []
                for source in sources:
                    source_conditions.append("source_site = ?")
                    params.append(source)
                query += f" AND ({' OR '.join(source_conditions)})"
            
            query += " ORDER BY created_at DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_jobs_by_company(self, company: str, limit: int = 50) -> List[Dict]:
        """Get all jobs from a specific company"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM job_listings 
                WHERE company LIKE ? 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (f"%{company}%", limit))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_jobs_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """Get jobs within a date range"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM job_listings 
                WHERE created_at BETWEEN ? AND ?
                ORDER BY created_at DESC
            """, (start_date, end_date))
            return [dict(row) for row in cursor.fetchall()]
    
    def export_to_csv(self, filename: str = None, days: int = 30):
        """Export jobs to CSV file"""
        if filename is None:
            filename = f"job_listings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with self.get_connection() as conn:
            df = pd.read_sql_query("""
                SELECT * FROM job_listings 
                WHERE created_at >= datetime('now', '-{} days')
                ORDER BY created_at DESC
            """.format(days), conn)
            
            df.to_csv(filename, index=False)
            print(f"Exported {len(df)} jobs to {filename}")
    
    def export_to_json(self, filename: str = None, days: int = 30):
        """Export jobs to JSON file"""
        if filename is None:
            filename = f"job_listings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        jobs = self.search_jobs(days=days, limit=10000)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, indent=2, default=str)
        
        print(f"Exported {len(jobs)} jobs to {filename}")
    
    def cleanup_old_jobs(self, days: int = 30):
        """Remove jobs older than specified days"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM job_listings 
                WHERE created_at < datetime('now', '-{} days')
            """.format(days))
            
            deleted_count = cursor.rowcount
            conn.commit()
            print(f"Deleted {deleted_count} old jobs")
    
    def get_duplicate_jobs(self) -> List[Dict]:
        """Find potential duplicate jobs"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT title, company, location, COUNT(*) as count
                FROM job_listings 
                GROUP BY title, company, location 
                HAVING COUNT(*) > 1
                ORDER BY count DESC
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_popular_companies(self, limit: int = 20) -> List[Dict]:
        """Get companies with most job postings"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT company, COUNT(*) as job_count
                FROM job_listings 
                GROUP BY company 
                ORDER BY job_count DESC 
                LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_job_trends(self, days: int = 7) -> Dict:
        """Get job posting trends over time"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    DATE(created_at) as date,
                    COUNT(*) as job_count,
                    source_site
                FROM job_listings 
                WHERE created_at >= datetime('now', '-{} days')
                GROUP BY DATE(created_at), source_site
                ORDER BY date DESC
            """.format(days))
            
            results = cursor.fetchall()
            trends = {}
            
            for row in results:
                date = row['date']
                if date not in trends:
                    trends[date] = {'total': 0, 'sources': {}}
                
                trends[date]['total'] += row['job_count']
                trends[date]['sources'][row['source_site']] = row['job_count']
            
            return trends


def main():
    """Main function for database utilities"""
    db = JobDatabase()
    
    print("Job Database Utilities")
    print("=" * 50)
    
    # Get statistics
    stats = db.get_stats()
    print(f"Total jobs: {stats['total_jobs']}")
    print(f"Recent jobs (24h): {stats['recent_jobs_24h']}")
    print("\nJobs by source:")
    for source, count in stats['jobs_by_source'].items():
        print(f"  {source}: {count}")
    
    print("\nTop locations:")
    for location, count in list(stats['top_locations'].items())[:5]:
        print(f"  {location}: {count}")
    
    # Export recent jobs
    print("\nExporting recent jobs...")
    db.export_to_csv(days=7)
    
    # Show popular companies
    print("\nPopular companies:")
    companies = db.get_popular_companies(limit=10)
    for company in companies:
        print(f"  {company['company']}: {company['job_count']} jobs")


if __name__ == "__main__":
    main() 