
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

EXTERNAL_PATH = BASE_DIR / "data/external/welFake_Dataset.csv"
TRAIN_PATH = BASE_DIR / "data/processed/cleaned_dataset.csv"


def normalize(text):
    if not isinstance(text, str):
        return ""
    return " ".join(text.lower().split())


# Load datasets
external = pd.read_csv(EXTERNAL_PATH)
training = pd.read_csv(TRAIN_PATH)

# Build article text
for df in [external, training]:
    df["title"] = df["title"].fillna("")
    df["text"] = df["text"].fillna("")

    df["article"] = (
        df["title"].astype(str)
        + " "
        + df["text"].astype(str)
    ).str.strip()

    df["normalized_article"] = df["article"].apply(normalize)

# Remove empty articles
external = external[external["normalized_article"] != ""].copy()
training = training[training["normalized_article"] != ""].copy()

# Convert WELFake labels to project labels
# Downloaded: 0 = Real, 1 = Fake
# Project:    0 = Fake, 1 = Real
external["project_label"] = external["label"].map({
    0: 1,
    1: 0
})

# Remove duplicate article texts for comparison
external_unique = external.drop_duplicates(
    subset="normalized_article"
).copy()

training_unique = training.drop_duplicates(
    subset="normalized_article"
).copy()

# Create training lookup
training_lookup = training_unique.set_index(
    "normalized_article"
)["label"]

# Find overlaps
external_unique["training_label"] = (
    external_unique["normalized_article"].map(training_lookup)
)

overlaps = external_unique[
    external_unique["training_label"].notna()
].copy()

# Compare labels
overlaps["label_match"] = (
    overlaps["project_label"] == overlaps["training_label"]
)

print("\n========== OVERLAP VERIFICATION ==========")

print("\nOriginal external rows:", len(pd.read_csv(EXTERNAL_PATH)))
print("External usable rows:", len(external))
print("Unique external articles:", len(external_unique))

print("\nOriginal training rows:", len(training))
print("Unique training articles:", len(training_unique))

print("\n========== OVERLAP RESULTS ==========")
print("Matching external articles:", len(overlaps))
print("Matching labels:", overlaps["label_match"].sum())
print("Conflicting labels:", (~overlaps["label_match"]).sum())

print("\n========== LABEL COMPARISON ==========")
print(pd.crosstab(
    overlaps["training_label"],
    overlaps["project_label"],
    rownames=["Training label"],
    colnames=["External label"]
))

print("\n========== NEW EXTERNAL ARTICLES ==========")
print(
    len(external_unique) - len(overlaps),
    "articles do not match the training dataset"
)

print("\n========== OVERLAP EXAMPLES ==========")
if len(overlaps):
    print(
        overlaps[
            ["title", "training_label", "project_label", "label_match"]
        ].head(5).to_string(index=False)
    )

print("\n========== VERIFICATION COMPLETED ==========")

