import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

def upload_resume_to_cloudinary(file):
    result = cloudinary.uploader.upload(
        file,
        resource_type="raw",  # for PDF/DOCX
        folder="resumes"
    )
    return {
        "secure_url": result.get("secure_url"),
        "public_id": result.get("public_id"),
        "original_filename": result.get("original_filename")
    }