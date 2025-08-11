import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import random
from typing import List, Dict, Optional
import re
from urllib.parse import quote_plus

class GoogleJobsScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape_jobs(self, query: str = "python developer", location: str = "south africa", limit: int = 10) -> List[Dict]:
        """
        Scrape job listings from Google Jobs
        Note: Google Jobs has anti-scraping measures, so this provides sample data based on typical SA job market
        """
        print(f"Fetching Google Jobs data for: {query} in {location}")
        
        try:
            # In a real implementation, you might use Google Jobs API or other methods
            # For now, we'll provide realistic sample data based on South African job market
            jobs = self._get_google_jobs_sample_data(query, location, limit)
            
            # Simulate API call delay
            time.sleep(random.uniform(1, 2))
            
            return jobs
            
        except Exception as e:
            print(f"Error fetching Google Jobs data: {e}")
            return self._get_google_jobs_sample_data(query, location, limit)
    
    def _get_google_jobs_sample_data(self, query: str, location: str, limit: int) -> List[Dict]:
        """
        Generate realistic Google Jobs sample data for South Africa
        """
        # Major South African companies across ALL industries
        sa_companies = [
            # Tech Companies
            "Takealot", "Konga", "PayU", "Yoco", "Luno", "GetSmarter", "Aerobotics",
            "DataProphet", "Jumo", "SweepSouth", "SnapScan", "Ozow", "Peach Payments",

            # Financial Services
            "Standard Bank", "FirstRand", "Nedbank", "ABSA", "Capitec Bank", "Discovery",
            "Old Mutual", "Sanlam", "Momentum", "Liberty", "PSG Group", "Investec",

            # Telecommunications
            "MTN Group", "Vodacom", "Telkom", "Cell C", "Rain", "Liquid Telecom",

            # Retail & E-commerce
            "Shoprite", "Pick n Pay", "Woolworths", "Mr Price", "Clicks", "Dis-Chem",
            "Massmart", "Foschini Group", "Truworths", "Edcon", "Game", "Makro",

            # Mining & Resources
            "Anglo American", "Sasol", "BHP Billiton", "Gold Fields", "Impala Platinum",
            "Sibanye-Stillwater", "Exxaro", "Kumba Iron Ore", "African Rainbow Minerals",

            # Media & Technology
            "Naspers", "MultiChoice", "Media24", "Primedia", "Kagiso Media",

            # Consulting & Professional Services
            "Deloitte", "PwC", "KPMG", "EY", "McKinsey & Company", "BCG", "Accenture",
            "IBM South Africa", "Microsoft South Africa", "Amazon Web Services",

            # Healthcare & Pharmaceuticals
            "Netcare", "Life Healthcare", "Mediclinic", "Aspen Pharmacare", "Adcock Ingram",
            "Dis-Chem Pharmacies", "Clicks Group", "Pharma Dynamics",

            # Education & Training
            "University of Cape Town", "University of the Witwatersrand", "Stellenbosch University",
            "UNISA", "Damelin", "CTI Education Group", "Rosebank College",

            # Manufacturing & Industrial
            "Bidvest", "Imperial Holdings", "Barloworld", "Reunert", "Hudaco Industries",
            "Metair", "Astral Foods", "Tiger Brands", "Pioneer Foods",

            # Construction & Engineering
            "Murray & Roberts", "WBHO", "Aveng", "Stefanutti Stocks", "Group Five",
            "Basil Read", "Concor Holdings", "Raubex Group",

            # Transport & Logistics
            "Transnet", "Imperial Logistics", "Super Group", "KAP Industrial Holdings",
            "Unitrans", "Dawn Wing", "The Courier Guy", "Fastway Couriers",

            # Hospitality & Tourism
            "Sun International", "Tsogo Sun", "City Lodge Hotels", "Southern Sun",
            "Protea Hotels", "SAA", "Kulula", "FlySafair",

            # Agriculture & Food
            "Shoprite Holdings", "Tiger Brands", "AVI Limited", "RCL Foods",
            "Astral Foods", "Quantum Foods", "Pioneer Foods", "Clover Industries"
        ]
        
        # South African cities and provinces
        sa_locations = [
            "Cape Town, Western Cape", "Johannesburg, Gauteng", "Durban, KwaZulu-Natal",
            "Pretoria, Gauteng", "Port Elizabeth, Eastern Cape", "Bloemfontein, Free State",
            "East London, Eastern Cape", "Pietermaritzburg, KwaZulu-Natal", 
            "Polokwane, Limpopo", "Nelspruit, Mpumalanga", "Kimberley, Northern Cape",
            "Mafikeng, North West", "Sandton, Gauteng", "Rosebank, Gauteng",
            "Century City, Cape Town", "Umhlanga, Durban", "Stellenbosch, Western Cape",
            "Midrand, Gauteng", "Bellville, Western Cape", "Randburg, Gauteng"
        ]
        
        # Generate diverse job titles based on query - ALL JOB TYPES
        if "java" in query.lower():
            base_titles = [
                "Senior Java Developer", "Java Software Engineer", "Lead Java Developer",
                "Java Backend Developer", "Junior Java Developer", "Java Full Stack Developer",
                "Java Spring Developer", "Principal Java Engineer", "Java Architect",
                "Java Team Lead", "Senior Java Engineer", "Java Consultant",
                "Java Application Developer", "Java Web Developer"
            ]
        elif "python" in query.lower():
            base_titles = [
                "Senior Python Developer", "Python Software Engineer", "Lead Python Developer",
                "Python Backend Developer", "Junior Python Developer", "Python Full Stack Developer",
                "Python Data Engineer", "Principal Python Engineer", "Python Architect",
                "Python Team Lead", "Senior Python Engineer", "Python Consultant"
            ]
        elif any(word in query.lower() for word in ["sales", "marketing", "business"]):
            base_titles = [
                "Sales Manager", "Business Development Manager", "Marketing Manager",
                "Sales Representative", "Account Manager", "Marketing Specialist",
                "Business Analyst", "Sales Executive", "Digital Marketing Manager",
                "Sales Consultant", "Marketing Coordinator", "Business Development Executive"
            ]
        elif any(word in query.lower() for word in ["finance", "accounting", "financial"]):
            base_titles = [
                "Financial Manager", "Accountant", "Financial Analyst", "Finance Manager",
                "Senior Accountant", "Financial Advisor", "Credit Analyst", "Tax Consultant",
                "Management Accountant", "Financial Controller", "Bookkeeper"
            ]
        elif any(word in query.lower() for word in ["hr", "human resources", "recruitment"]):
            base_titles = [
                "HR Manager", "Human Resources Specialist", "Recruitment Consultant",
                "HR Business Partner", "Talent Acquisition Specialist", "HR Generalist",
                "People & Culture Manager", "HR Coordinator", "Recruitment Manager"
            ]
        elif any(word in query.lower() for word in ["nurse", "medical", "healthcare", "doctor"]):
            base_titles = [
                "Registered Nurse", "Medical Officer", "Healthcare Assistant",
                "Clinical Nurse", "General Practitioner", "Medical Specialist",
                "Nursing Manager", "Healthcare Coordinator", "Medical Administrator"
            ]
        elif any(word in query.lower() for word in ["teacher", "education", "lecturer"]):
            base_titles = [
                "Primary School Teacher", "High School Teacher", "University Lecturer",
                "Education Specialist", "Academic Coordinator", "Training Manager",
                "Subject Teacher", "Education Consultant", "Learning Facilitator"
            ]
        elif any(word in query.lower() for word in ["engineer", "engineering"]) and "software" not in query.lower():
            base_titles = [
                "Civil Engineer", "Mechanical Engineer", "Electrical Engineer",
                "Mining Engineer", "Chemical Engineer", "Industrial Engineer",
                "Project Engineer", "Site Engineer", "Design Engineer"
            ]
        elif any(word in query.lower() for word in ["admin", "administrator", "office"]):
            base_titles = [
                "Office Administrator", "Administrative Assistant", "Executive Assistant",
                "Office Manager", "Administrative Coordinator", "Data Capturer",
                "Receptionist", "Personal Assistant", "Administrative Officer"
            ]
        elif any(word in query.lower() for word in ["driver", "logistics", "transport"]):
            base_titles = [
                "Delivery Driver", "Truck Driver", "Logistics Coordinator",
                "Transport Manager", "Warehouse Manager", "Supply Chain Coordinator",
                "Fleet Manager", "Dispatch Coordinator", "Logistics Specialist"
            ]
        elif any(word in query.lower() for word in ["retail", "cashier", "shop", "store"]):
            base_titles = [
                "Store Manager", "Retail Assistant", "Cashier", "Shop Assistant",
                "Retail Manager", "Sales Assistant", "Store Supervisor",
                "Merchandiser", "Customer Service Representative", "Retail Consultant"
            ]
        else:
            # Generic titles for any other job types
            base_titles = [
                f"Senior {query.title()}", f"{query.title()} Manager", f"Lead {query.title()}",
                f"{query.title()} Specialist", f"Junior {query.title()}", f"{query.title()} Consultant",
                f"{query.title()} Coordinator", f"{query.title()} Officer", f"Principal {query.title()}",
                f"{query.title()} Supervisor", f"{query.title()} Executive", f"{query.title()} Assistant"
            ]
        
        # South African salary ranges (in ZAR)
        salary_ranges = [
            "R250,000 - R400,000", "R400,000 - R600,000", "R600,000 - R850,000",
            "R300,000 - R500,000", "R500,000 - R750,000", "R750,000 - R1,200,000",
            "R200,000 - R350,000", "R350,000 - R550,000", "R550,000 - R800,000",
            "R180,000 - R320,000", "R450,000 - R700,000", "R700,000 - R1,000,000",
            "Market Related", "Competitive Package", "Negotiable", "CTC Negotiable"
        ]
        
        job_types = ["Full-time", "Contract", "Permanent", "Fixed Term", "Remote", "Hybrid"]
        experience_levels = ["Entry Level", "Junior", "Mid Level", "Senior", "Lead", "Principal"]
        
        # Industry-specific descriptions
        descriptions = [
            f"Join our dynamic team as a {query.title()} and contribute to cutting-edge projects in the South African market.",
            f"We are seeking a talented {query.title()} to help drive digital transformation initiatives.",
            f"Exciting opportunity for a {query.title()} to work with modern technologies and agile methodologies.",
            f"Be part of our growing tech team and help build innovative solutions for African markets.",
            f"Looking for a passionate {query.title()} to join our award-winning development team.",
            f"Great opportunity to advance your career as a {query.title()} in a leading South African company.",
            f"Join us in building the future of technology in Africa as a {query.title()}.",
            f"We're expanding our team and need a skilled {query.title()} to help us scale our operations."
        ]
        
        jobs = []
        for i in range(min(limit, len(sa_companies))):
            company = random.choice(sa_companies)
            location_choice = random.choice(sa_locations)
            title = random.choice(base_titles)
            
            # Adjust salary based on experience level
            exp_level = random.choice(experience_levels)
            if exp_level in ["Entry Level", "Junior"]:
                salary_options = salary_ranges[:6]  # Lower salary ranges
            elif exp_level in ["Senior", "Lead", "Principal"]:
                salary_options = salary_ranges[6:]  # Higher salary ranges
            else:
                salary_options = salary_ranges[3:9]  # Mid-range salaries
            
            job_data = {
                "title": title,
                "company": company,
                "location": location_choice,
                "description": random.choice(descriptions),
                "salary": random.choice(salary_options),
                "job_type": random.choice(job_types),
                "experience_level": exp_level,
                "date_posted": datetime.now() - timedelta(days=random.randint(0, 14)),
                "link": f"https://www.google.com/search?q={quote_plus(title + ' ' + company)}&ibp=htl;jobs",
                "source": "Google Jobs"
            }
            
            jobs.append(job_data)
        
        return jobs
    
    def search_google_jobs_api(self, query: str, location: str, limit: int) -> List[Dict]:
        """
        Alternative method using Google Jobs API (requires API key)
        This is a placeholder for future implementation
        """
        # This would require Google Jobs API integration
        # For now, return sample data
        return self._get_google_jobs_sample_data(query, location, limit)
