from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, or_
from typing import List, Optional
from datetime import datetime, timedelta
import asyncio

from app.core.database import get_db
from app.models.job import Job
from scraper.unified_scraper import scrape_jobs_unified, scrape_jobs_single_site, UnifiedJobScraper

router = APIRouter(tags=["jobs"])

@router.get("/jobs", response_model=List[dict])
async def get_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    company: Optional[str] = None,
    location: Optional[str] = None,
    source: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all jobs with optional filtering
    """
    query = db.query(Job).filter(Job.is_active == True)
    
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (Job.title.ilike(search_filter)) |
            (Job.description.ilike(search_filter)) |
            (Job.company.ilike(search_filter))
        )
    
    if company:
        query = query.filter(Job.company.ilike(f"%{company}%"))
    
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    
    if source:
        query = query.filter(Job.source == source)
    
    jobs = query.offset(skip).limit(limit).all()
    
    return [
        {
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "description": job.description,
            "salary": job.salary,
            "job_type": job.job_type,
            "experience_level": job.experience_level,
            "date_posted": job.date_posted,
            "link": job.link,
            "source": job.source,
            "created_at": job.created_at
        }
        for job in jobs
    ]

@router.post("/scrape")
async def trigger_scrape(
    query: str = Query("python developer"),
    location: str = Query("south africa"),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Trigger manual scraping of job listings
    """
    try:
        # Use unified scraper for all locations
        jobs_data = await scrape_jobs_unified(query=query, location=location, max_jobs=limit)

        # Save jobs to database
        saved_count = 0
        for job_data in jobs_data:
            # Check if job already exists
            existing_job = db.query(Job).filter(Job.link == job_data["link"]).first()
            if not existing_job:
                job = Job(
                    title=job_data["title"],
                    company=job_data["company"],
                    location=job_data["location"],
                    description=job_data.get("description", ""),
                    salary=job_data.get("salary", ""),
                    job_type=job_data.get("job_type", ""),
                    experience_level=job_data.get("experience_level", ""),
                    date_posted=job_data.get("date_posted"),
                    link=job_data["link"],
                    source=job_data["source"]
                )
                db.add(job)
                saved_count += 1
        
        db.commit()
        
        return {
            "message": f"Scraping completed successfully",
            "scraped_count": len(jobs_data),
            "saved_count": saved_count,
            "query": query,
            "location": location
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

@router.delete("/jobs/mock")
async def clear_mock_data(db: Session = Depends(get_db)):
    """
    Clear mock/sample data from the database
    """
    try:
        # Delete jobs with mock company names or sample links
        mock_companies = ["TechCorp Inc.", "StartupXYZ", "BigTech Company"]
        sample_links = ["https://indeed.com/viewjob?jk=sample", "https://example.com/job"]

        deleted_count = db.query(Job).filter(
            or_(
                Job.company.in_(mock_companies),
                Job.link.like("%sample%"),
                Job.link.like("%example.com%")
            )
        ).delete(synchronize_session=False)

        db.commit()

        return {
            "message": "Mock data cleared successfully",
            "deleted_count": deleted_count
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to clear mock data: {str(e)}")

@router.post("/scrape-efficient")
async def scrape_jobs_efficient(
    query: str = Query("software developer", description="Job search query"),
    location: str = Query("South Africa", description="Job location"),
    keywords: str = Query("", description="Comma-separated target keywords"),
    max_jobs: int = Query(20, description="Maximum number of jobs to scrape"),
    sites: str = Query("", description="Comma-separated list of sites to scrape"),
    db: Session = Depends(get_db)
):
    """
    Efficient job scraping with async requests, deduplication, and relevance scoring
    """
    try:
        # Parse keywords and sites
        target_keywords = [k.strip() for k in keywords.split(",") if k.strip()] if keywords else []
        site_list = [s.strip() for s in sites.split(",") if s.strip()] if sites else None
        
        # Run the unified scraper
        if site_list and len(site_list) == 1:
            # Single site scraping
            jobs_data = await scrape_jobs_single_site(
                site=site_list[0],
                query=query,
                location=location,
                max_jobs=max_jobs
            )
        else:
            # Multi-site scraping
            jobs_data = await scrape_jobs_unified(
                query=query,
                location=location,
                max_jobs=max_jobs
            )
        
        # Save jobs to database
        saved_count = 0
        for job_data in jobs_data:
            # Check if job already exists
            existing_job = db.query(Job).filter(Job.link == job_data["link"]).first()
            if not existing_job:
                db_job = Job(
                    title=job_data["title"],
                    company=job_data["company"],
                    location=job_data["location"],
                    description=job_data.get("description", f"Job opportunity at {job_data['company']}"),
                    salary=job_data.get("salary", "Competitive"),
                    job_type=job_data.get("job_type", "Full-time"),
                    experience_level=job_data.get("experience_level", "Mid"),
                    date_posted=job_data.get("date_posted"),
                    link=job_data["link"],
                    source=job_data["source"],
                    is_active=True
                )
                
                db.add(db_job)
                saved_count += 1
        
        db.commit()
        
        return {
            "message": "Efficient scraping completed successfully",
            "scraped_count": len(jobs_data),
            "saved_count": saved_count,
            "query": query,
            "location": location,
            "keywords": target_keywords,
            "sites_used": site_list or ["all available sites"]
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Efficient scraping failed: {str(e)}")

@router.get("/stats")
async def get_statistics(db: Session = Depends(get_db)):
    """
    Get job statistics
    """
    # Jobs per company
    jobs_per_company = db.query(
        Job.company,
        func.count(Job.id).label('count')
    ).filter(Job.is_active == True).group_by(Job.company).order_by(desc('count')).limit(10).all()
    
    # Jobs per source
    jobs_per_source = db.query(
        Job.source,
        func.count(Job.id).label('count')
    ).filter(Job.is_active == True).group_by(Job.source).all()
    
    # Jobs per experience level
    jobs_per_level = db.query(
        Job.experience_level,
        func.count(Job.id).label('count')
    ).filter(Job.is_active == True, Job.experience_level.isnot(None)).group_by(Job.experience_level).all()
    
    # Total jobs
    total_jobs = db.query(func.count(Job.id)).filter(Job.is_active == True).scalar()
    
    # Jobs posted today
    today = datetime.now().date()
    jobs_today = db.query(func.count(Job.id)).filter(
        Job.is_active == True,
        func.date(Job.date_posted) == today
    ).scalar()
    
    return {
        "total_jobs": total_jobs,
        "jobs_today": jobs_today,
        "jobs_per_company": [{"company": item.company, "count": item.count} for item in jobs_per_company],
        "jobs_per_source": [{"source": item.source, "count": item.count} for item in jobs_per_source],
        "jobs_per_level": [{"level": item.experience_level, "count": item.count} for item in jobs_per_level]
    }
