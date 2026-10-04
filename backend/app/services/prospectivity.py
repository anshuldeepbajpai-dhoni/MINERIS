from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.mine import Mine
from app.models.prospectivity import ProspectivityResult

from ml.prospectivity.predictor import predict_prospectivity


MODEL_VERSION = "random-forest-v1"


def calculate_prospectivity(mine: Mine) -> dict:
    """
    Generate prospectivity using the trained Random Forest model.
    """

    prediction = predict_prospectivity(mine)

    features = prediction["features"]

    explanation = (
        f"The {mine.name} zone received a "
        f"{prediction['classification'].lower()} prospectivity "
        f"classification with a score of "
        f"{prediction['prospectivity_score']}/100. "
        f"The Random Forest model estimated a "
        f"{prediction['confidence']}% confidence for the predicted "
        f"classification using geological, remote-sensing, structural, "
        f"historical, elevation, and drainage features."
    )

    return {
        "prospectivity_score": prediction["prospectivity_score"],
        "classification": prediction["classification"],

        "geological_score": round(
            features["geological_score"], 2
        ),
        "remote_sensing_score": round(
            features["remote_sensing_score"], 2
        ),
        "structural_score": round(
            features["structural_score"], 2
        ),
        "historical_score": round(
            features["historical_score"], 2
        ),

        "confidence": prediction["confidence"],
        "class_probabilities": prediction["class_probabilities"],
        "feature_importance": prediction["feature_importance"],

        "explanation": explanation,
        "model_version": MODEL_VERSION,
    }


def get_or_create_prospectivity(
    db: Session,
    mine: Mine,
) -> ProspectivityResult:

    existing = db.scalar(
        select(ProspectivityResult)
        .where(
            ProspectivityResult.mine_id == mine.id,
            ProspectivityResult.model_version == MODEL_VERSION,
        )
        .order_by(ProspectivityResult.id.desc())
    )

    if existing:
        return existing

    result_data = calculate_prospectivity(mine)

    result = ProspectivityResult(
        mine_id=mine.id,
        **result_data,
    )

    db.add(result)
    db.commit()
    db.refresh(result)

    return result