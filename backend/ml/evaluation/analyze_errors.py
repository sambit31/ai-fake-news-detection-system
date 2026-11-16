
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

PREDICTIONS_PATH = (
    BASE_DIR / "ml" / "artifacts" / "test_predictions.csv"
)

OUTPUT_PATH = (
    BASE_DIR / "ml" / "artifacts" / "error_analysis_by_group.csv"
)


def main():

    print("\n========== DETAILED ERROR ANALYSIS ==========\n")

    df = pd.read_csv(PREDICTIONS_PATH)

    required = [
        "title", "text", "subject", "date",
        "actual_label", "predicted_label"
    ]

    missing = [column for column in required if column not in df.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df["actual_label"] = pd.to_numeric(
        df["actual_label"], errors="coerce"
    )

    df["predicted_label"] = pd.to_numeric(
        df["predicted_label"], errors="coerce"
    )

    df = df.dropna(
        subset=["actual_label", "predicted_label"]
    ).copy()

    df["actual_label"] = df["actual_label"].astype(int)
    df["predicted_label"] = df["predicted_label"].astype(int)

    # 0 = Fake, 1 = Real
    errors = df[
        df["actual_label"] != df["predicted_label"]
    ].copy()

    errors["error_type"] = errors.apply(
        lambda row:
        "Fake classified as Real"
        if row["actual_label"] == 0
        else "Real classified as Fake",
        axis=1
    )

    errors["subject"] = errors["subject"].fillna("Unknown")

    errors["article_length"] = (
        errors["title"].fillna("").astype(str).str.len()
        + errors["text"].fillna("").astype(str).str.len()
    )

    errors["parsed_date"] = pd.to_datetime(
        errors["date"],
        errors="coerce",
        format="mixed"
    )

    errors["year"] = errors["parsed_date"].dt.year

    print("Total test articles:", len(df))
    print("Total errors:", len(errors))

    print("\n========== ERROR TYPE COUNTS ==========")

    print(errors["error_type"].value_counts())

    print("\n========== ERRORS BY SUBJECT ==========")

    print(
        errors.groupby(
            ["error_type", "subject"],
            dropna=False
        ).size().to_string()
    )

    print("\n========== ERRORS BY YEAR ==========")

    print(
        errors.groupby(
            ["error_type", "year"],
            dropna=False
        ).size().to_string()
    )

    print("\n========== ARTICLE LENGTH ==========")

    if not errors.empty:
        print(
            errors.groupby("error_type")["article_length"]
            .agg(["count", "mean", "median", "min", "max"])
            .round(2)
        )

    print("\n========== ERROR EXAMPLES ==========")

    for _, row in errors.iterrows():

        print("\n----------------------------------------")
        print("Error:", row["error_type"])
        print("Subject:", row["subject"])
        print("Date:", row["date"])
        print("Title:", str(row["title"])[:200])
        print("Article length:", row["article_length"])
        print("----------------------------------------")

    # Save grouped error details.
    if not errors.empty:

        summary = (
            errors.groupby(
                ["error_type", "subject", "year"],
                dropna=False
            )
            .agg(
                error_count=("title", "count"),
                average_article_length=("article_length", "mean")
            )
            .reset_index()
        )

        summary.to_csv(OUTPUT_PATH, index=False)

    print("\nSaved detailed error analysis:")
    print(OUTPUT_PATH)

    print("\nERROR ANALYSIS COMPLETED!")


if __name__ == "__main__":
    main()

