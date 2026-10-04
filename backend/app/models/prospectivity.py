from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from sqlalchemy import JSON, Float


class ProspectivityResult(Base):
    __tablename__ = "prospectivity_results"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    mine_id: Mapped[int] = mapped_column(
        ForeignKey("mines.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    prospectivity_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    classification: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    geological_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    remote_sensing_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    structural_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    historical_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    explanation: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    model_version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="baseline-v1",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)

    class_probabilities: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    feature_importance: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )