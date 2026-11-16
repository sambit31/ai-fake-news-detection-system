
import sys
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "ml"))

MODEL_PATH = BASE_DIR / "ml" / "artifacts" / "fake_news_pipeline.joblib"

model = joblib.load(MODEL_PATH)

tests = [
    {
        "name": "Short RBI statement",
        "text": "The Reserve Bank of India is India's central bank."
    },
    {
        "name": "Detailed RBI statement",
        "text": (
            "The Reserve Bank of India (RBI) is India's central bank. "
            "It is responsible for monetary policy, issuing currency, "
            "regulating banks, and maintaining financial stability. "
            "The RBI was established in 1935 under the Reserve Bank of India Act."
        )
    },
    {
        "name": "Short Constitution statement",
        "text": "India's Constitution came into effect on 26 January 1950."
    },
    {
        "name": "Detailed Constitution statement",
        "text": (
            "The Constitution of India came into effect on 26 January 1950. "
            "This date is celebrated every year as Republic Day. "
            "The Constitution establishes the framework of government, "
            "defines the powers of institutions, and protects citizens' rights."
        )
    }
]

print("\n========== TEXT LENGTH EXPERIMENT ==========")

for item in tests:
    prediction = int(model.predict([item["text"]])[0])
    score = float(model.decision_function([item["text"]])[0])

    print(f"\nTest: {item['name']}")
    print(f"Characters: {len(item['text'])}")
    print(f"Prediction: {'Real' if prediction == 1 else 'Fake'}")
    print(f"Decision score: {score:.6f}")

print("\n========== EXPERIMENT COMPLETED ==========")
