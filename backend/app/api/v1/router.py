from fastapi import APIRouter

from app.api.v1.auth.routes import router as auth_router

from app.api.v1.mines.routes import router as mines_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(mines_router)


@router.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "mineris-api",
        "version": "v1",
    }