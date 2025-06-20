from pydantic import BaseModel
from datetime import datetime

class ResumeAnalysisOut(BaseModel):
    id: int
    resume_name: str
    resume_url: str
    job_description: str
    skills_score: float
    skills_reason: str
    education_score: float
    education_reason: str
    experience_score: float
    experience_reason: str
    job_role_score: float
    job_role_reason: str
    overall_score: float
    status: str
    final_reason: str
    created_at: datetime

    class Config:
        form_attributes = True