from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Risk(Base):
    __tablename__ = "risks"

    id: Mapped[int] = mapped_column(primary_key=True)

    mine_id: Mapped[int] = mapped_column(
        ForeignKey("mines.id"),
        index=True,
    )

    risk_type: Mapped[str] = mapped_column(
        String(100)
    )

    severity: Mapped[str] = mapped_column(
        String(30)
    )

    probability: Mapped[float] = mapped_column(
        Float
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )