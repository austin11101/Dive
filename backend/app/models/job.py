from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False, index=True)
    location = Column(String(255), nullable=True, index=True)
    description = Column(Text, nullable=True)
    salary = Column(String(255), nullable=True)
    job_type = Column(String(100), nullable=True)  # Full-time, Part-time, Contract, etc.
    experience_level = Column(String(100), nullable=True)  # Entry, Mid, Senior, etc.
    date_posted = Column(DateTime, nullable=True, index=True)
    application_deadline = Column(DateTime, nullable=True)
    link = Column(String(500), nullable=False, unique=True)
    source = Column(String(100), nullable=False, index=True)  # Indeed, LinkedIn, Spane4all
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
