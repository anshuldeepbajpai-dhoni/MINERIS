from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.mine import Mine
from app.models.production import ProductionRecord
from app.services.prospectivity import (
    calculate_prospectivity,
)


def calculate_forecast(values: list[float]) -> float:
    """
    Baseline trend forecast using average
    year-to-year change.
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


def generate_recommendations(
    prospectivity_score: float,
    prospectivity_classification: str,
    risk_level: str,
    shortfall: float,
    shortfall_percentage: float,
) -> list[str]:

    recommendations: list[str] = []

    # -----------------------------------------
    # Prospectivity-driven recommendation
    # -----------------------------------------

    if prospectivity_classification == "HIGH":
        recommendations.append(
            "Prioritize exploration activities in this "
            "high-potential mineral zone."
        )

    elif prospectivity_classification == "MEDIUM":
        recommendations.append(
            "Conduct targeted exploration and collect "
            "additional geological evidence before expansion."
        )

    else:
        recommendations.append(
            "Maintain lower exploration priority and "
            "focus resources on higher-potential zones."
        )

    # -----------------------------------------
    # Production risk
    # -----------------------------------------

    if risk_level == "HIGH":
        recommendations.append(
            f"Immediate production intervention is recommended "
            f"to address the projected {shortfall:,.0f} t demand gap."
        )

    elif risk_level == "MEDIUM":
        recommendations.append(
            f"Review production capacity and operational efficiency "
            f"to reduce the projected {shortfall:,.0f} t demand gap."
        )

    else:
        recommendations.append(
            "Current production capacity is broadly aligned "
            "with projected demand."
        )

    # -----------------------------------------
    # Demand monitoring
    # -----------------------------------------

    if shortfall_percentage > 0:
        recommendations.append(
            "Monitor demand growth and production performance "
            "through periodic forecast updates."
        )

    # -----------------------------------------
    # Data confidence
    # -----------------------------------------

    recommendations.append(
        "Integrate satellite-derived spectral features, "
        "structural lineaments, and verified geological data "
        "to improve prospectivity confidence."
    )

    return recommendations


def generate_decision_support(
    db: Session,
    mine: Mine,
) -> dict:

    # =========================================
    # 1. Prospectivity
    # =========================================

    prospectivity = calculate_prospectivity(mine)

    # =========================================
    # 2. Production history
    # =========================================

    records = db.scalars(
        select(ProductionRecord)
        .where(
            ProductionRecord.mine_id == mine.id
        )
        .order_by(
            ProductionRecord.year
        )
    ).all()

    if not records:
        return {
            "mine_id": mine.id,
            "mine_name": mine.name,
            "prospectivity_score": prospectivity[
                "prospectivity_score"
            ],
            "prospectivity_classification": prospectivity[
                "classification"
            ],
            "production_available": False,
            "production_risk": "UNKNOWN",
            "shortfall": 0,
            "shortfall_percentage": 0,
            "decision_priority": (
                "HIGH"
                if prospectivity["classification"] == "HIGH"
                else "MEDIUM"
            ),
            "recommendations": [
                "Prioritize exploration according to "
                "prospectivity classification.",
                "Production forecast unavailable because "
                "historical production data is missing.",
                "Collect production data before making "
                "capacity decisions.",
                "Integrate real geospatial features to "
                "improve prospectivity confidence.",
            ],
        }

    # =========================================
    # 3. Production forecast
    # =========================================

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

    # =========================================
    # 4. Shortfall
    # =========================================

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

    shortfall_percentage = round(
        shortfall_percentage,
        2,
    )

    # =========================================
    # 5. Production risk
    # =========================================

    risk_level = calculate_risk(
        shortfall_percentage
    )

    # =========================================
    # 6. Decision priority
    # =========================================

    prospectivity_classification = prospectivity[
        "classification"
    ]

    if (
        prospectivity_classification == "HIGH"
        and risk_level in ("HIGH", "MEDIUM")
    ):
        decision_priority = "CRITICAL"

    elif prospectivity_classification == "HIGH":
        decision_priority = "HIGH"

    elif risk_level == "HIGH":
        decision_priority = "HIGH"

    elif (
        prospectivity_classification == "MEDIUM"
        or risk_level == "MEDIUM"
    ):
        decision_priority = "MEDIUM"

    else:
        decision_priority = "LOW"

    # =========================================
    # 7. Recommendations
    # =========================================

    recommendations = generate_recommendations(
        prospectivity_score=prospectivity[
            "prospectivity_score"
        ],
        prospectivity_classification=(
            prospectivity_classification
        ),
        risk_level=risk_level,
        shortfall=shortfall,
        shortfall_percentage=shortfall_percentage,
    )

    # =========================================
    # 8. Final response
    # =========================================

    return {
        "mine_id": mine.id,
        "mine_name": mine.name,

        "prospectivity_score": prospectivity[
            "prospectivity_score"
        ],

        "prospectivity_classification": (
            prospectivity_classification
        ),

        "production_available": True,

        "forecast_production": forecast_production,

        "forecast_demand": forecast_demand,

        "shortfall": round(shortfall, 2),

        "shortfall_percentage": shortfall_percentage,

        "production_risk": risk_level,

        "decision_priority": decision_priority,

        "recommendations": recommendations,

        "model_version": "decision-support-v1",
    }