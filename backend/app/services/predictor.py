import pickle
import os
import re

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MODELS_DIR = os.path.join(BASE_DIR, "ml", "trained_models")

print(f"Loading model from {MODELS_DIR}...")

with open(os.path.join(MODELS_DIR, "logreg_model.pkl"), "rb") as f:
    model = pickle.load(f)

with open(os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl"), "rb") as f:
    tfidf = pickle.load(f)

print("Model loaded ✓")

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"[^a-z0-9\s.,!?']", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def predict(text: str) -> dict:
    cleaned  = clean_text(text)
    vec      = tfidf.transform([cleaned])
    pred     = model.predict(vec)[0]
    proba    = model.predict_proba(vec)[0]

    label      = "REAL" if pred == 1 else "FAKE"
    confidence = round(float(proba[pred]) * 100, 2)
    fake_score = round(float(proba[0]) * 100, 2)
    real_score = round(float(proba[1]) * 100, 2)

    return {
        "prediction": label,
        "confidence": confidence,
        "fake_score": fake_score,
        "real_score": real_score,
        "cleaned_content": cleaned[:500]
    }