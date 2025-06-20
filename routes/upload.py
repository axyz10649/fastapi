from fastapi import APIRouter, UploadFile, File, HTTPException
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