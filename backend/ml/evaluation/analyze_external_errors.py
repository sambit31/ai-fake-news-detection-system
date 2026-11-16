
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = BASE_DIR / "data/external/welFake_cleaned.csv"

PREDICTION_PATH = (
    BASE_DIR / "ml/artifacts/external_predictions.csv"
)

OUTPUT_PATH = (
    BASE_DIR / "ml/artifacts/external_errors.csv"
)

print("\n========== EXTERNAL ERROR ANALYSIS ==========\n")

df = pd.read_csv(DATA_PATH)
pred = pd.read_csv(PREDICTION_PATH)

if len(df) != len(pred):
    raise ValueError("Dataset and prediction row counts do not match.")

df["predicted_label"] = pred["predicted_label"].values
df["correct"] = pred["correct"].values

if "decision_score" in pred.columns:
    df["decision_score"] = pred["decision_score"].values

# Identify errors
errors = df[df["correct"] == False].copy()

# Identify error types
false_real = errors[
    (errors["label"] == 0) &
    (errors["predicted_label"] == 1)
]

false_fake = errors[
    (errors["label"] == 1) &
    (errors["predicted_label"] == 0)
]

print("Total external articles:", len(df))
print("Total incorrect predictions:", len(errors))

print("\n========== ERROR TYPES ==========")

print(
    "Fake classified as Real:",
    len(false_real)
)

print(
    "Real classified as Fake:",
    len(false_fake)
)

print("\n========== ERROR PERCENTAGES ==========")

print(
    "Fake misclassification rate:",
    round(len(false_real) / (df["label"] == 0).sum() * 100, 2),
    "%"
)

print(
    "Real misclassification rate:",
    round(len(false_fake) / (df["label"] == 1).sum() * 100, 2),
    "%"
)

# Decision score analysis
if "decision_score" in df.columns:
    print("\n========== DECISION SCORE ANALYSIS ==========")

    print(
        df.groupby("label")["decision_score"]
        .agg(["count", "mean", "std", "min", "max"])
    )

    print("\nScores by actual and predicted class:")

    print(
        df.groupby(["label", "predicted_label"])["decision_score"]
        .agg(["count", "mean", "std"])
    )

# Article length analysis
df["article_length"] = df["article"].fillna("").str.len()

print("\n========== ARTICLE LENGTH ANALYSIS ==========")

print(
    df.groupby(["label", "predicted_label"])["article_length"]
    .agg(["count", "mean", "median"])
)

# Save all errors
errors.to_csv(OUTPUT_PATH, index=False)

print("\n========== FALSE POSITIVE EXAMPLES ==========")

for _, row in false_fake.head(5).iterrows():
    print("\nTITLE:", row["title"])
    print("ACTUAL: Real")
    print("PREDICTED: Fake")
    print("ARTICLE:", str(row["text"])[:500])

    if "decision_score" in row:
        print("DECISION SCORE:", row["decision_score"])

print("\n========== FALSE NEGATIVE EXAMPLES ==========")

for _, row in false_real.head(5).iterrows():
    print("\nTITLE:", row["title"])
    print("ACTUAL: Fake")
    print("PREDICTED: Real")
    print("ARTICLE:", str(row["text"])[:500])

    if "decision_score" in row:
        print("DECISION SCORE:", row["decision_score"])

print("\nSaved error report:", OUTPUT_PATH)

print("\n========== ANALYSIS COMPLETED ==========")

