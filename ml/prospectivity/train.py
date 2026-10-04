from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split


FEATURES = [
    "geological_score",
    "remote_sensing_score",
    "structural_score",
    "historical_score",
    "elevation_score",
    "drainage_score",
]

TARGET = "prospectivity_class"

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "prospectivity_training.csv"

MODEL_DIR = BASE_DIR / "artifacts"
MODEL_PATH = MODEL_DIR / "prospectivity_rf.joblib"


def train_model():
    # ---------------------------------------------------------
    # 1. Load dataset
    # ---------------------------------------------------------
    df = pd.read_csv(DATA_PATH)

    X = df[FEATURES]
    y = df[TARGET]

    # ---------------------------------------------------------
    # 2. Train/test split
    # ---------------------------------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    # ---------------------------------------------------------
    # 3. Random Forest
    # ---------------------------------------------------------
    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    # ---------------------------------------------------------
    # 4. Predictions
    # ---------------------------------------------------------
    predictions = model.predict(X_test)

    # ---------------------------------------------------------
    # 5. Evaluation
    # ---------------------------------------------------------
    accuracy = accuracy_score(y_test, predictions)

    print("\n" + "=" * 60)
    print("MINERIS — PROSPECTIVITY RANDOM FOREST")
    print("=" * 60)

    print(f"\nTraining samples : {len(X_train)}")
    print(f"Testing samples  : {len(X_test)}")
    print(f"Accuracy         : {accuracy:.4f}")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            digits=4,
        )
    )

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, predictions))

    # ---------------------------------------------------------
    # 6. Feature importance
    # ---------------------------------------------------------
    importance = pd.DataFrame(
        {
            "feature": FEATURES,
            "importance": model.feature_importances_,
        }
    ).sort_values(
        "importance",
        ascending=False,
    )

    print("\nFeature Importance:")
    print(importance.to_string(index=False))

    # ---------------------------------------------------------
    # 7. Save model
    # ---------------------------------------------------------
    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    artifact = {
        "model": model,
        "features": FEATURES,
        "target": TARGET,
        "model_version": "random-forest-v1",
    }

    joblib.dump(
        artifact,
        MODEL_PATH,
    )

    print(f"\nModel saved to:")
    print(MODEL_PATH)

    return model


if __name__ == "__main__":
    train_model()