# Job Listings Scraper

A comprehensive Python job scraper that collects job postings from multiple South African job sites including Indeed, LinkedIn Jobs, and Spane4all.

## Features

- **Multi-site scraping**: Indeed South Africa, LinkedIn Jobs, Spane4all
- **Anti-blocking measures**: Random delays, user agent rotation, respectful crawling
- **Database storage**: SQLite database with duplicate prevention
- **Comprehensive logging**: Track scraping activities and errors
- **Easy automation**: Simple script for cron jobs and CI/CD
- **Configurable**: Easy to modify search keywords and locations
- **Robust error handling**: Graceful handling of network issues and site changes

## Installation

### Prerequisites

- Python 3.8+
- Chrome/Chromium browser (for Selenium)
- ChromeDriver (automatically managed by webdriver-manager)

### Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements-scraper.txt
   ```

2. **Install Chrome/Chromium** (if not already installed):
   - **Ubuntu/Debian**: `sudo apt install chromium-browser`
   - **macOS**: `brew install chromium`
   - **Windows**: Download from https://www.google.com/chrome/

3. **Verify installation**:
   ```bash
   python job_scraper.py
   ```

## Usage

### Basic Usage

Run the scraper with default settings:
```bash
python run_scraper.py
```

### Custom Search

Modify `scraper_config.py` to customize:
- Search keywords
- Target locations
- Rate limiting
- Database settings

### Individual Scrapers

```python
from job_scraper import JobScraper

scraper = JobScraper()

# Run individual scrapers
indeed_jobs = scraper.scrape_indeed_jobs()
linkedin_jobs = scraper.scrape_linkedin_jobs()
spane4all_jobs = scraper.scrape_spane4all_jobs()

# Run all scrapers
results = scraper.run_all_scrapers()
```

### Database Queries

```python
# Get recent jobs
recent_jobs = scraper.get_recent_jobs(hours=24)

# Get jobs by source
indeed_jobs = scraper.get_jobs_by_source("Indeed South Africa", limit=50)
```

## Automation

### Cron Job Setup

Add to your crontab (`crontab -e`):
```bash
# Run daily at 6 AM
0 6 * * * /usr/bin/python3 /path/to/your/project/backend/run_scraper.py

# Run every 6 hours
0 */6 * * * /usr/bin/python3 /path/to/your/project/backend/run_scraper.py
```

### Docker Integration

Add to your Dockerfile:
```dockerfile
# Install Chrome
RUN apt-get update && apt-get install -y chromium-browser

# Install Python dependencies
COPY requirements-scraper.txt .
RUN pip install -r requirements-scraper.txt

# Copy scraper files
COPY job_scraper.py .
COPY scraper_config.py .
COPY run_scraper.py .
```

### CI/CD Pipeline

Example GitHub Actions workflow:
```yaml
name: Job Scraper
on:
  schedule:
    - cron: '0 6 * * *'  # Daily at 6 AM
  workflow_dispatch:  # Manual trigger

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: |
          sudo apt-get update
          sudo apt-get install -y chromium-browser
      - run: pip install -r backend/requirements-scraper.txt
      - run: python backend/run_scraper.py
```

## Configuration

### Search Keywords

Modify `DEFAULT_KEYWORDS` in `scraper_config.py`:
```python
DEFAULT_KEYWORDS = [
    "software developer",
    "web developer",
    "data scientist",
    "devops engineer",
    # Add your keywords here
]
```

### Target Locations

Modify `DEFAULT_LOCATIONS` in `scraper_config.py`:
```python
DEFAULT_LOCATIONS = [
    "South Africa",
    "Cape Town",
    "Johannesburg",
    # Add your locations here
]
```

### Rate Limiting

Adjust delays to avoid being blocked:
```python
MIN_DELAY = 2  # Minimum delay between requests (seconds)
MAX_DELAY = 5  # Maximum delay between requests (seconds)
```

## Database Schema

The scraper creates a SQLite database with the following structure:

```sql
CREATE TABLE job_listings (
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
);
```

## Logging

The scraper logs to both console and file (`job_scraper.log`):

```
2024-01-15 10:30:00 - INFO - Starting job scraping process
2024-01-15 10:30:01 - INFO - Running Indeed scraper...
2024-01-15 10:30:15 - INFO - Indeed scraper completed: 45 jobs found
2024-01-15 10:30:16 - INFO - Running LinkedIn scraper...
2024-01-15 10:30:45 - INFO - LinkedIn scraper completed: 32 jobs found
2024-01-15 10:30:46 - INFO - Running Spane4all scraper...
2024-01-15 10:31:00 - INFO - Spane4all scraper completed: 18 jobs found
2024-01-15 10:31:01 - INFO - Saved 95 new jobs to database
2024-01-15 10:31:01 - INFO - Scraping completed in 61.23 seconds
```

## Troubleshooting

### Common Issues

1. **ChromeDriver not found**:
   ```bash
   pip install webdriver-manager
   ```

2. **Permission denied**:
   ```bash
   chmod +x run_scraper.py
   ```

3. **Database locked**:
   - Ensure no other process is using the database
   - Check file permissions

4. **Site blocking**:
   - Increase delays in `scraper_config.py`
   - Use proxies (configure in `scraper_config.py`)
   - Rotate user agents

### Debug Mode

Enable debug logging:
```python
# In scraper_config.py
LOG_LEVEL = "DEBUG"
```

### Testing Individual Sites

```python
from job_scraper import JobScraper

scraper = JobScraper()

# Test Indeed only
jobs = scraper.scrape_indeed_jobs(["python developer"], ["Cape Town"])
print(f"Found {len(jobs)} jobs")
```

## Legal and Ethical Considerations

- **Respect robots.txt**: The scraper respects site robots.txt files
- **Rate limiting**: Built-in delays prevent overwhelming servers
- **Terms of service**: Ensure compliance with each site's terms
- **Data usage**: Use scraped data responsibly and in accordance with site policies

## Contributing

To add support for new job sites:

1. Create a new method in `JobScraper` class
2. Add site configuration to `SITE_CONFIGS`
3. Update the `run_all_scrapers` method
4. Test thoroughly with different keywords and locations

## License

This scraper is part of the CV Revamp Application and follows the same license terms.

## Support

For issues and questions:
1. Check the logs in `job_scraper.log`
2. Review the troubleshooting section
3. Check site structure changes (sites may update their HTML)
4. Verify network connectivity and firewall settings 