from pathlib import Path

import joblib
import pandas as pd

from app.models.mine import Mine
from .model import generate_features


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "artifacts" / "prospectivity_rf.joblib"


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Prospectivity model not found: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


def predict_prospectivity(mine: Mine) -> dict:
    artifact = load_model()

    model = artifact["model"]
    feature_names = artifact["features"]
    model_version = artifact["model_version"]

    features = generate_features(mine)
    feature_values = features.as_dict()

    X = pd.DataFrame(
        [
            {
                feature: feature_values[feature]
                for feature in feature_names
            }
        ]
    )

    prediction = model.predict(X)[0]

    probabilities = model.predict_proba(X)[0]

    class_probabilities = {
        class_name: round(float(probability) * 100, 2)
        for class_name, probability in zip(
            model.classes_,
            probabilities,
        )
    }

    prediction_confidence = class_probabilities[prediction]

    feature_importance = {
        feature: round(float(importance) * 100, 2)
        for feature, importance in zip(
            feature_names,
            model.feature_importances_,
        )
    }

    feature_importance = dict(
        sorted(
            feature_importance.items(),
            key=lambda item: item[1],
            reverse=True,
        )
    )

    class_score_map = {
        "LOW": 35.0,
        "MEDIUM": 62.5,
        "HIGH": 87.5,
    }

    base_score = class_score_map.get(
        prediction,
        50.0,
    )

    score = base_score + (
        prediction_confidence - 50
    ) * 0.20

    score = round(
        max(0.0, min(score, 100.0)),
        2,
    )

    return {
        "prospectivity_score": score,
        "classification": prediction,
        "confidence": round(
            prediction_confidence,
            2,
        ),
        "class_probabilities": class_probabilities,
        "features": feature_values,
        "feature_importance": feature_importance,
        "model_version": model_version,
    }