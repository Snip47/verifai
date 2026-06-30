from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import os
import sys
from app.db.database import get_db
from app.models.analysis import Analysis
from app.services.predictor import predict, reload_model
from app.services.scraper import scrape_article
from app.services.news import fetch_news

router = APIRouter()

class TextRequest(BaseModel):
    text: str

class UrlRequest(BaseModel):
    url: str

class AnalysisResponse(BaseModel):
    prediction:      str
    confidence:      float
    fake_score:      float
    real_score:      float
    title:           Optional[str] = None
    content_preview: str
    id:              int

@router.get("/")
def health_check():
    return {"status": "VerifAI API is running ✓", "version": "1.0.0"}

@router.post("/analyze/text", response_model=AnalysisResponse)
def analyze_text(request: TextRequest, db: Session = Depends(get_db)):
    if len(request.text.strip()) < 20:
        raise HTTPException(status_code=400, detail="Text too short.")
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
def get_history(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    analyses = db.query(Analysis).order_by(Analysis.created_at.desc()).offset(skip).limit(limit).all()
    return analyses

@router.delete("/history/clear")
def clear_history(db: Session = Depends(get_db)):
    db.query(Analysis).delete()
    db.commit()
    return {"message": "History cleared successfully"}

@router.delete("/history/{item_id}")
def delete_history_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Analysis).filter(Analysis.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted successfully"}

@router.get("/news")
def get_news(query: str = Query("latest"), page_size: int = Query(10)):
    result = fetch_news(query=query, page_size=page_size)
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.post("/news/analyze", response_model=AnalysisResponse)
def analyze_news_article(request: TextRequest, db: Session = Depends(get_db)):
    result = predict(request.text)
    record = Analysis(
        input_type  = "news",
        input_value = request.text[:500],
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

@router.post("/retrain")
def retrain_model():
    try:
        script_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            "ml", "scripts", "fetch_and_retrain.py"
        )
        import subprocess
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True, text=True, timeout=300
        )
        if result.returncode == 0:
            reload_model()
            return {"status": "success", "message": result.stdout}
        else:
            raise HTTPException(status_code=500, detail=result.stderr)
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=500, detail="Retraining timed out")
