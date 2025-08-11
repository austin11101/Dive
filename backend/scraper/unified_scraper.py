"""
Unified High-Performance Job Scraper
Consolidates all scrapers into one efficient system
"""

import asyncio
import aiohttp
import time
import random
import hashlib
import json
from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse, quote_plus
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import logging
from collections import defaultdict
import re
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class JobResult:
    """Standardized job result structure"""
    title: str
    company: str
    location: str
    description: str
    salary: Optional[str] = None
    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    date_posted: Optional[datetime] = None
    link: str = ""
    source: str = ""
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for API response"""
        return {
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'description': self.description,
            'salary': self.salary,
            'job_type': self.job_type,
            'experience_level': self.experience_level,
            'date_posted': self.date_posted.isoformat() if self.date_posted else None,
            'link': self.link,
            'source': self.source
        }

@dataclass
class ScrapingConfig:
    """Configuration for each job site"""
    name: str
    base_url: str
    search_url: str
    selectors: Dict[str, str]
    rate_limit: float = 2.0  # seconds between requests
    max_pages: int = 5
    enabled: bool = True

class UnifiedJobScraper:
    """High-performance unified job scraper"""
    
    def __init__(self):
        self.ua = UserAgent()
        self.session: Optional[aiohttp.ClientSession] = None
        self.seen_jobs: Set[str] = set()
        self.rate_limits: Dict[str, float] = {}
        
        # Job site configurations
        self.configs = {
            'indeed_za': ScrapingConfig(
                name='Indeed South Africa',
                base_url='https://za.indeed.com',
                search_url='https://za.indeed.com/jobs?q={query}&l={location}&start={start}',
                selectors={
                    'job_container': '.jobsearch-SerpJobCard, .job_seen_beacon',
                    'title': '.jobTitle a span, .jobTitle-color-purple',
                    'company': '.companyName, [data-testid="company-name"]',
                    'location': '.companyLocation, [data-testid="job-location"]',
                    'description': '.job-snippet, [data-testid="job-snippet"]',
                    'salary': '.salary-snippet, .salaryText',
                    'link': '.jobTitle a, h2 a'
                },
                rate_limit=1.5
            ),
            'careers24': ScrapingConfig(
                name='Careers24',
                base_url='https://www.careers24.com',
                search_url='https://www.careers24.com/jobs/search?q={query}&l={location}&p={page}',
                selectors={
                    'job_container': '.job-result-card, .search-result',
                    'title': '.job-title, h3 a',
                    'company': '.company-name, .employer',
                    'location': '.job-location, .location',
                    'description': '.job-description, .snippet',
                    'salary': '.salary, .remuneration',
                    'link': '.job-title a, h3 a'
                },
                rate_limit=2.0
            ),
            'pnet': ScrapingConfig(
                name='PNet',
                base_url='https://www.pnet.co.za',
                search_url='https://www.pnet.co.za/jobs/search-results?q={query}&l={location}&p={page}',
                selectors={
                    'job_container': '.job-item, .search-item',
                    'title': '.job-title, h2 a',
                    'company': '.company, .employer-name',
                    'location': '.location, .job-location',
                    'description': '.description, .job-summary',
                    'salary': '.salary, .package',
                    'link': '.job-title a, h2 a'
                },
                rate_limit=2.5
            ),
            'spane4all': ScrapingConfig(
                name='Spane4All',
                base_url='https://spane4all.co.za',
                search_url='https://spane4all.co.za/jobs?search={query}&location={location}&page={page}',
                selectors={
                    'job_container': '.job-listing, .job-card',
                    'title': '.job-title, h3',
                    'company': '.company-name, .employer',
                    'location': '.job-location, .location',
                    'description': '.job-description, .summary',
                    'salary': '.salary, .compensation',
                    'link': '.job-title a, h3 a'
                },
                rate_limit=1.0
            )
        }
    
    async def __aenter__(self):
        """Async context manager entry"""
        connector = aiohttp.TCPConnector(
            limit=50,
            limit_per_host=10,
            ttl_dns_cache=300,
            use_dns_cache=True,
            keepalive_timeout=30,
            enable_cleanup_closed=True
        )
        
        timeout = aiohttp.ClientTimeout(
            total=30,
            connect=10,
            sock_read=15
        )
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                'User-Agent': self.ua.random,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    def _generate_job_hash(self, job: JobResult) -> str:
        """Generate unique hash for deduplication"""
        key_string = f"{job.title.lower().strip()}|{job.company.lower().strip()}|{job.location.lower().strip()}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _is_duplicate(self, job: JobResult) -> bool:
        """Check if job is duplicate"""
        job_hash = self._generate_job_hash(job)
        if job_hash in self.seen_jobs:
            return True
        self.seen_jobs.add(job_hash)
        return False
    
    async def _respect_rate_limit(self, site: str):
        """Respect rate limiting for each site"""
        config = self.configs.get(site)
        if not config:
            return
        
        last_request = self.rate_limits.get(site, 0)
        time_since_last = time.time() - last_request
        
        if time_since_last < config.rate_limit:
            sleep_time = config.rate_limit - time_since_last
            await asyncio.sleep(sleep_time)
        
        self.rate_limits[site] = time.time()
    
    async def _fetch_page(self, url: str, site: str) -> Optional[str]:
        """Fetch a single page with error handling"""
        try:
            await self._respect_rate_limit(site)
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    logger.info(f"Successfully fetched {site}: {url}")
                    return content
                else:
                    logger.warning(f"HTTP {response.status} for {site}: {url}")
                    return None
                    
        except asyncio.TimeoutError:
            logger.error(f"Timeout fetching {site}: {url}")
            return None
        except Exception as e:
            logger.error(f"Error fetching {site}: {url} - {str(e)}")
            return None
    
    def _extract_jobs_from_html(self, html: str, config: ScrapingConfig) -> List[JobResult]:
        """Extract jobs from HTML using BeautifulSoup"""
        jobs = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            job_containers = soup.select(config.selectors['job_container'])
            
            logger.info(f"Found {len(job_containers)} job containers for {config.name}")
            
            for container in job_containers:
                try:
                    # Extract job data
                    title_elem = container.select_one(config.selectors['title'])
                    company_elem = container.select_one(config.selectors['company'])
                    location_elem = container.select_one(config.selectors['location'])
                    description_elem = container.select_one(config.selectors['description'])
                    salary_elem = container.select_one(config.selectors['salary'])
                    link_elem = container.select_one(config.selectors['link'])
                    
                    # Skip if missing essential data
                    if not title_elem or not company_elem:
                        continue
                    
                    # Clean and extract text
                    title = title_elem.get_text(strip=True)
                    company = company_elem.get_text(strip=True)
                    location = location_elem.get_text(strip=True) if location_elem else "South Africa"
                    description = description_elem.get_text(strip=True) if description_elem else ""
                    salary = salary_elem.get_text(strip=True) if salary_elem else None
                    
                    # Extract link
                    link = ""
                    if link_elem:
                        href = link_elem.get('href', '')
                        if href.startswith('/'):
                            link = urljoin(config.base_url, href)
                        elif href.startswith('http'):
                            link = href
                    
                    # Create job result
                    job = JobResult(
                        title=title,
                        company=company,
                        location=location,
                        description=description[:500],  # Limit description length
                        salary=salary,
                        link=link,
                        source=config.name,
                        date_posted=datetime.now()
                    )
                    
                    # Check for duplicates
                    if not self._is_duplicate(job):
                        jobs.append(job)
                    
                except Exception as e:
                    logger.warning(f"Error extracting job from {config.name}: {str(e)}")
                    continue
            
        except Exception as e:
            logger.error(f"Error parsing HTML for {config.name}: {str(e)}")
        
        return jobs
    
    async def _scrape_site(self, site: str, query: str, location: str, max_jobs: int = 20) -> List[JobResult]:
        """Scrape a single job site"""
        config = self.configs.get(site)
        if not config or not config.enabled:
            logger.warning(f"Site {site} not configured or disabled")
            return []
        
        jobs = []
        page = 0
        start = 0
        
        logger.info(f"Starting to scrape {config.name} for '{query}' in '{location}'")
        
        while len(jobs) < max_jobs and page < config.max_pages:
            # Build URL
            if '{start}' in config.search_url:
                url = config.search_url.format(
                    query=quote_plus(query),
                    location=quote_plus(location),
                    start=start
                )
                start += 10  # Indeed-style pagination
            else:
                url = config.search_url.format(
                    query=quote_plus(query),
                    location=quote_plus(location),
                    page=page + 1
                )
            
            # Fetch page
            html = await self._fetch_page(url, site)
            if not html:
                break
            
            # Extract jobs
            page_jobs = self._extract_jobs_from_html(html, config)
            if not page_jobs:
                logger.info(f"No more jobs found on page {page + 1} for {config.name}")
                break
            
            jobs.extend(page_jobs)
            page += 1
            
            logger.info(f"Scraped {len(page_jobs)} jobs from {config.name} page {page}")
        
        logger.info(f"Total scraped from {config.name}: {len(jobs)} jobs")
        return jobs[:max_jobs]
    
    async def scrape_all_sites(self, query: str, location: str = "South Africa", max_jobs_per_site: int = 10) -> List[Dict]:
        """Scrape all enabled job sites concurrently with mock data fallback"""
        logger.info(f"Starting unified scraping for '{query}' in '{location}'")

        # Create scraping tasks
        tasks = []
        for site in self.configs.keys():
            if self.configs[site].enabled:
                task = self._scrape_site(site, query, location, max_jobs_per_site)
                tasks.append(task)

        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Combine results
        all_jobs = []
        successful_scrapes = 0

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                site = list(self.configs.keys())[i]
                logger.error(f"Error scraping {site}: {str(result)}")
            else:
                all_jobs.extend(result)
                if result:  # If we got jobs from this site
                    successful_scrapes += 1

        # If no real jobs were found, return empty list
        if len(all_jobs) == 0:
            logger.info("No jobs found from scraping")
            return []

        # Convert to dictionaries and sort by date
        job_dicts = [job.to_dict() for job in all_jobs]
        job_dicts.sort(key=lambda x: x.get('date_posted', ''), reverse=True)

        logger.info(f"Unified scraping completed: {len(job_dicts)} total jobs found from {successful_scrapes} sites")
        return job_dicts
    
    async def scrape_single_site(self, site: str, query: str, location: str = "South Africa", max_jobs: int = 20) -> List[Dict]:
        """Scrape a single specific site"""
        jobs = await self._scrape_site(site, query, location, max_jobs)
        return [job.to_dict() for job in jobs]
    
    def get_available_sites(self) -> List[str]:
        """Get list of available job sites"""
        return [site for site, config in self.configs.items() if config.enabled]
    
    def enable_site(self, site: str):
        """Enable a job site"""
        if site in self.configs:
            self.configs[site].enabled = True
    
    def disable_site(self, site: str):
        """Disable a job site"""
        if site in self.configs:
            self.configs[site].enabled = False

# Convenience functions for backward compatibility
async def scrape_jobs_unified(query: str, location: str = "South Africa", max_jobs: int = 50) -> List[Dict]:
    """Main scraping function - scrapes all sites"""
    async with UnifiedJobScraper() as scraper:
        return await scraper.scrape_all_sites(query, location, max_jobs // 4)  # Distribute across sites

async def scrape_jobs_single_site(site: str, query: str, location: str = "South Africa", max_jobs: int = 20) -> List[Dict]:
    """Scrape a single site"""
    async with UnifiedJobScraper() as scraper:
        return await scraper.scrape_single_site(site, query, location, max_jobs)

# Test function
async def test_scraper():
    """Test the unified scraper"""
    async with UnifiedJobScraper() as scraper:
        jobs = await scraper.scrape_all_sites("python developer", "johannesburg", 5)
        print(f"Found {len(jobs)} jobs")
        for job in jobs[:3]:
            print(f"- {job['title']} at {job['company']} ({job['source']})")

if __name__ == "__main__":
    asyncio.run(test_scraper())
