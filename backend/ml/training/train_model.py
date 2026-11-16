
import re
import html
import joblib
import pandas as pd

from pathlib import Path
import sys

ML_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ML_DIR))

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC

from text_preprocessing import clean_text

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


# ============================================================
# 1. PROJECT PATHS AND SETTINGS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cleaned_dataset.csv"
)

ARTIFACT_DIR = PROJECT_ROOT / "ml" / "artifacts"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42
TEST_SIZE = 0.20

# Label definitions:
# 0 = Fake
# 1 = Real


# ============================================================
# 2. LOAD CLEANED DATASET
# ============================================================

def load_dataset():

    if not DATA_PATH.is_file():
        raise FileNotFoundError(
            f"Cleaned dataset not found: {DATA_PATH}"
        )

    print("Loading cleaned dataset:", DATA_PATH)

    data = pd.read_csv(DATA_PATH)

    data.columns = (
        data.columns.str.strip().str.lower()
    )

    required_columns = ["title", "text", "label"]

    for column in required_columns:
        if column not in data.columns:
            raise ValueError(
                f"Required column missing: {column}"
            )

    return data


data = load_dataset()


# ============================================================
# 3. VALIDATE DATASET
# ============================================================

print("\n========== DATASET VALIDATION ==========")

print("Dataset shape:", data.shape)

print("\nColumns:")
print(data.columns.tolist())

print("\nMissing values:")
print(data[["title", "text", "label"]].isnull().sum())

if data[["title", "text", "label"]].isnull().any().any():
    raise ValueError(
        "Missing values found in required training columns."
    )

data["label"] = pd.to_numeric(
    data["label"],
    errors="raise"
).astype("int64")

if not set(data["label"].unique()).issubset({0, 1}):
    raise ValueError(
        "Labels must contain only 0 (Fake) and 1 (Real)."
    )

if set(data["label"].unique()) != {0, 1}:
    raise ValueError(
        "Both Fake and Real classes must be present."
    )

print("\nClass distribution:")
print(
    data["label"].value_counts().sort_index().rename(
        index={0: "Fake", 1: "Real"}
    )
)


# ============================================================
# 4. PREPARE ARTICLE TEXT
# ============================================================

data["title"] = data["title"].fillna("").astype(str)
data["text"] = data["text"].fillna("").astype(str)

data["article"] = (
    data["title"] + " " + data["text"]
).str.strip()

data = data[
    data["article"].str.len() > 0
].copy()

if data.empty:
    raise ValueError("No usable articles found.")

print("\nUsable articles:", len(data))


# ============================================================
# 5. TEXT PREPROCESSING
# ============================================================


# ============================================================
# 6. TRAIN-TEST SPLIT
# ============================================================

X = data["article"].to_numpy(dtype=object)
y = data["label"].to_numpy(dtype="int64")

# Keep original row positions for error analysis.
row_indices = data.index.to_numpy()

(
    X_train,
    X_test,
    y_train,
    y_test,
    train_indices,
    test_indices
) = train_test_split(
    X,
    y,
    row_indices,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=y
)

print("\n========== DATA SPLIT ==========")

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

print(
    "Training class distribution:",
    pd.Series(y_train).value_counts().to_dict()
)

print(
    "Testing class distribution:",
    pd.Series(y_test).value_counts().to_dict()
)


# ============================================================
# 7. CREATE WORD + CHARACTER TF-IDF FEATURES
# ============================================================

def create_features():

    return FeatureUnion([

        (
            "word_tfidf",

            TfidfVectorizer(
                preprocessor=clean_text,
                lowercase=False,
                analyzer="word",
                ngram_range=(1, 2),
                max_features=80000,
                min_df=2,
                max_df=0.95,
                sublinear_tf=True
            )
        ),

        (
            "char_tfidf",

            TfidfVectorizer(
                preprocessor=clean_text,
                lowercase=False,
                analyzer="char_wb",
                ngram_range=(3, 5),
                max_features=50000,
                min_df=2,
                sublinear_tf=True
            )
        )

    ])


# ============================================================
# 8. DEFINE CLASSIFIERS
# ============================================================

models = {

    "Logistic Regression": LogisticRegression(
        max_iter=2000,
        random_state=RANDOM_STATE
    ),

    "Multinomial Naive Bayes": MultinomialNB(
        alpha=0.1
    ),

    "Linear SVM": LinearSVC(
        max_iter=5000,
        random_state=RANDOM_STATE
    )

}


# ============================================================
# 9. TRAIN AND EVALUATE MODELS
# ============================================================

results = []
trained_models = {}
model_predictions = {}

for model_name, classifier in models.items():

    print("\n" + "=" * 65)
    print("TRAINING:", model_name)
    print("=" * 65)

    # Create a fresh feature extractor for every model.
    pipeline = Pipeline([

        ("features", create_features()),

        ("classifier", classifier)

    ])

    pipeline.fit(
        X_train,
        y_train
    )

    predictions = pipeline.predict(X_test)

    model_predictions[model_name] = predictions
    trained_models[model_name] = pipeline

    # Evaluation metrics.
    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        average="macro",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        average="macro",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        average="macro",
        zero_division=0
    )

    results.append({

        "Model": model_name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1-Score": f1

    })

    print(f"\nAccuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")

    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            predictions,
            labels=[0, 1],
            target_names=["Fake", "Real"],
            zero_division=0
        )
    )

    print("Confusion Matrix:")

    print(
        confusion_matrix(
            y_test,
            predictions,
            labels=[0, 1]
        )
    )


# ============================================================
# 10. MODEL COMPARISON
# ============================================================

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by=["F1-Score", "Accuracy"],
    ascending=False
).reset_index(drop=True)

print("\n========== MODEL COMPARISON ==========")

print(
    results_df.to_string(index=False)
)

comparison_path = (
    ARTIFACT_DIR / "model_comparison.csv"
)

results_df.to_csv(
    comparison_path,
    index=False
)


# ============================================================
# 11. SELECT BEST MODEL
# ============================================================

best_model_name = results_df.iloc[0]["Model"]

best_model = trained_models[best_model_name]

best_predictions = model_predictions[best_model_name]

model_path = (
    ARTIFACT_DIR / "fake_news_pipeline.joblib"
)

joblib.dump(
    best_model,
    model_path
)


# ============================================================
# 12. SAVE TEST PREDICTIONS FOR ERROR ANALYSIS
# ============================================================

test_data = data.loc[test_indices].copy()

test_data["actual_label"] = y_test
test_data["predicted_label"] = best_predictions

test_data["actual_class"] = (
    test_data["actual_label"]
    .map({0: "Fake", 1: "Real"})
)

test_data["predicted_class"] = (
    test_data["predicted_label"]
    .map({0: "Fake", 1: "Real"})
)

test_data["correct_prediction"] = (
    test_data["actual_label"]
    == test_data["predicted_label"]
)

error_path = (
    ARTIFACT_DIR / "test_predictions.csv"
)

test_data.to_csv(
    error_path,
    index=False
)


# ============================================================
# 13. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 65)
print("PHASE 1 - TRAINING SUMMARY")
print("=" * 65)

print("Best model:", best_model_name)

print("Model saved:", model_path)

print("Comparison saved:", comparison_path)

print("Test predictions saved:", error_path)

print("\nFinal test confusion matrix:")

print(
    confusion_matrix(
        y_test,
        best_predictions,
        labels=[0, 1]
    )
)

print("\nTRAINING COMPLETED SUCCESSFULLY!")

