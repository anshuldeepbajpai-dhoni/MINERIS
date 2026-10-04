from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProspectivityResponse(BaseModel):
    id: int
    mine_id: int
    prospectivity_score: float
    classification: str

    geological_score: float
    remote_sensing_score: float
    structural_score: float
    historical_score: float

    confidence: float | None = None
    class_probabilities: dict[str, float] | None = None
    feature_importance: dict[str, float] | None = None

    explanation: str
    model_version: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)