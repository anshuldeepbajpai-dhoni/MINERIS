from .features import ProspectivityFeatures


WEIGHTS = {
    "geological_score": 0.30,
    "remote_sensing_score": 0.25,
    "structural_score": 0.20,
    "historical_score": 0.15,
    "elevation_score": 0.05,
    "drainage_score": 0.05,
}


def calculate_prospectivity_score(
    features: ProspectivityFeatures,
) -> float:

    values = features.as_dict()

    score = sum(
        values[name] * weight
        for name, weight in WEIGHTS.items()
    )

    return round(
        max(0.0, min(score, 100.0)),
        2,
    )


def classify_prospectivity(
    score: float,
) -> str:

    if score >= 75:
        return "HIGH"

    if score >= 50:
        return "MEDIUM"

    return "LOW"