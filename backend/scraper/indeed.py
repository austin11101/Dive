import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import random
from typing import List, Dict, Optional

class IndeedScraper:
    def __init__(self):
        self.base_url = "https://www.indeed.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    
    def scrape_jobs(self, query: str = "python developer", location: str = "remote", limit: int = 10) -> List[Dict]:
        """
        Scrape job listings from Indeed and South African job sites
        """
        print(f"Scraping jobs for: {query} in {location}")

        all_jobs = []

        # Check if location is South Africa related
        sa_keywords = ['south africa', 'cape town', 'johannesburg', 'durban', 'pretoria', 'za', 'gauteng', 'western cape']
        is_sa_location = any(keyword in location.lower() for keyword in sa_keywords)

        if is_sa_location:
            # Use South African scraper for SA locations
            print("Using South African job scraper...")
            try:
                from .south_africa_scraper import SouthAfricaJobScraper
                sa_scraper = SouthAfricaJobScraper()
                sa_jobs = sa_scraper.scrape_jobs(query, location, limit)
                all_jobs.extend(sa_jobs)
            except ImportError as e:
                print(f"Could not import SA scraper: {e}")
                # Only return empty list for now - no sample data
                all_jobs = []
        else:
            # For international locations, try real scraping first
            print("Attempting to scrape international job sites...")
            try:
                # Try to scrape real international jobs (placeholder for future implementation)
                real_jobs = self._scrape_international_jobs(query, location, limit)
                all_jobs.extend(real_jobs)
            except Exception as e:
                print(f"Real scraping failed: {e}")
                # Only generate sample data if specifically requested or for demo purposes
                if limit <= 5:  # Only for small requests
                    sample_jobs = self._get_international_sample_jobs(query, location, min(3, limit))
                    all_jobs.extend(sample_jobs)

        return all_jobs[:limit]

    def _scrape_international_jobs(self, query: str, location: str, limit: int) -> List[Dict]:
        """
        Attempt to scrape real international jobs
        This is a placeholder for future real scraping implementation
        """
        # For now, return empty list to avoid mock data
        # In the future, this would contain real scraping logic for Indeed.com, LinkedIn, etc.
        print(f"Real international scraping not yet implemented for {query} in {location}")
        return []

    def _get_international_sample_jobs(self, query: str, location: str, limit: int) -> List[Dict]:
        """
        Generate international sample job data
        """
        companies = [
            "Google", "Microsoft", "Amazon", "Apple", "Meta", "Netflix", "Tesla",
            "Spotify", "Uber", "Airbnb", "Stripe", "Shopify", "Slack", "Zoom",
            "Adobe", "Salesforce", "Oracle", "IBM", "Intel", "NVIDIA"
        ]

        locations = [
            "San Francisco, CA", "New York, NY", "Seattle, WA", "Austin, TX",
            "Boston, MA", "Chicago, IL", "Los Angeles, CA", "Denver, CO",
            "Remote", "London, UK", "Berlin, Germany", "Amsterdam, Netherlands",
            "Toronto, Canada", "Sydney, Australia", "Singapore", "Tokyo, Japan"
        ]

        if location.lower() != "remote":
            locations = [location] + locations[:5]

        job_titles = [
            f"Senior {query.title()}", f"{query.title()} Developer", f"Lead {query.title()}",
            f"{query.title()} Engineer", f"Principal {query.title()}", f"{query.title()} Architect",
            f"Staff {query.title()}", f"{query.title()} Manager", f"Senior {query.title()} Engineer"
        ]

        sample_jobs = []
        for i in range(min(limit, 15)):
            company = random.choice(companies)
            job_location = random.choice(locations)
            title = random.choice(job_titles)

            # International salary ranges (in USD)
            salary_ranges = [
                "$120,000 - $180,000", "$150,000 - $220,000", "$180,000 - $280,000",
                "$100,000 - $150,000", "$200,000 - $300,000", "$90,000 - $140,000",
                "$160,000 - $240,000", "$140,000 - $200,000", "Competitive", "Market Rate"
            ]

            sample_jobs.append({
                "title": title,
                "company": company,
                "location": job_location,
                "description": f"Join {company} as a {title} in {job_location}. We're looking for talented professionals to help build the future of technology.",
                "salary": random.choice(salary_ranges),
                "job_type": random.choice(["Full-time", "Contract", "Remote"]),
                "experience_level": random.choice(["Mid", "Senior", "Lead"]),
                "date_posted": datetime.now() - timedelta(days=random.randint(0, 5)),
                "link": f"https://indeed.com/viewjob?jk=sample{i+1}",
                "source": "Indeed"
            })

        # Simulate processing time
        time.sleep(random.uniform(1, 2))

        return sample_jobs

    def _get_sa_sample_jobs(self, query: str, location: str, limit: int) -> List[Dict]:
        """
        Generate South African sample job data as fallback
        """
        sa_companies = [
            "Naspers", "Shoprite", "MTN Group", "Standard Bank", "FirstRand",
            "Sasol", "Anglo American", "Vodacom", "Discovery", "Capitec Bank"
        ]

        sa_locations = [
            "Cape Town, Western Cape", "Johannesburg, Gauteng", "Durban, KwaZulu-Natal",
            "Pretoria, Gauteng", "Port Elizabeth, Eastern Cape"
        ]

        sample_jobs = []
        for i in range(min(limit, 5)):
            company = random.choice(sa_companies)
            job_location = random.choice(sa_locations)

            sample_jobs.append({
                "title": f"Senior {query.title()}",
                "company": company,
                "location": job_location,
                "description": f"Join {company} as a {query.title()} in {job_location}.",
                "salary": f"R{random.randint(300, 800)},000 - R{random.randint(400, 1000)},000",
                "job_type": "Full-time",
                "experience_level": "Senior",
                "date_posted": datetime.now() - timedelta(days=random.randint(0, 7)),
                "link": f"https://spane4all.co.za/job/{i+1}",
                "source": "Spane4all"
            })

        return sample_jobs

    def _parse_job_card(self, job_element) -> Optional[Dict]:
        """
        Parse individual job card element
        To be implemented with real scraping logic
        """
        # This will contain the actual parsing logic later
        pass
    
    def _get_job_details(self, job_url: str) -> Optional[Dict]:
        """
        Get detailed job information from job page
        To be implemented with real scraping logic
        """
        # This will contain the actual detail scraping logic later
        pass
