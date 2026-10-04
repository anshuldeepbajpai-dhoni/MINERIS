from fastapi import FastAPI
from app.api.v1.router import router as api_router
from fastapi.middleware.cors import CORSMiddleware

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
        "http://localhost:5173",
        "http://127.0.0.1:5173",
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