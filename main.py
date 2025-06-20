from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import upload, analyze
from database import init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB tables
init_db()

app.include_router(upload.router)
app.include_router(analyze.router)