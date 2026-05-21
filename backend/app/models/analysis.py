from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from app.db.database import Base

class Analysis(Base):
    __tablename__ = "analyses"

    id           = Column(Integer, primary_key=True, index=True)
    input_type   = Column(String(10))   # "text" or "url"
    input_value  = Column(Text)         # original text or URL
    content      = Column(Text)         # cleaned content analyzed
    prediction   = Column(String(10))   # "REAL" or "FAKE"
    confidence   = Column(Float)        # e.g. 94.23
    fake_score   = Column(Float)
    real_score   = Column(Float)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())