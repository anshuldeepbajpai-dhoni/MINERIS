from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ProductionRecord(Base):
    __tablename__ = "production_records"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    mine_id: Mapped[int] = mapped_column(
        ForeignKey("mines.id"),
        nullable=False,
        index=True,
    )

    year: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    planned_production: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    actual_production: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    demand: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )