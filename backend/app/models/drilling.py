from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from geoalchemy2 import Geometry

from app.db.database import Base


class DrillHole(Base):
    __tablename__ = "drill_holes"

    id: Mapped[int] = mapped_column(primary_key=True)

    mine_id: Mapped[int] = mapped_column(
        ForeignKey("mines.id"),
        index=True,
    )

    depth_m: Mapped[float | None] = mapped_column(Float)

    manganese_grade: Mapped[float | None] = mapped_column(Float)

    location = mapped_column(
        Geometry(
            geometry_type="POINT",
            srid=4326,
        ),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )