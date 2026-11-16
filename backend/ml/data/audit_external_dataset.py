
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    BASE_DIR / "data" / "external" / "welFake_Dataset.csv"
)

print("\n========== WELFAKE DATASET AUDIT ==========\n")

if not DATASET_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATASET_PATH}"
    )

# Load dataset
try:
    df = pd.read_csv(DATASET_PATH)
except UnicodeDecodeError:
    df = pd.read_csv(DATASET_PATH, encoding="latin1")

# Basic information
print("Dataset path:", DATASET_PATH)
print("Dataset shape:", df.shape)

print("\n========== COLUMNS ==========")
print(df.columns.tolist())

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== DUPLICATE ROWS ==========")
print("Exact duplicate rows:", df.duplicated().sum())

# Identify possible label columns
possible_labels = [
    col for col in df.columns
    if col.lower() in ["label", "class", "target", "category"]
]

print("\n========== POSSIBLE LABEL COLUMNS ==========")
print(possible_labels)

for col in possible_labels:
    print(f"\nDistribution for '{col}':")
    print(df[col].value_counts(dropna=False))

# Display sample records
print("\n========== FIRST 5 RECORDS ==========")
print(df.head().to_string())

# Display text samples
for col in df.columns:
    if col.lower() in ["text", "article", "content"]:
        print(f"\n========== SAMPLE {col.upper()} ==========")
        for value in df[col].dropna().head(2):
            print(str(value)[:500])
            print("-" * 60)

print("\n========== AUDIT COMPLETED ==========")

