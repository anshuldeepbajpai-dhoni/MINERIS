import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI
from app.api.v1.router import router as api_router
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

app = FastAPI(
    title="MINERIS API",
    description=(
        "Mineral Intelligence & Resource Information System "
        "for manganese resource and production intelligence."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in settings.cors_origins.split(",")
        if origin.strip()
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    api_router,
    prefix="/api/v1",
)


@app.get("/")
async def root():
    return {
        "name": "MINERIS",
        "version": "0.1.0",
        "status": "online",
    }
