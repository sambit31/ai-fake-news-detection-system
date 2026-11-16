
import os
import sys
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "ml" / "artifacts" / "fake_news_pipeline.joblib"
OUTPUT_DIR = PROJECT_ROOT / "ml" / "artifacts"

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("\n========== FEATURE IMPORTANCE ANALYSIS ==========")

# Load trained pipeline
model = joblib.load(MODEL_PATH)

features = model.named_steps["features"]
classifier = model.named_steps["classifier"]

print("\nClassifier:", type(classifier).__name__)
print("Classes:", classifier.classes_)

# LinearSVC coefficients
if not hasattr(classifier, "coef_"):
    raise ValueError("The classifier does not support coefficient analysis.")

coefficients = classifier.coef_[0]

# Binary classification:
# Your project labels: 0 = Fake, 1 = Real
# Positive coefficient = Real
# Negative coefficient = Fake

print("\nTotal features:", len(coefficients))

# Extract feature names from each FeatureUnion transformer
all_results = []
offset = 0

for transformer_name, transformer in features.transformer_list:

    print(f"\nAnalyzing: {transformer_name}")

    vectorizer = transformer

    if not hasattr(vectorizer, "get_feature_names_out"):
        print("Skipping: feature names unavailable.")
        continue

    feature_names = vectorizer.get_feature_names_out()

    count = len(feature_names)

    current_coefficients = coefficients[offset:offset + count]

    if len(current_coefficients) != count:
        raise ValueError(
            f"Feature mismatch in {transformer_name}"
        )

    result = pd.DataFrame({
        "feature": feature_names,
        "coefficient": current_coefficients
    })

    result["absolute_importance"] = (
        result["coefficient"].abs()
    )

    result["influences"] = np.where(
        result["coefficient"] > 0,
        "REAL",
        "FAKE"
    )

    # Save all features for this transformer
    output_path = os.path.join(
        OUTPUT_DIR,
        f"feature_importance_{transformer_name}.csv"
    )

    result.sort_values(
        "absolute_importance",
        ascending=False
    ).to_csv(output_path, index=False)

    print("Saved:", output_path)

    print("\nTop 20 REAL-influencing features:")

    print(
        result.nlargest(20, "coefficient")[
            ["feature", "coefficient"]
        ].to_string(index=False)
    )

    print("\nTop 20 FAKE-influencing features:")

    print(
        result.nsmallest(20, "coefficient")[
            ["feature", "coefficient"]
        ].to_string(index=False)
    )

    all_results.append(result)
    offset += count

if offset != len(coefficients):
    raise ValueError(
        "Some classifier coefficients were not matched "
        "to the extracted features."
    )

print("\n========== ANALYSIS COMPLETED ==========")


