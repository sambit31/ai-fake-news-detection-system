
import re
from numpy import real
import pandas as pd
from pathlib import Path


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"


# ============================================================
# 2. LOAD DATASETS
# ============================================================
def load_dataset(folder_name, file_name):

    path = DATA_DIR / folder_name / file_name

    if not path.is_file():
        raise FileNotFoundError(
            f"Dataset file not found: {path}"
        )

    for encoding in ["utf-8", "latin-1", "cp1252"]:

        try:
            print(f"Loading: {path}")

            return pd.read_csv(
                path,
                encoding=encoding
            )

        except UnicodeDecodeError:
            continue

    raise ValueError(f"Could not read dataset: {path}")

# ============================================================
# 3. NORMALIZE TEXT
# ============================================================

def normalize(text):

    text = str(text).lower()

    text = re.sub(
        r"http\S+|www\.\S+",
        " ",
        text
    )

    text = re.sub(
        r"[^a-z0-9]+",
        " ",
        text
    )

    return re.sub(
        r"\s+",
        " ",
        text
    ).strip()


# ============================================================
# 4. DATASET AUDIT
# ============================================================

def inspect_dataset():

    # Load datasets directly from the data directory
    real = load_dataset("True.csv", "True.csv")
    fake = load_dataset("Fake.csv", "Fake.csv")

    # Standardize column names
    real.columns = real.columns.str.strip().str.lower()
    fake.columns = fake.columns.str.strip().str.lower()

    # Assign labels
    real["label"] = 1
    fake["label"] = 0

    # Combine datasets
    data = pd.concat(
        [real, fake],
        ignore_index=True
    )

    print("\n========== DATASET AUDIT ==========")

    # --------------------------------------------------------
    # 1. DATASET SIZE
    # --------------------------------------------------------

    print("\n1. DATASET SIZE")

    print("Total articles:", len(data))
    print("Real articles:", (data["label"] == 1).sum())
    print("Fake articles:", (data["label"] == 0).sum())

    # --------------------------------------------------------
    # 2. REQUIRED COLUMNS
    # --------------------------------------------------------

    for column in ["title", "text", "subject", "date"]:

        if column not in data.columns:
            data[column] = ""

    data["title"] = data["title"].fillna("").astype(str)
    data["text"] = data["text"].fillna("").astype(str)
    data["subject"] = data["subject"].fillna("Unknown").astype(str)
    data["date"] = data["date"].fillna("").astype(str)

    # --------------------------------------------------------
    # 3. SUBJECT DISTRIBUTION
    # --------------------------------------------------------

    print("\n2. SUBJECT DISTRIBUTION")

    print(
        pd.crosstab(
            data["subject"],
            data["label"],
            margins=True
        )
    )

    # --------------------------------------------------------
    # 4. ARTICLE LENGTH ANALYSIS
    # --------------------------------------------------------

    print("\n3. ARTICLE LENGTH ANALYSIS")

    data["text_length"] = data["text"].str.len()
    data["title_length"] = data["title"].str.len()

    print(
        data.groupby("label")[
            ["text_length", "title_length"]
        ].describe().round(2)
    )

    # --------------------------------------------------------
    # 5. DATE ANALYSIS
    # --------------------------------------------------------

    print("\n4. DATE ANALYSIS")

    data["parsed_date"] = pd.to_datetime(
        data["date"],
        errors="coerce",
        utc=True
    )

    for label, name in [(0, "FAKE"), (1, "REAL")]:

        subset = data[data["label"] == label]
        valid = subset["parsed_date"].dropna()

        print(f"\n{name}")

        print("Valid dates:", len(valid))
        print("Invalid dates:", len(subset) - len(valid))

        if not valid.empty:

            print("Earliest:", valid.min())
            print("Latest:", valid.max())

            print("\nYear distribution:")

            print(
                valid.dt.year.value_counts().sort_index()
            )

    # --------------------------------------------------------
    # 6. TITLE OVERLAP
    # --------------------------------------------------------

    print("\n5. TITLE OVERLAP")

    data["normalized_title"] = data["title"].apply(normalize)

    title_counts = (
        data.groupby("normalized_title")["label"].nunique()
    )

    conflicting_titles = title_counts[title_counts > 1]

    print(
        "Conflicting title groups:",
        len(conflicting_titles)
    )

    # --------------------------------------------------------
    
    # --------------------------------------------------------
    # 7. DUPLICATE INVESTIGATION
    # --------------------------------------------------------

    print("\n6. DUPLICATE INVESTIGATION")

    data["normalized_article"] = (
        data["title"] + " " + data["text"]
    ).apply(normalize)

    # Number of duplicate rows
    duplicate_mask = data["normalized_article"].duplicated(
        keep="first"
    )

    print("Total duplicate rows:", duplicate_mask.sum())

    # Same article appearing with different labels
    label_counts = data.groupby(
        "normalized_article"
    )["label"].nunique()

    conflicting_groups = label_counts[label_counts > 1]

    print(
        "Cross-label duplicate groups:",
        len(conflicting_groups)
    )

    # Rows belonging to cross-label duplicate groups
    conflict_mask = data["normalized_article"].isin(
        conflicting_groups.index
    )

    print(
        "Rows in cross-label duplicate groups:",
        conflict_mask.sum()
    )

    # Duplicate rows within the same label
    print(
        "Same-label duplicate rows:",
        (
            data.duplicated(
                subset=["normalized_article", "label"],
                keep="first"
            )
        ).sum()
    )

    # --------------------------------------------------------
    # 8. VERIFY ARTICLE LENGTHS
    # --------------------------------------------------------

    print("\n7. ARTICLE LENGTH VERIFICATION")

    for label, name in [(0, "FAKE"), (1, "REAL")]:

        subset = data[data["label"] == label]

        print(f"\n{name}")

        print("\nArticle length:")

        print(subset["text"].str.len().describe())

        print("\nTitle length:")

        print(subset["title"].str.len().describe())


    # --------------------------------------------------------
    # 8. EMPTY AND MISSING DATA
    # --------------------------------------------------------

    print("\n7. EMPTY AND MISSING DATA")

    print(
        "Empty titles:",
        (data["title"].str.strip() == "").sum()
    )

    print(
        "Empty articles:",
        (data["text"].str.strip() == "").sum()
    )

    # --------------------------------------------------------
    # 9. SUBJECT-LABEL DISTRIBUTION
    # --------------------------------------------------------

    print("\n8. SUBJECT-LABEL DISTRIBUTION")

    print(
        pd.crosstab(
            data["subject"],
            data["label"],
            normalize="index"
        ).round(3)
    )

    print("\n========== AUDIT COMPLETED ==========")


# ============================================================
# 5. MAIN
# ============================================================

if __name__ == "__main__":
    inspect_dataset()

