
import pandas as pd
import joblib

from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    balanced_accuracy_score,
    matthews_corrcoef
)

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = BASE_DIR / "data" / "external" / "welFake_cleaned.csv"

MODEL_PATH = BASE_DIR / "ml" / "artifacts" / "fake_news_pipeline.joblib"

OUTPUT_PATH = BASE_DIR / "ml" / "artifacts" / "external_predictions.csv"


print("\n========== EXTERNAL MODEL EVALUATION ==========\n")

# 1. Load external dataset
df = pd.read_csv(DATA_PATH)

print("External dataset size:", len(df))

# 2. Load previously trained model
model = joblib.load(MODEL_PATH)

print("Model loaded:", type(model).__name__)

# 3. Prepare input and labels
X = df["article"].fillna("").astype(str)
y_true = df["label"].astype(int)

# 4. Generate predictions (NO RETRAINING)
y_pred = model.predict(X)

# 5. Calculate evaluation metrics
accuracy = accuracy_score(y_true, y_pred)

precision = precision_score(
    y_true, y_pred, average="macro", zero_division=0
)

recall = recall_score(
    y_true, y_pred, average="macro", zero_division=0
)

f1 = f1_score(
    y_true, y_pred, average="macro", zero_division=0
)

balanced_acc = balanced_accuracy_score(y_true, y_pred)

mcc = matthews_corrcoef(y_true, y_pred)

# 6. Print results
print("\n========== EXTERNAL TEST METRICS ==========\n")

print(f"Accuracy:          {accuracy:.4f} ({accuracy * 100:.2f}%)")
print(f"Macro Precision:   {precision:.4f}")
print(f"Macro Recall:      {recall:.4f}")
print(f"Macro F1 Score:    {f1:.4f}")
print(f"Balanced Accuracy: {balanced_acc:.4f}")
print(f"Matthews Corrcoef: {mcc:.4f}")

# 7. Confusion matrix
cm = confusion_matrix(y_true, y_pred, labels=[0, 1])

print("\n========== CONFUSION MATRIX ==========")
print("Labels: 0 = Fake, 1 = Real")
print(cm)

# 8. Classification report
print("\n========== CLASSIFICATION REPORT ==========\n")

print(
    classification_report(
        y_true,
        y_pred,
        labels=[0, 1],
        target_names=["Fake", "Real"],
        zero_division=0
    )
)

# 9. Save predictions for error analysis
results = df[["title", "label"]].copy()

results["predicted_label"] = y_pred
results["correct"] = (
    results["label"] == results["predicted_label"]
)

# Decision scores are NOT calibrated probabilities.
if hasattr(model, "decision_function"):
    results["decision_score"] = model.decision_function(X)

results.to_csv(OUTPUT_PATH, index=False)

print("\n========== PREDICTION SUMMARY ==========")
print("Correct predictions:", results["correct"].sum())
print("Incorrect predictions:", (~results["correct"]).sum())

print("\nPredictions saved to:")
print(OUTPUT_PATH)

print("\n========== EVALUATION COMPLETED ==========")

