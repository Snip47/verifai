import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base
from app.api.routes import router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="VerifAI API",
    description="AI-powered fake news detection API",
    version="1.0.0"
)

# CORS — allow React frontend to talk to the API
allowed_origins = [
    "http://localhost:3000",
    "https://verifai-nine.vercel.app",
    os.getenv("FRONTEND_URL", "https://verifai-nine.vercel.app")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

# Debug endpoint to check environment variables
@app.get("/api/debug/env")
def debug_env():
    return {
        "NEWS_API_KEY": "***" + os.getenv("NEWS_API_KEY", "NOT SET")[-10:] if os.getenv("NEWS_API_KEY") else "NOT SET",
        "DATABASE_URL": "SET" if os.getenv("DATABASE_URL") else "NOT SET",
        "PYTHONUNBUFFERED": os.getenv("PYTHONUNBUFFERED", "NOT SET"),
        "FRONTEND_URL": os.getenv("FRONTEND_URL", "NOT SET")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
