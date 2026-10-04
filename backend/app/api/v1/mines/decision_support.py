from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.dependencies import get_db
from app.models.mine import Mine
from app.models.user import User
from app.schemas.decision_support import (
    DecisionSupportResponse,
)
from app.services.decision_support import (
    generate_decision_support,
)


router = APIRouter(
    tags=["Decision Support"],
)


@router.get(
    "/{mine_id}/decision-support",
    response_model=DecisionSupportResponse,
)
def get_decision_support(
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

    return generate_decision_support(
        db=db,
        mine=mine,
    )