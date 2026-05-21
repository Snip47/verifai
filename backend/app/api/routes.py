from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl
from typing import Optional
from app.db.database import get_db
from app.models.analysis import Analysis
from app.services.predictor import predict
from app.services.scraper import scrape_article

router = APIRouter()

# ── Schemas ────────────────────────────────────────────
class TextRequest(BaseModel):
    text: str

class UrlRequest(BaseModel):
    url: str

class AnalysisResponse(BaseModel):
    prediction:  str
    confidence:  float
    fake_score:  float
    real_score:  float
    title:       Optional[str] = None
    content_preview: str
    id:          int

# ── Routes ─────────────────────────────────────────────
@router.get("/")
def health_check():
    return {"status": "VerifAI API is running ✓", "version": "1.0.0"}

@router.post("/analyze/text", response_model=AnalysisResponse)
def analyze_text(request: TextRequest, db: Session = Depends(get_db)):
    if len(request.text.strip()) < 20:
        raise HTTPException(status_code=400, detail="Text too short. Please provide at least 20 characters.")

    result = predict(request.text)

    record = Analysis(
        input_type  = "text",
        input_value = request.text[:1000],
        content     = result["cleaned_content"],
        prediction  = result["prediction"],
        confidence  = result["confidence"],
        fake_score  = result["fake_score"],
        real_score  = result["real_score"]
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return AnalysisResponse(
        prediction      = result["prediction"],
        confidence      = result["confidence"],
        fake_score      = result["fake_score"],
        real_score      = result["real_score"],
        content_preview = result["cleaned_content"][:200],
        id              = record.id
    )

@router.post("/analyze/url", response_model=AnalysisResponse)
def analyze_url(request: UrlRequest, db: Session = Depends(get_db)):
    scraped = scrape_article(request.url)

    if not scraped["success"]:
        raise HTTPException(status_code=422, detail=scraped["error"])

    result = predict(scraped["content"])

    record = Analysis(
        input_type  = "url",
        input_value = request.url,
        content     = result["cleaned_content"],
        prediction  = result["prediction"],
        confidence  = result["confidence"],
        fake_score  = result["fake_score"],
        real_score  = result["real_score"]
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return AnalysisResponse(
        prediction      = result["prediction"],
        confidence      = result["confidence"],
        fake_score      = result["fake_score"],
        real_score      = result["real_score"],
        title           = scraped.get("title"),
        content_preview = result["cleaned_content"][:200],
        id              = record.id
    )

@router.get("/history")
def get_history(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    analyses = db.query(Analysis).order_by(Analysis.created_at.desc()).offset(skip).limit(limit).all()
    return analyses