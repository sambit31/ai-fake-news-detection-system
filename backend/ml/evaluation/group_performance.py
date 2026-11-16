
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

PREDICTIONS_PATH = (
    BASE_DIR / "ml" / "artifacts" / "test_predictions.csv"
)


def evaluate_group(df, group_column):

    print(f"\n========== PERFORMANCE BY {group_column.upper()} ==========")

    results = []

    for group, subset in df.groupby(group_column, dropna=False):

        total = len(subset)

        correct = (
            subset["actual_label"] == subset["predicted_label"]
        ).sum()

        incorrect = total - correct

        accuracy = correct / total if total else 0

        fake_total = (subset["actual_label"] == 0).sum()

        fake_missed = (
            (subset["actual_label"] == 0)
            & (subset["predicted_label"] == 1)
        ).sum()

        real_total = (subset["actual_label"] == 1).sum()

        real_misclassified = (
            (subset["actual_label"] == 1)
            & (subset["predicted_label"] == 0)
        ).sum()

        fake_miss_rate = (
            fake_missed / fake_total if fake_total else None
        )

        real_misclassification_rate = (
            real_misclassified / real_total
            if real_total else None
        )

        results.append({
            group_column: group,
            "Total": total,
            "Correct": correct,
            "Errors": incorrect,
            "Accuracy": accuracy,
            "Fake_Articles": fake_total,
            "Fake_Miss_Rate": fake_miss_rate,
            "Real_Articles": real_total,
            "Real_Misclassification_Rate": real_misclassification_rate
        })

    result_df = pd.DataFrame(results)

    print(
        result_df.to_string(
            index=False,
            formatters={
                "Accuracy": lambda x: f"{x:.4%}",
                "Fake_Miss_Rate": lambda x: (
                    f"{x:.4%}" if pd.notna(x) else "N/A"
                ),
                "Real_Misclassification_Rate": lambda x: (
                    f"{x:.4%}" if pd.notna(x) else "N/A"
                )
            }
        )
    )

    return result_df


def main():

    print("\n========== GROUP PERFORMANCE ANALYSIS ==========")

    df = pd.read_csv(PREDICTIONS_PATH)

    required = [
        "actual_label",
        "predicted_label",
        "subject",
        "date",
        "text",
        "title"
    ]

    missing = [col for col in required if col not in df.columns]

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

    df["subject"] = df["subject"].fillna("Unknown")

    df["parsed_date"] = pd.to_datetime(
        df["date"],
        errors="coerce",
        format="mixed"
    )

    df["year"] = df["parsed_date"].dt.year

    # Overall accuracy
    overall_accuracy = (
        df["actual_label"] == df["predicted_label"]
    ).mean()

    print(f"\nOverall accuracy: {overall_accuracy:.4%}")

    # Subject performance
    subject_results = evaluate_group(df, "subject")

    # Year performance
    year_results = evaluate_group(df, "year")

    output_dir = BASE_DIR / "ml" / "artifacts"

    subject_results.to_csv(
        output_dir / "subject_performance.csv",
        index=False
    )

    year_results.to_csv(
        output_dir / "year_performance.csv",
        index=False
    )

    print("\nGenerated:")
    print("- subject_performance.csv")
    print("- year_performance.csv")

    print("\nGROUP PERFORMANCE ANALYSIS COMPLETED!")


if __name__ == "__main__":
    main()

