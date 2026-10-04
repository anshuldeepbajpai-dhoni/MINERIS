from app.models.mine import Mine

from .features import ProspectivityFeatures


MANGANESE_REGIONS = [
    "balaghat",
    "nagpur",
    "keonjhar",
    "odisha",
    "madhya pradesh",
    "maharashtra",
]


def generate_features(
    mine: Mine,
) -> ProspectivityFeatures:

    name = (mine.name or "").lower()
    location = (mine.location or "").lower()

    regional_match = any(
        region in name or region in location
        for region in MANGANESE_REGIONS
    )

    geological_score = 85.0 if regional_match else 60.0

    return ProspectivityFeatures(
        geological_score=geological_score,
        remote_sensing_score=72.0,
        structural_score=78.0,
        historical_score=80.0,
        elevation_score=68.0,
        drainage_score=65.0,
    )