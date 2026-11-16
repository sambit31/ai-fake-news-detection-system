
import pandas as pd
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

EXTERNAL_PATH = BASE_DIR / "data" / "external" / "welFake_Dataset.csv"
TRAIN_PATH = BASE_DIR / "data" / "processed" / "cleaned_dataset.csv"
OUTPUT_PATH = BASE_DIR / "data" / "external" / "welFake_cleaned.csv"


def normalize(text):
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


print("\n========== EXTERNAL DATA PREPARATION ==========\n")

# Load datasets
external = pd.read_csv(EXTERNAL_PATH)
training = pd.read_csv(TRAIN_PATH)

print("Original external records:", len(external))

# Remove unnecessary index column
external = external.drop(
    columns=["Unnamed: 0"],
    errors="ignore"
)

# Keep required columns
external = external[["title", "text", "label"]].copy()

# Validate labels
external["label"] = pd.to_numeric(
    external["label"],
    errors="coerce"
)

external = external[
    external["label"].isin([0, 1])
].copy()

# Convert downloaded labels to project labels
# Downloaded: 0 = Real, 1 = Fake
# Project:    0 = Fake, 1 = Real
external["label"] = external["label"].map({
    0: 1,
    1: 0
}).astype(int)

# Build article text in the same format as training
external["title"] = external["title"].fillna("")
external["text"] = external["text"].fillna("")

external["article"] = (
    external["title"].astype(str)
    + " "
    + external["text"].astype(str)
).str.strip()

# Remove records without usable article content
external = external[
    external["article"].str.len() > 0
].copy()

# Normalize text for duplicate checking
external["normalized_article"] = (
    external["article"].apply(normalize)
)

# Remove duplicate articles within external dataset
external = external.drop_duplicates(
    subset=["normalized_article"]
).copy()

# Build training article text
training["title"] = training["title"].fillna("")
training["text"] = training["text"].fillna("")

training_articles = (
    training["title"].astype(str)
    + " "
    + training["text"].astype(str)
).apply(normalize)

training_set = set(training_articles)

# Remove articles already present in training data
before_overlap = len(external)

external = external[
    ~external["normalized_article"].isin(training_set)
].copy()

overlap_removed = before_overlap - len(external)

# Keep only required columns
external = external[
    ["title", "text", "article", "label"]
].copy()

# Save prepared external test dataset
external.to_csv(OUTPUT_PATH, index=False)

print("\n========== PREPARATION RESULTS ==========")
print("Final external records:", len(external))
print("Overlapping training articles removed:", overlap_removed)

print("\nFinal label distribution:")
print(external["label"].value_counts().sort_index())

print("\nLabel meaning:")
print("0 = Fake")
print("1 = Real")

print("\nMissing values:")
print(external.isnull().sum())

print("\nSaved to:", OUTPUT_PATH)
print("\n========== COMPLETED ==========")

