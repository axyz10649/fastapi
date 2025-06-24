from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from services.cloudinary_utils import upload_resume_to_cloudinary

router = APIRouter()

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF or DOCX files are allowed.")
    try:
        cloudinary_response = upload_resume_to_cloudinary(file.file)
        return {
            "fileName": file.filename,
            "message": "Resume uploaded successfully",
            "data": cloudinary_response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")



# @router.post("/upload-resumes")
# async def upload_resumes(files: List[UploadFile] = File(...)):
#     if not files:
#         raise HTTPException(status_code=400, detail="No files uploaded.")

#     uploaded_files = []

#     for file in files:
#         if not file.filename.lower().endswith(('.pdf', '.docx')):
#             raise HTTPException(status_code=400, detail=f"Invalid file type: {file.filename}. Only PDF or DOCX files are allowed.")

#         try:
#             cloudinary_response = upload_resume_to_cloudinary(file.file)
#             uploaded_files.append({
#                 "fileName": file.filename,
#                 "url": cloudinary_response.get("secure_url")  # assuming your function returns Cloudinary's upload response
#             })
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Upload failed for {file.filename}: {str(e)}")

#     return {
#         "message": "Resumes uploaded successfully",
#         "files": uploaded_files
#     }
