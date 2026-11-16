
import json
import sys
from pathlib import Path

import joblib
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "ml" / "artifacts" / "fake_news_pipeline.joblib"
DATASET_PATH = BASE_DIR / "tests" / "dataset" / "test_articles.json"
OUTPUT_PATH = BASE_DIR / "ml" / "artifacts" / "fixed_test_predictions.csv"

# Allow the saved pipeline's preprocessing function to be imported.
sys.path.insert(0, str(BASE_DIR / "ml"))


def main():
    print("\n========== ML EVALUATION ==========")

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATASET_PATH}")

    # Load model
    model = joblib.load(MODEL_PATH)

    print("Model loaded:", type(model).__name__)
    print("Classifier:", type(model.named_steps["classifier"]).__name__)
    print("Model classes:", model.classes_)

    # Load dataset
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        articles = json.load(file)

    print("\nTotal articles:", len(articles))

    # Only evaluate articles with binary ground-truth labels.
    # Mixed and ambiguous articles are retained for separate analysis.
    eligible = [
        article for article in articles
        if article["expected_ml"] in ("Fake", "Real")
    ]

    excluded = [
        article for article in articles
        if article["expected_ml"] not in ("Fake", "Real")
    ]

    print("Binary evaluation articles:", len(eligible))
    print("Excluded for binary accuracy:", len(excluded))

    if not eligible:
        raise ValueError("No articles have valid binary evaluation labels.")

    label_map = {"Fake": 0, "Real": 1}

    y_true = [label_map[item["expected_ml"]] for item in eligible]
    texts = [item["text"] for item in eligible]

    # Predict using the existing model.
    predictions = model.predict(texts)

    # Convert numeric predictions to readable labels.
    readable_predictions = [
        "Real" if prediction == 1 else "Fake"
        for prediction in predictions
    ]

    print("\n========== PREDICTION RESULTS ==========")

    correct = 0
    results = []

    for article, actual, predicted in zip(
        eligible, [item["expected_ml"] for item in eligible],
        readable_predictions
    ):
        is_correct = actual == predicted
        correct += int(is_correct)

        print(
            f'{article["id"]}: Expected={actual}, '
            f'Predicted={predicted}, Correct={is_correct}'
        )

        results.append({
            "id": article["id"],
            "category": article["category"],
            "expected": actual,
            "predicted": predicted,
            "correct": is_correct,
        })

    # Metrics
    accuracy = accuracy_score(y_true, predictions)
    precision = precision_score(
        y_true, predictions, average="binary",
        pos_label=1, zero_division=0
    )
    recall = recall_score(
        y_true, predictions, average="binary",
        pos_label=1, zero_division=0
    )
    f1 = f1_score(
        y_true, predictions, average="binary",
        pos_label=1, zero_division=0
    )

    print("\n========== METRICS ==========")
    print(f"Correct predictions: {correct}/{len(eligible)}")
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision (Real): {precision:.4f}")
    print(f"Recall (Real):    {recall:.4f}")
    print(f"F1-score (Real):  {f1:.4f}")

    print("\nClassification report:")
    print(
        classification_report(
            y_true,
            predictions,
            labels=[0, 1],
            target_names=["Fake", "Real"],
            zero_division=0
        )
    )

    print("Confusion matrix (rows=actual, columns=predicted):")
    print(confusion_matrix(y_true, predictions, labels=[0, 1]))

    # Save predictions
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    import csv

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["id", "category", "expected", "predicted", "correct"]
        )
        writer.writeheader()
        writer.writerows(results)

    print("\nPredictions saved to:", OUTPUT_PATH)
    print("\nML EVALUATION COMPLETED!")


if __name__ == "__main__":
    main()
