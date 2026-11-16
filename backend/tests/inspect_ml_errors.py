
import sys
import joblib
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "ml"))

MODEL_PATH = BASE_DIR / "ml" / "artifacts" / "fake_news_pipeline.joblib"
DATASET_PATH = BASE_DIR / "tests" / "dataset" / "test_articles.json"

model = joblib.load(MODEL_PATH)

with open(DATASET_PATH, "r", encoding="utf-8") as file:
    articles = json.load(file)

print("\n========== MISCLASSIFICATION INSPECTION ==========")

for article in articles:
    if article["id"] not in ["T01", "T03", "T05"]:
        continue

    text = article["text"]
    prediction = int(model.predict([text])[0])

    print(f"\nID: {article['id']}")
    print(f"Expected: {article['expected_ml']}")
    print(f"Predicted: {'Real' if prediction == 1 else 'Fake'}")

    if hasattr(model, "decision_function"):
        score = float(model.decision_function([text])[0])
        print(f"Decision score: {score:.6f}")

print("\n========== INSPECTION COMPLETED ==========")
