from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from services.llm_service import mock_llm_response
from sqlalchemy.orm import Session
from database import SessionLocal
from models import ResumeAnalysis
from schemas import ResumeAnalysisOut
import os
from datetime import datetime

router = APIRouter()
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

class AnalyzeRequest(BaseModel):
    resume_urls: List[str]  # Accept list of resume URLs
    job_description: str

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/analyze")
async def analyze_resume(request: AnalyzeRequest, db: Session = Depends(get_db)):
    try:
        response = mock_llm_response(request.resume_url, request.job_description)

        analysis = ResumeAnalysis(
            resume_name=response["resume_name"],
            resume_url=request.resume_url,
            job_description=request.job_description,
            skills_score=response["skills"]["score"],
            skills_reason=response["skills"]["reason"],
            education_score=response["education"]["score"],
            education_reason=response["education"]["reason"],
            experience_score=response["experience"]["score"],
            experience_reason=response["experience"]["reason"],
            job_role_score=response["job_role"]["score"],
            job_role_reason=response["job_role"]["reason"],
            overall_score=response["overall_score"],
            status=response["status"],
            final_reason=response["final_reason"]
        )
        db.add(analysis)
        db.commit()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_content = f"""
[ANALYSIS LOG] - {timestamp}
Resume: {response['resume_name']}
Overall Score: {response['overall_score']}%
Status: {response['status']}
Reason: {response['final_reason']}

Details:
- Skills: {response['skills']['score']}% | {response['skills']['reason']}
- Education: {response['education']['score']}% | {response['education']['reason']}
- Experience: {response['experience']['score']}% | {response['experience']['reason']}
- Job Role: {response['job_role']['score']}% | {response['job_role']['reason']}
"""
        log_file = os.path.join(LOGS_DIR, f"{response['resume_name']}_log.txt")
        with open(log_file, "w") as f:
            f.write(log_content.strip())

        return {"message": "Resume analyzed successfully", "data": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/results", response_model=list[ResumeAnalysisOut])
def get_results(db: Session = Depends(get_db)):
    results = db.query(ResumeAnalysis).order_by(ResumeAnalysis.created_at.desc()).all()
    return results









# @router.post("/analyze")
# async def analyze_resumes(request: AnalyzeRequest, db: Session = Depends(get_db)):
#     responses = []

#     for resume_url in request.resume_urls:
#         try:
#             response = mock_llm_response(resume_url, request.job_description)

#             analysis = ResumeAnalysis(
#                 resume_name=response["resume_name"],
#                 resume_url=resume_url,
#                 job_description=request.job_description,
#                 skills_score=response["skills"]["score"],
#                 skills_reason=response["skills"]["reason"],
#                 education_score=response["education"]["score"],
#                 education_reason=response["education"]["reason"],
#                 experience_score=response["experience"]["score"],
#                 experience_reason=response["experience"]["reason"],
#                 job_role_score=response["job_role"]["score"],
#                 job_role_reason=response["job_role"]["reason"],
#                 overall_score=response["overall_score"],
#                 status=response["status"],
#                 final_reason=response["final_reason"]
#             )
#             db.add(analysis)
#             db.commit()

#             # Logging
#             timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             log_content = f"""
# [ANALYSIS LOG] - {timestamp}
# Resume: {response['resume_name']}
# Overall Score: {response['overall_score']}%
# Status: {response['status']}
# Reason: {response['final_reason']}

# Details:
# - Skills: {response['skills']['score']}% | {response['skills']['reason']}
# - Education: {response['education']['score']}% | {response['education']['reason']}
# - Experience: {response['experience']['score']}% | {response['experience']['reason']}
# - Job Role: {response['job_role']['score']}% | {response['job_role']['reason']}
# """
#             log_file = os.path.join(LOGS_DIR, f"{response['resume_name']}_log.txt")
#             with open(log_file, "w") as f:
#                 f.write(log_content.strip())

#             responses.append(response)

#         except Exception as e:
#             responses.append({
#                 "resume_url": resume_url,
#                 "error": f"Analysis failed: {str(e)}"
#             })

#     return {
#         "message": "Resumes analyzed",
        # "results": responses
    # }
