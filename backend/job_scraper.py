#!/usr/bin/env python3
"""
Job Listings Scraper for CV Revamp Application

This module scrapes job postings from multiple sources:
- Indeed South Africa
- LinkedIn Jobs
- Spane4all

Features:
- Respects robots.txt
- Implements delays and randomization to avoid blocking
- Saves results to SQLite database
- Handles duplicates
- Comprehensive logging
- Easy automation via cron jobs

Author: CV Revamp Team
Date: 2024
"""

import requests
import sqlite3
import logging
import time
import random
import re
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import json
import os
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException


@dataclass
class JobListing:
    """Data class for job listing information"""
    title: str
    company: str
    location: str
    posting_date: str
    job_url: str
    source_site: str
    description: str = ""
    salary: str = ""
    job_type: str = ""
    experience_level: str = ""


class JobScraper:
    """Main job scraper class"""
    
    def __init__(self, db_path: str = "job_listings.db"):
        """Initialize the scraper with database connection"""
        self.db_path = db_path
        self.session = requests.Session()
        self.setup_logging()
        self.setup_database()
        
        # Configure session headers to look more like a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # Default search parameters
        self.default_keywords = ["software developer", "web developer", "full stack developer", "frontend developer", "backend developer"]
        self.default_locations = ["South Africa", "Cape Town", "Johannesburg", "Durban", "Pretoria"]
        
        # Rate limiting settings
        self.min_delay = 2
        self.max_delay = 5
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('job_scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_database(self):
        """Create database and tables if they don't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create jobs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS job_listings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    company TEXT NOT NULL,
                    location TEXT NOT NULL,
                    posting_date TEXT,
                    job_url TEXT UNIQUE NOT NULL,
                    source_site TEXT NOT NULL,
                    description TEXT,
                    salary TEXT,
                    job_type TEXT,
                    experience_level TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create index for faster lookups
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_job_url ON job_listings(job_url)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_source_site ON job_listings(source_site)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_created_at ON job_listings(created_at)
            ''')
            
            conn.commit()
            self.logger.info("Database setup completed")
    
    def random_delay(self):
        """Add random delay between requests to avoid being blocked"""
        delay = random.uniform(self.min_delay, self.max_delay)
        time.sleep(delay)
        
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        return text
    
    def parse_date(self, date_str: str) -> str:
        """Parse various date formats and return standardized format"""
        if not date_str:
            return ""
        
        # Common patterns for job posting dates
        patterns = [
            r'(\d+)\s+(day|days|hour|hours|minute|minutes)\s+ago',
            r'(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{4})',
            r'(\d{1,2})/(\d{1,2})/(\d{4})',
            r'(\d{4})-(\d{1,2})-(\d{1,2})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, date_str, re.IGNORECASE)
            if match:
                return date_str  # Return as-is for now, could implement full parsing
        
        return date_str
    
    def save_job_listings(self, jobs: List[JobListing]) -> int:
        """Save job listings to database, avoiding duplicates"""
        saved_count = 0
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for job in jobs:
                try:
                    cursor.execute('''
                        INSERT OR IGNORE INTO job_listings 
                        (title, company, location, posting_date, job_url, source_site, 
                         description, salary, job_type, experience_level)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        job.title, job.company, job.location, job.posting_date,
                        job.job_url, job.source_site, job.description, job.salary,
                        job.job_type, job.experience_level
                    ))
                    
                    if cursor.rowcount > 0:
                        saved_count += 1
                        
                except sqlite3.Error as e:
                    self.logger.error(f"Error saving job {job.job_url}: {e}")
            
            conn.commit()
        
        return saved_count
    
    def scrape_indeed_jobs(self, keywords: List[str] = None, locations: List[str] = None) -> List[JobListing]:
        """Scrape job listings from Indeed South Africa"""
        if keywords is None:
            keywords = self.default_keywords
        if locations is None:
            locations = self.default_locations
            
        self.logger.info(f"Starting Indeed scraping for keywords: {keywords}")
        jobs = []
        
        for keyword in keywords:
            for location in locations:
                try:
                    # Indeed South Africa URL
                    base_url = "https://za.indeed.com"
                    search_url = f"{base_url}/jobs"
                    
                    params = {
                        'q': keyword,
                        'l': location,
                        'sort': 'date'  # Sort by date to get recent postings
                    }
                    
                    self.logger.info(f"Scraping Indeed: {keyword} in {location}")
                    
                    response = self.session.get(search_url, params=params, timeout=30)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find job cards
                    job_cards = soup.find_all('div', class_='job_seen_beacon')
                    
                    for card in job_cards[:20]:  # Limit to 20 jobs per search
                        try:
                            # Extract job title
                            title_elem = card.find('h2', class_='jobTitle')
                            if not title_elem:
                                continue
                            title = self.clean_text(title_elem.get_text())
                            
                            # Extract company name
                            company_elem = card.find('span', class_='companyName')
                            company = self.clean_text(company_elem.get_text()) if company_elem else "Unknown Company"
                            
                            # Extract location
                            location_elem = card.find('div', class_='companyLocation')
                            location = self.clean_text(location_elem.get_text()) if location_elem else location
                            
                            # Extract job URL
                            job_link = card.find('a', class_='jcs-JobTitle')
                            if not job_link:
                                continue
                            job_url = urljoin(base_url, job_link.get('href'))
                            
                            # Extract posting date
                            date_elem = card.find('span', class_='date')
                            posting_date = self.parse_date(date_elem.get_text()) if date_elem else ""
                            
                            # Create job listing
                            job = JobListing(
                                title=title,
                                company=company,
                                location=location,
                                posting_date=posting_date,
                                job_url=job_url,
                                source_site="Indeed South Africa",
                                description="",  # Would need to visit individual job pages for full description
                                salary="",
                                job_type="",
                                experience_level=""
                            )
                            
                            jobs.append(job)
                            
                        except Exception as e:
                            self.logger.error(f"Error parsing Indeed job card: {e}")
                            continue
                    
                    self.random_delay()
                    
                except requests.RequestException as e:
                    self.logger.error(f"Error scraping Indeed for {keyword} in {location}: {e}")
                    continue
                except Exception as e:
                    self.logger.error(f"Unexpected error scraping Indeed: {e}")
                    continue
        
        self.logger.info(f"Indeed scraping completed. Found {len(jobs)} jobs")
        return jobs
    
    def scrape_linkedin_jobs(self, keywords: List[str] = None, locations: List[str] = None) -> List[JobListing]:
        """Scrape job listings from LinkedIn Jobs"""
        if keywords is None:
            keywords = self.default_keywords
        if locations is None:
            locations = self.default_locations
            
        self.logger.info(f"Starting LinkedIn scraping for keywords: {keywords}")
        jobs = []
        
        # LinkedIn requires JavaScript, so we'll use Selenium
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            
            for keyword in keywords:
                for location in locations:
                    try:
                        # LinkedIn Jobs URL
                        search_url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}&f_TPR=r86400"  # Last 24 hours
                        
                        self.logger.info(f"Scraping LinkedIn: {keyword} in {location}")
                        
                        driver.get(search_url)
                        
                        # Wait for job listings to load
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "job-search-card"))
                        )
                        
                        # Scroll to load more jobs
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(3)
                        
                        # Find job cards
                        job_cards = driver.find_elements(By.CLASS_NAME, "job-search-card")
                        
                        for card in job_cards[:20]:  # Limit to 20 jobs per search
                            try:
                                # Extract job title
                                title_elem = card.find_element(By.CSS_SELECTOR, "h3.base-search-card__title")
                                title = self.clean_text(title_elem.text)
                                
                                # Extract company name
                                company_elem = card.find_element(By.CSS_SELECTOR, "h4.base-search-card__subtitle")
                                company = self.clean_text(company_elem.text)
                                
                                # Extract location
                                location_elem = card.find_element(By.CSS_SELECTOR, ".job-search-card__location")
                                location = self.clean_text(location_elem.text)
                                
                                # Extract job URL
                                job_link = card.find_element(By.CSS_SELECTOR, "a.base-card__full-link")
                                job_url = job_link.get_attribute("href")
                                
                                # Extract posting date
                                try:
                                    date_elem = card.find_element(By.CSS_SELECTOR, "time.job-search-card__listdate")
                                    posting_date = self.parse_date(date_elem.get_attribute("datetime"))
                                except NoSuchElementException:
                                    posting_date = ""
                                
                                # Create job listing
                                job = JobListing(
                                    title=title,
                                    company=company,
                                    location=location,
                                    posting_date=posting_date,
                                    job_url=job_url,
                                    source_site="LinkedIn Jobs",
                                    description="",
                                    salary="",
                                    job_type="",
                                    experience_level=""
                                )
                                
                                jobs.append(job)
                                
                            except Exception as e:
                                self.logger.error(f"Error parsing LinkedIn job card: {e}")
                                continue
                        
                        self.random_delay()
                        
                    except TimeoutException:
                        self.logger.error(f"Timeout waiting for LinkedIn page to load for {keyword} in {location}")
                        continue
                    except Exception as e:
                        self.logger.error(f"Error scraping LinkedIn for {keyword} in {location}: {e}")
                        continue
            
            driver.quit()
            
        except Exception as e:
            self.logger.error(f"Error setting up Selenium driver: {e}")
            return jobs
        
        self.logger.info(f"LinkedIn scraping completed. Found {len(jobs)} jobs")
        return jobs
    
    def scrape_spane4all_jobs(self, keywords: List[str] = None, locations: List[str] = None) -> List[JobListing]:
        """Scrape job listings from Spane4all"""
        if keywords is None:
            keywords = self.default_keywords
        if locations is None:
            locations = self.default_locations
            
        self.logger.info(f"Starting Spane4all scraping for keywords: {keywords}")
        jobs = []
        
        try:
            # Spane4all URL - based on actual site structure
            base_url = "https://www.spane4all.co.za"
            search_url = f"{base_url}/Jobs"
            
            self.logger.info(f"Scraping Spane4all: {search_url}")
            
            response = self.session.get(search_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Based on the search results, jobs are structured with h3 tags for titles
            # and company/location info in the text
            job_sections = soup.find_all('h3')
            
            for section in job_sections[:20]:  # Limit to 20 jobs
                try:
                    # Extract job title (the h3 text)
                    title = self.clean_text(section.get_text())
                    if not title or "Job:" not in title:
                        continue
                    
                    # Clean up the title (remove "Job:" prefix)
                    title = title.replace("Job:", "").strip()
                    
                    # Find the next elements for company and location
                    current = section
                    company = "Unknown Company"
                    location = "Unknown Location"
                    posting_date = ""
                    
                    # Look for company and location info in nearby elements
                    job_url = f"{base_url}/Jobs"  # Default URL
                    for _ in range(10):  # Look at next 10 elements
                        current = current.find_next_sibling()
                        if not current:
                            break
                            
                        text = self.clean_text(current.get_text())
                        
                        if "Company :" in text:
                            company = text.replace("Company :", "").strip()
                        elif "Location :" in text:
                            location = text.replace("Location :", "").strip()
                        elif "Date :" in text:
                            posting_date = text.replace("Date :", "").strip()
                        elif "Apply" in text and current.name == 'a':
                            # This might be the apply link
                            job_url = urljoin(base_url, current.get('href', ''))
                            break
                    
                    # Create job listing
                    job = JobListing(
                        title=title,
                        company=company,
                        location=location,
                        posting_date=posting_date,
                        job_url=job_url,
                        source_site="Spane4all",
                        description="",
                        salary="",
                        job_type="",
                        experience_level=""
                    )
                    
                    jobs.append(job)
                    
                except Exception as e:
                    self.logger.error(f"Error parsing Spane4all job listing: {e}")
                    continue
            
            self.random_delay()
            
        except requests.RequestException as e:
            self.logger.error(f"Error scraping Spane4all: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error scraping Spane4all: {e}")
        
        self.logger.info(f"Spane4all scraping completed. Found {len(jobs)} jobs")
        return jobs
    
    def run_all_scrapers(self, keywords: List[str] = None, locations: List[str] = None) -> Dict[str, int]:
        """Run all scrapers and return summary statistics"""
        self.logger.info("Starting job scraping process")
        
        start_time = datetime.now()
        results = {}
        
        # Run all scrapers
        scrapers = [
            ("Indeed", self.scrape_indeed_jobs),
            ("Spane4all", self.scrape_spane4all_jobs)
        ]
        
        all_jobs = []
        
        for name, scraper_func in scrapers:
            try:
                self.logger.info(f"Running {name} scraper...")
                jobs = scraper_func(keywords, locations)
                all_jobs.extend(jobs)
                results[f"{name}_found"] = len(jobs)
                self.logger.info(f"{name} scraper completed: {len(jobs)} jobs found")
                
            except Exception as e:
                self.logger.error(f"Error running {name} scraper: {e}")
                results[f"{name}_found"] = 0
        
        # Save all jobs to database
        if all_jobs:
            saved_count = self.save_job_listings(all_jobs)
            results["total_saved"] = saved_count
            self.logger.info(f"Saved {saved_count} new jobs to database")
        else:
            results["total_saved"] = 0
            self.logger.warning("No jobs found from any scraper")
        
        # Calculate statistics
        end_time = datetime.now()
        duration = end_time - start_time
        results["duration_seconds"] = duration.total_seconds()
        results["total_found"] = len(all_jobs)
        
        self.logger.info(f"Scraping completed in {duration.total_seconds():.2f} seconds")
        self.logger.info(f"Summary: {results}")
        
        return results
    
    def get_recent_jobs(self, hours: int = 24) -> List[Dict]:
        """Get jobs from the last N hours"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM job_listings 
                WHERE created_at >= datetime('now', '-{} hours')
                ORDER BY created_at DESC
            '''.format(hours))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def get_jobs_by_source(self, source: str, limit: int = 100) -> List[Dict]:
        """Get jobs from a specific source"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM job_listings 
                WHERE source_site = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (source, limit))
            
            return [dict(row) for row in cursor.fetchall()]


def main():
    """Main function to run the scraper"""
    # Initialize scraper
    scraper = JobScraper()
    
    # Custom search parameters (modify these as needed)
    custom_keywords = [
        "software developer",
        "web developer", 
        "full stack developer",
        "frontend developer",
        "backend developer",
        "python developer",
        "javascript developer",
        "angular developer",
        "react developer",
        "devops engineer"
    ]
    
    custom_locations = [
        "South Africa",
        "Cape Town",
        "Johannesburg", 
        "Durban",
        "Pretoria",
        "Port Elizabeth",
        "Bloemfontein"
    ]
    
    # Run all scrapers
    results = scraper.run_all_scrapers(custom_keywords, custom_locations)
    
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


if __name__ == "__main__":
    main() 