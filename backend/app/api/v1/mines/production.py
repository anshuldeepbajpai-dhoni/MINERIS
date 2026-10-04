from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.dependencies import get_db
from app.models.mine import Mine
from app.models.production import ProductionRecord
from app.models.user import User
from app.schemas.production import ProductionResponse


router = APIRouter(
    tags=["Production"],
)


def calculate_forecast(values: list[float]) -> float:
    """
    Simple linear trend forecast.

    Uses the average year-to-year change
    from historical production.
    """

    if not values:
        return 0.0

    if len(values) == 1:
        return values[-1]

    changes = [
        values[i] - values[i - 1]
        for i in range(1, len(values))
    ]

    average_change = sum(changes) / len(changes)

    forecast = values[-1] + average_change

    return round(max(forecast, 0), 2)


def calculate_risk(shortfall_percentage: float) -> str:
    if shortfall_percentage <= 5:
        return "LOW"

    if shortfall_percentage <= 10:
        return "MEDIUM"

    return "HIGH"


@router.get(
    "/{mine_id}/production",
    response_model=ProductionResponse,
)
def get_production_analysis(
    mine_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # --------------------------------------------------
    # Verify mine
    # --------------------------------------------------

    mine = db.get(Mine, mine_id)

    if mine is None:
        raise HTTPException(
            status_code=404,
            detail="Mine not found",
        )

    # --------------------------------------------------
    # Get historical production
    # --------------------------------------------------

    records = db.scalars(
        select(ProductionRecord)
        .where(
            ProductionRecord.mine_id == mine_id
        )
        .order_by(
            ProductionRecord.year
        )
    ).all()

    if not records:
        raise HTTPException(
            status_code=404,
            detail="No production data found for this mine",
        )

    # --------------------------------------------------
    # Historical response
    # --------------------------------------------------

    history = [
        {
            "year": record.year,
            "planned_production": record.planned_production,
            "actual_production": record.actual_production,
            "demand": record.demand,
        }
        for record in records
    ]

    # --------------------------------------------------
    # Production forecast
    # --------------------------------------------------

    actual_values = [
        record.actual_production
        for record in records
    ]

    demand_values = [
        record.demand
        for record in records
    ]

    forecast_production = calculate_forecast(
        actual_values
    )

    forecast_demand = calculate_forecast(
        demand_values
    )

    # --------------------------------------------------
    # Shortfall
    # --------------------------------------------------

    shortfall = max(
        forecast_demand - forecast_production,
        0,
    )

    if forecast_demand > 0:
        shortfall_percentage = (
            shortfall / forecast_demand
        ) * 100
    else:
        shortfall_percentage = 0

    # --------------------------------------------------
    # Production achievement
    # --------------------------------------------------

    total_planned = sum(
        record.planned_production
        for record in records
    )

    total_actual = sum(
        record.actual_production
        for record in records
    )

    if total_planned > 0:
        production_achievement = (
            total_actual / total_planned
        ) * 100
    else:
        production_achievement = 0

    # --------------------------------------------------
    # Risk
    # --------------------------------------------------

    risk_level = calculate_risk(
        shortfall_percentage
    )

    return {
        "mine_id": mine_id,
        "historical_production": history,
        "forecast_production": forecast_production,
        "forecast_demand": forecast_demand,
        "shortfall": round(shortfall, 2),
        "shortfall_percentage": round(
            shortfall_percentage,
            2,
        ),
        "production_achievement": round(
            production_achievement,
            2,
        ),
        "risk_level": risk_level,
    }