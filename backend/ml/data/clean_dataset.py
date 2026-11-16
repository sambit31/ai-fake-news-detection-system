
import re
import pandas as pd
from pathlib import Path


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = DATA_DIR / "processed"

OUTPUT_FILE = OUTPUT_DIR / "cleaned_dataset.csv"


# ============================================================
# 2. LOAD DATASETS
# ============================================================

def load_dataset(folder_name, file_name):

    path = DATA_DIR / folder_name / file_name

    if not path.is_file():
        raise FileNotFoundError(f"Dataset not found: {path}")

    for encoding in ["utf-8", "latin-1", "cp1252"]:

        try:
            print(f"Loading: {path}")
            return pd.read_csv(path, encoding=encoding)

        except UnicodeDecodeError:
            continue

    raise ValueError(f"Could not decode dataset: {path}")


# ============================================================
# 3. TEXT NORMALIZATION
# ============================================================

def normalize(text):

    text = str(text).lower()

    text = re.sub(r"http\S+|www\.\S+", " ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)

    return re.sub(r"\s+", " ", text).strip()


# ============================================================
# 4. DATASET CLEANING
# ============================================================

def clean_dataset():

    print("\n========== DATA CLEANING STARTED ==========")

    # --------------------------------------------------------
    # STEP 1: LOAD DATA
    # --------------------------------------------------------

    real = load_dataset("True.csv", "True.csv")
    fake = load_dataset("Fake.csv", "Fake.csv")

    real.columns = real.columns.str.strip().str.lower()
    fake.columns = fake.columns.str.strip().str.lower()

    real["label"] = 1
    fake["label"] = 0

    data = pd.concat(
        [real, fake],
        ignore_index=True
    )

    print("\nOriginal dataset size:", len(data))

    # --------------------------------------------------------
    # STEP 2: CHECK REQUIRED COLUMNS
    # --------------------------------------------------------

    required_columns = ["title", "text", "subject", "date"]

    for column in required_columns:

        if column not in data.columns:
            data[column] = ""

    data["title"] = data["title"].fillna("").astype(str)
    data["text"] = data["text"].fillna("").astype(str)

    data["subject"] = (
        data["subject"].fillna("Unknown").astype(str)
    )

    data["date"] = data["date"].fillna("").astype(str)

    # --------------------------------------------------------
    # STEP 3: REMOVE EMPTY RECORDS
    # --------------------------------------------------------

    empty_title = data["title"].str.strip().eq("")
    empty_text = data["text"].str.strip().eq("")

    print("\nEmpty titles:", empty_title.sum())
    print("Empty articles:", empty_text.sum())

    invalid_mask = empty_title | empty_text

    data = data.loc[~invalid_mask].copy()

    print("Records after removing empty data:", len(data))

    # --------------------------------------------------------
    # STEP 4: CREATE NORMALIZED ARTICLE KEY
    # --------------------------------------------------------

    print("\nGenerating normalized article keys...")

    data["_normalized_article"] = (
        data["title"].apply(normalize)
        + " "
        + data["text"].apply(normalize)
    )

    # --------------------------------------------------------
    # STEP 5: CHECK LABEL CONFLICTS
    # --------------------------------------------------------

    label_counts = data.groupby(
        "_normalized_article"
    )["label"].nunique()

    conflicting_keys = label_counts[
        label_counts > 1
    ]

    print(
        "Cross-label duplicate groups:",
        len(conflicting_keys)
    )

    if not conflicting_keys.empty:
        raise ValueError(
            "Conflicting duplicate articles detected. "
            "Investigate them before removing duplicates."
        )

    # --------------------------------------------------------
    # STEP 6: REMOVE DUPLICATES
    # --------------------------------------------------------

    duplicate_count = data.duplicated(
        subset=["_normalized_article"],
        keep="first"
    ).sum()

    print("Duplicate rows to remove:", duplicate_count)

    data = data.drop_duplicates(
        subset=["_normalized_article"],
        keep="first"
    ).copy()

    print("Records after deduplication:", len(data))

    # --------------------------------------------------------
    # STEP 7: REMOVE TEMPORARY COLUMN
    # --------------------------------------------------------

    data.drop(
        columns=["_normalized_article"],
        inplace=True
    )

    # --------------------------------------------------------
    # STEP 8: FINAL DATASET VALIDATION
    # --------------------------------------------------------

    print("\n========== CLEANING SUMMARY ==========")

    print("Final dataset size:", len(data))

    print("Real articles:", (data["label"] == 1).sum())
    print("Fake articles:", (data["label"] == 0).sum())

    print(
        "Remaining duplicate rows:",
        data.duplicated(
            subset=["title", "text"]
        ).sum()
    )

    print(
        "Remaining empty articles:",
        data["text"].str.strip().eq("").sum()
    )

    print("\nClass distribution:")

    print(data["label"].value_counts())

    # --------------------------------------------------------
    # STEP 9: SAVE CLEANED DATASET
    # --------------------------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    data.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8"
    )

    print("\nCleaned dataset saved successfully!")

    print("Output:", OUTPUT_FILE)

    print("\n========== DATA CLEANING COMPLETED ==========")


# ============================================================
# 5. MAIN
# ============================================================

if __name__ == "__main__":
    clean_dataset()

