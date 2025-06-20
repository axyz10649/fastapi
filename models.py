from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ResumeAnalysis(Base):
    __tablename__ = "resume_analysis"

    id = Column(Integer, primary_key=True, index=True)
    resume_name = Column(String)
    resume_url = Column(String)
    job_description = Column(String)
    skills_score = Column(Float)
    skills_reason = Column(String)
    education_score = Column(Float)
    education_reason = Column(String)
    experience_score = Column(Float)
    experience_reason = Column(String)
    job_role_score = Column(Float)
    job_role_reason = Column(String)
    overall_score = Column(Float)
    status = Column(String)
    final_reason = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
