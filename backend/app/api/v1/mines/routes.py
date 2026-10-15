import json
import logging
import pickle

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.dependencies import get_db
from app.models.mine import Mine
from app.models.user import User
from app.schemas.mine import MineResponse
from app.schemas.prospectivity import (
    ProspectivityOverviewItem,
    ProspectivityResponse,
)
from app.services.prospectivity import get_or_create_prospectivity
from app.api.v1.mines.production import router as production_router
from app.api.v1.mines.decision_support import (
    router as decision_support_router,
)


router = APIRouter(
    prefix="/mines",
    tags=["Mines"],
)
logger = logging.getLogger(__name__)


@router.get(
    "",
    response_model=list[MineResponse],
)
def get_mines(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    mines = db.scalars(
        select(Mine).order_by(Mine.id)
    ).all()

    return mines


@router.get(
    "/geojson",
)
def get_mines_geojson(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    mines = db.execute(
        select(
            Mine.id,
            Mine.name,
            Mine.location,
            Mine.description,
            Mine.area_hectares,
            func.ST_AsGeoJSON(
                Mine.boundary
            ).label("geometry"),
        ).order_by(Mine.id)
    ).all()

    features = []

    for mine in mines:
        features.append(
            {
                "type": "Feature",
                "geometry": (
                    None
                    if mine.geometry is None
                    else json.loads(mine.geometry)
                ),
                "properties": {
                    "id": mine.id,
                    "name": mine.name,
                    "location": mine.location,
                    "description": mine.description,
                    "area_hectares": mine.area_hectares,
                },
            }
        )

    return {
        "type": "FeatureCollection",
        "features": features,
    }

@router.get(
    "/{mine_id}/prospectivity",
    response_model=ProspectivityResponse,
)
def get_mine_prospectivity(
    mine_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    mine = db.get(Mine, mine_id)

    if mine is None:
        raise HTTPException(
            status_code=404,
            detail="Mine not found",
        )

    return get_or_create_prospectivity(
        db=db,
        mine=mine,
    )


@router.get(
    "/prospectivity-overview",
    response_model=list[ProspectivityOverviewItem],
)
def get_prospectivity_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return the current model's prospectivity result for each mine."""
    try:
        mines = db.scalars(select(Mine).order_by(Mine.id)).all()
        results = [get_or_create_prospectivity(db, mine) for mine in mines]
    except (
        AttributeError,
        EOFError,
        FileNotFoundError,
        ImportError,
        KeyError,
        pickle.UnpicklingError,
        TypeError,
        ValueError,
    ) as exc:
        db.rollback()
        logger.exception("Prospectivity model could not produce an overview")
        raise HTTPException(
            status_code=503,
            detail="Prospectivity model is unavailable. Prepare the model artifact and retry.",
        ) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Database error while building prospectivity overview")
        raise HTTPException(
            status_code=500,
            detail="Unable to load prospectivity overview.",
        ) from exc

    return [
        ProspectivityOverviewItem(
            mine_id=mine.id,
            mine_name=mine.name,
            score=result.prospectivity_score,
            classification=result.classification,
            confidence=result.confidence,
            model_version=result.model_version,
        )
        for mine, result in zip(mines, results)
    ]

@router.get(
    "/{mine_id}",
    response_model=MineResponse,
)
def get_mine(
    mine_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    mine = db.get(Mine, mine_id)

    if mine is None:
        raise HTTPException(
            status_code=404,
            detail="Mine not found",
        )

    return mine

router.include_router(production_router)
router.include_router(decision_support_router)
