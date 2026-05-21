import pickle
import os
import sys

# ── Paths ──────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "trained_models")

# ── Load model + vectorizer ────────────────────────────
print("Loading model...")
with open(os.path.join(MODELS_DIR, "logreg_model.pkl"), "rb") as f:
    model = pickle.load(f)

with open(os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl"), "rb") as f:
    tfidf = pickle.load(f)

print("Model loaded ✓\n")

# ── Predict function ───────────────────────────────────
def predict(text: str):
    vec   = tfidf.transform([text])
    pred  = model.predict(vec)[0]
    proba = model.predict_proba(vec)[0]

    label = "REAL" if pred == 1 else "FAKE"
    confidence = round(proba[pred] * 100, 2)
    fake_score = round(proba[0] * 100, 2)
    real_score = round(proba[1] * 100, 2)

    print(f"{'─'*50}")
    print(f"  Prediction : {label}")
    print(f"  Confidence : {confidence}%")
    print(f"  Fake score : {fake_score}%")
    print(f"  Real score : {real_score}%")
    print(f"{'─'*50}\n")

    return label, confidence

# ── Test samples ───────────────────────────────────────
print("Running test predictions...\n")

samples = [
    "Scientists at NASA confirm water found on Mars surface in large quantities",
    "BREAKING: President secretly replaced by clone, insider reveals shocking truth",
    "Kenya's inflation rate drops to 4.2% according to latest CBK report",
    "Doctors HATE him! Man cures cancer with this one simple trick they don't want you to know",
    "The Kenyan government has launched a new digital ID system to streamline public services",
]

for sample in samples:
    print(f"Text: {sample[:80]}...")
    predict(sample)

# ── Interactive mode ───────────────────────────────────
print("\nEnter your own text to test (type 'quit' to exit):")
while True:
    text = input("\n> ").strip()
    if text.lower() in ("quit", "exit", "q"):
        break
    if len(text) < 10:
        print("Please enter a longer text.")
        continue
    predict(text)