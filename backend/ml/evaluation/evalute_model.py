
import sys
from pathlib import Path

import joblib
import pandas as pd

from sklearn.base import clone
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate


# --------------------------------------------------
# PATHS AND IMPORTS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]
ML_DIR = BASE_DIR / "ml"
DATA_PATH = BASE_DIR / "data" / "processed" / "cleaned_dataset.csv"
MODEL_PATH = ML_DIR / "artifacts" / "fake_news_pipeline.joblib"
PREDICTIONS_PATH = ML_DIR / "artifacts" / "test_predictions.csv"

OUTPUT_DIR = ML_DIR / "artifacts"
ERRORS_PATH = OUTPUT_DIR / "misclassified_articles.csv"

# Make the custom preprocessing module available to Joblib.
sys.path.insert(0, str(ML_DIR))
from text_preprocessing import clean_text  # noqa: E402


def main():

    print("\n========== MODEL EVALUATION ==========\n")

    # --------------------------------------------------
    # 1. LOAD DATASET
    # --------------------------------------------------

    print("Loading cleaned dataset...")

    data = pd.read_csv(DATA_PATH)

    required_columns = {"title", "text", "label"}

    if not required_columns.issubset(data.columns):
        raise ValueError(
            f"Dataset must contain: {required_columns}"
        )

    data = data.dropna(subset=["title", "text", "label"]).copy()

    data["article"] = (
        data["title"].astype(str)
        + " "
        + data["text"].astype(str)
    )

    X = data["article"]
    y = data["label"].astype(int)

    print("Dataset shape:", data.shape)
    print("Class distribution:")
    print(y.value_counts().sort_index())

    # --------------------------------------------------
    # 2. RECREATE ORIGINAL TRAIN/TEST SPLIT
    # --------------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    print("\nTraining samples:", len(X_train))
    print("Testing samples:", len(X_test))

    # --------------------------------------------------
    # 3. LOAD SAVED MODEL
    # --------------------------------------------------

    print("\nLoading saved model...")

    saved_model = joblib.load(MODEL_PATH)

    print("Loaded:", type(saved_model).__name__)

    # clone() removes learned parameters but preserves
    # the pipeline structure and hyperparameters.
    model = clone(saved_model)

    # --------------------------------------------------
    # 4. STRATIFIED 5-FOLD CROSS-VALIDATION
    # --------------------------------------------------

    print("\n========== 5-FOLD CROSS-VALIDATION ==========")

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )

    scoring = {
        "accuracy": "accuracy",
        "precision": "precision_macro",
        "recall": "recall_macro",
        "f1": "f1_macro"
    }

    results = cross_validate(
        model,
        X_train,
        y_train,
        cv=cv,
        scoring=scoring,
        n_jobs=1,
        return_train_score=False
    )

    metrics = [
        "accuracy",
        "precision",
        "recall",
        "f1"
    ]

    print("\nIndividual fold results:")

    for metric in metrics:
        values = results[f"test_{metric}"]

        print(f"\n{metric.upper()}:")

        for fold_number, value in enumerate(values, start=1):
            print(f"Fold {fold_number}: {value:.4f}")

        print(f"Mean: {values.mean():.4f}")
        print(f"Standard deviation: {values.std():.4f}")

    # Save cross-validation results.
    cv_results = pd.DataFrame({
        "Fold": range(1, 6),
        "Accuracy": results["test_accuracy"],
        "Precision": results["test_precision"],
        "Recall": results["test_recall"],
        "F1_Score": results["test_f1"]
    })

    cv_results.to_csv(
        OUTPUT_DIR / "cross_validation_results.csv",
        index=False
    )

    # --------------------------------------------------
    # 5. ERROR ANALYSIS ON ORIGINAL TEST SET
    # --------------------------------------------------

    print("\n========== ERROR ANALYSIS ==========")

    if not PREDICTIONS_PATH.exists():
        raise FileNotFoundError(
            f"Prediction file not found: {PREDICTIONS_PATH}"
        )

    predictions = pd.read_csv(PREDICTIONS_PATH)

    print("\nPrediction file columns:")
    print(predictions.columns.tolist())

    actual_candidates = [
        "actual_label", "y_true", "true_label", "label"
    ]

    predicted_candidates = [
        "predicted_label", "y_pred", "prediction"
    ]

    actual_col = next(
        (c for c in actual_candidates if c in predictions.columns),
        None
    )

    predicted_col = next(
        (c for c in predicted_candidates if c in predictions.columns),
        None
    )

    if actual_col is None or predicted_col is None:
        raise ValueError(
            "Could not identify actual/predicted label columns. "
            "Check the printed column names and update the script."
        )

    predictions[actual_col] = pd.to_numeric(
        predictions[actual_col], errors="coerce"
    )

    predictions[predicted_col] = pd.to_numeric(
        predictions[predicted_col], errors="coerce"
    )

    predictions = predictions.dropna(
        subset=[actual_col, predicted_col]
    ).copy()

    predictions["actual"] = predictions[actual_col].astype(int)
    predictions["predicted"] = predictions[predicted_col].astype(int)

    # 0 = Fake, 1 = Real
    false_positives = predictions[
        (predictions["actual"] == 0)
        & (predictions["predicted"] == 1)
    ].copy()

    false_negatives = predictions[
        (predictions["actual"] == 1)
        & (predictions["predicted"] == 0)
    ].copy()

    print("\nFalse Positives:")
    print("Fake articles classified as Real:", len(false_positives))

    print("\nFalse Negatives:")
    print("Real articles classified as Fake:", len(false_negatives))

    errors = pd.concat(
        [false_positives, false_negatives],
        ignore_index=True
    )

    errors["error_type"] = errors.apply(
        lambda row: (
            "Fake classified as Real"
            if row["actual"] == 0
            else "Real classified as Fake"
        ),
        axis=1
    )

    errors.to_csv(ERRORS_PATH, index=False)

    print("\nMisclassified articles saved to:")
    print(ERRORS_PATH)

    # --------------------------------------------------
    # 6. DISPLAY SAMPLE ERRORS
    # --------------------------------------------------

    print("\n========== SAMPLE MISCLASSIFICATIONS ==========")

    for _, row in errors.head(10).iterrows():

        title = str(row.get("title", "No title"))
        article_text = str(row.get("text", ""))

        print("\n----------------------------------------")
        print("Error type:", row["error_type"])
        print("Title:", title[:250])
        print("Article:", article_text[:400].replace("\n", " "))
        print("----------------------------------------")

    print("\n========== EVALUATION COMPLETED ==========")

    print("\nGenerated files:")
    print("- cross_validation_results.csv")
    print("- misclassified_articles.csv")


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    main()

