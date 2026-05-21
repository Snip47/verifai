import pandas as pd
import numpy as np
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import time

# ── Paths ──────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR    = os.path.join(BASE_DIR, "data", "processed")
MODELS_DIR  = os.path.join(BASE_DIR, "trained_models")
os.makedirs(MODELS_DIR, exist_ok=True)

# ── Load data ──────────────────────────────────────────
print("Loading processed data...")
train_df = pd.read_csv(os.path.join(DATA_DIR, "train.csv"))
val_df   = pd.read_csv(os.path.join(DATA_DIR, "val.csv"))
test_df  = pd.read_csv(os.path.join(DATA_DIR, "test.csv"))

X_train, y_train = train_df["content"], train_df["label"]
X_val,   y_val   = val_df["content"],   val_df["label"]
X_test,  y_test  = test_df["content"],  test_df["label"]

print(f"Train: {len(X_train)}  |  Val: {len(X_val)}  |  Test: {len(X_test)}")

# ── TF-IDF Vectorizer ──────────────────────────────────
print("\nFitting TF-IDF vectorizer...")
tfidf = TfidfVectorizer(
    max_features=50000,
    ngram_range=(1, 2),      # unigrams + bigrams
    sublinear_tf=True,       # apply log normalization
    min_df=2,                # ignore very rare terms
    strip_accents="unicode",
    analyzer="word"
)

X_train_tfidf = tfidf.fit_transform(X_train)
X_val_tfidf   = tfidf.transform(X_val)
X_test_tfidf  = tfidf.transform(X_test)

print(f"Vocabulary size: {len(tfidf.vocabulary_):,}")

# ── Train Logistic Regression ──────────────────────────
print("\nTraining Logistic Regression...")
start = time.time()

model = LogisticRegression(
    C=1.0,
    max_iter=1000,
    solver="lbfgs",
    n_jobs=-1,
    verbose=1
)
model.fit(X_train_tfidf, y_train)

elapsed = time.time() - start
print(f"Training time: {elapsed:.1f}s")

# ── Evaluate ───────────────────────────────────────────
def evaluate(name, X, y_true):
    y_pred = model.predict(X)
    acc  = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred)
    rec  = recall_score(y_true, y_pred)
    f1   = f1_score(y_true, y_pred)
    print(f"\n{'─'*40}")
    print(f"{name} Results")
    print(f"{'─'*40}")
    print(f"  Accuracy : {acc:.4f}  ({acc*100:.2f}%)")
    print(f"  Precision: {prec:.4f}")
    print(f"  Recall   : {rec:.4f}")
    print(f"  F1 Score : {f1:.4f}")
    print(f"\n{classification_report(y_true, y_pred, target_names=['Fake','Real'])}")
    return acc, prec, rec, f1

val_results  = evaluate("Validation", X_val_tfidf,  y_val)
test_results = evaluate("Test",       X_test_tfidf, y_test)

# ── Save model + vectorizer ────────────────────────────
print("\nSaving model and vectorizer...")

with open(os.path.join(MODELS_DIR, "logreg_model.pkl"), "wb") as f:
    pickle.dump(model, f)

with open(os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl"), "wb") as f:
    pickle.dump(tfidf, f)

print(f"Saved to {MODELS_DIR}")

# ── Save results summary ───────────────────────────────
results = {
    "model": "Logistic Regression + TF-IDF",
    "val_accuracy":  round(val_results[0],  4),
    "val_f1":        round(val_results[3],  4),
    "test_accuracy": round(test_results[0], 4),
    "test_f1":       round(test_results[3], 4),
}

results_df = pd.DataFrame([results])
results_df.to_csv(os.path.join(MODELS_DIR, "results.csv"), index=False)
print("\nResults summary saved.")
print("\n✓ Phase 2 baseline model complete!")