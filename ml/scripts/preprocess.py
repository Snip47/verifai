import pandas as pd
import numpy as np
import re
import os
from sklearn.model_selection import train_test_split

# ── Paths ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUT_DIR  = os.path.join(DATA_DIR, "processed")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Load ───────────────────────────────────────────────
print("Loading datasets...")
true_df = pd.read_csv(os.path.join(DATA_DIR, "True.csv"))
fake_df = pd.read_csv(os.path.join(DATA_DIR, "Fake.csv"))

true_df["label"] = 1   # 1 = real
fake_df["label"] = 0   # 0 = fake

df = pd.concat([true_df, fake_df], ignore_index=True)
print(f"Total samples: {len(df)}  |  Real: {true_df.shape[0]}  |  Fake: {fake_df.shape[0]}")

# ── Clean ──────────────────────────────────────────────
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)        # remove URLs
    text = re.sub(r"\[.*?\]", "", text)                # remove bracketed text
    text = re.sub(r"[^a-z0-9\s.,!?']", "", text)      # keep basic punctuation
    text = re.sub(r"\s+", " ", text).strip()           # collapse whitespace
    return text

print("Cleaning text...")
df["title"]   = df["title"].apply(clean_text)
df["text"]    = df["text"].apply(clean_text)

# Combine title + body for richer features
df["content"] = df["title"] + " " + df["text"]

# Drop rows with empty content
df = df[df["content"].str.len() > 20].reset_index(drop=True)

# ── Keep only what we need ─────────────────────────────
df = df[["content", "label"]]

# ── Split ──────────────────────────────────────────────
print("Splitting into train / val / test...")
train_df, temp_df = train_test_split(df, test_size=0.2,  random_state=42, stratify=df["label"])
val_df,   test_df = train_test_split(temp_df, test_size=0.5, random_state=42, stratify=temp_df["label"])

print(f"Train: {len(train_df)}  |  Val: {len(val_df)}  |  Test: {len(test_df)}")

# ── Save ───────────────────────────────────────────────
train_df.to_csv(os.path.join(OUT_DIR, "train.csv"), index=False)
val_df.to_csv(os.path.join(OUT_DIR,   "val.csv"),   index=False)
test_df.to_csv(os.path.join(OUT_DIR,  "test.csv"),  index=False)

print(f"Saved processed files to {OUT_DIR}")
print("Done! ✓")