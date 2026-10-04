from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Equipment(Base):
    __tablename__ = "equipment"

    id: Mapped[int] = mapped_column(primary_key=True)

    mine_id: Mapped[int] = mapped_column(
        ForeignKey("mines.id"),
        index=True,
    )

    name: Mapped[str] = mapped_column(String(100))

    equipment_type: Mapped[str] = mapped_column(String(100))

    status: Mapped[str] = mapped_column(
        String(50),
        default="operational",
    )

    downtime_hours: Mapped[float] = mapped_column(
        Float,
        default=0,
    )