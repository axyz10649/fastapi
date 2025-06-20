import uuid
from datetime import datetime

def mock_llm_response(resume_url: str, job_description: str):
    return {
        "resume_name": resume_url.split("/")[-1],
        "skills": {"score": 82, "reason": "Good match with JD keywords"},
        "education": {"score": 70, "reason": "Sufficient academic background"},
        "experience": {"score": 90, "reason": "Relevant industry experience"},
        "job_role": {"score": 85, "reason": "Similar job role in past"},
        "overall_score": 82,
        "status": "shortlisted",
        "final_reason": "Strong match across skills and experience"
    }


# for using async function
# import httpx

# async def real_llm_response(resume_url: str, job_description: str):
#     payload = {
#         "resume_url": resume_url,
#         "job_description": job_description
#     }

#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.post("https://www.google.com", json=payload)
#             response.raise_for_status()
#             return response.json()
#     except httpx.HTTPError as e:
#         raise RuntimeError(f"LLM request failed: {str(e)}")
