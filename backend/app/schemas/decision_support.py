from pydantic import BaseModel


class DecisionSupportResponse(BaseModel):
    mine_id: int
    mine_name: str

    prospectivity_score: float
    prospectivity_classification: str

    production_available: bool

    forecast_production: float | None = None
    forecast_demand: float | None = None

    shortfall: float
    shortfall_percentage: float

    production_risk: str
    decision_priority: str

    recommendations: list[str]

    model_version: str