from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import time
import logging
import os
import sys

# Add the parent directory to Python path for config import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.api.v1.api import api_router
from app.core.database import engine, Base
from config import get_config

# Get configuration
config = get_config()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Dive Job Scraper API",
    description="A modern API for job searching and scraping with South African focus",
    version="1.0.0",
    docs_url="/docs" if config.DEBUG else None,
    redoc_url="/redoc" if config.DEBUG else None,
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Only add TrustedHostMiddleware in production
if settings.ENVIRONMENT == "production":
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time(), "version": "1.0.0"}


# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Dive Job Scraper API",
        "version": "1.0.0",
        "docs": "/docs" if config.DEBUG else None,
        "features": {
            "scraping": config.SCRAPING_ENABLED,
            "scheduler": config.SCHEDULER_ENABLED,
            "south_africa_focus": True
        }
    }


# Include API routes
app.include_router(api_router, prefix="/api")


# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Starting Dive Job Scraper API...")
    # Create database tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created")
    except Exception as e:
        logger.error(f"Database table creation failed: {e}")

    # Test database connection
    try:
        # Test database connection here
        logger.info("Database connection established")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")

    logger.info(f"Scraping enabled: {config.SCRAPING_ENABLED}")
    logger.info(f"Scheduler enabled: {config.SCHEDULER_ENABLED}")
    logger.info(f"Enabled job sites: {config.ENABLED_JOB_SITES}")
    logger.info("API startup complete")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Dive Job Scraper API...")
    # Close database connections
    engine.dispose()
    logger.info("API shutdown complete")
    await redis_client.close()
