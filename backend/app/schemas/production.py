from pydantic import BaseModel


class ProductionHistory(BaseModel):
    year: int
    planned_production: float
    actual_production: float
    demand: float


class ProductionResponse(BaseModel):
    mine_id: int
    historical_production: list[ProductionHistory]

    forecast_production: float
    forecast_demand: float

    shortfall: float
    shortfall_percentage: float

    production_achievement: float
    risk_level: str