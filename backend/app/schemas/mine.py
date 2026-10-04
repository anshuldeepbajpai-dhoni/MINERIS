from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MineBase(BaseModel):
    name: str
    location: str | None = None
    description: str | None = None
    area_hectares: float | None = None


class MineResponse(MineBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)