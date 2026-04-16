"""API v1 router — aggregates all endpoint routers."""

from fastapi import APIRouter

from app.api.v1.endpoints.analyze import router as analyze_router
from app.api.v1.endpoints.generate import router as generate_router
from app.core.styles import STYLES, STYLE_IDS

api_router = APIRouter()

# Mount endpoint routers
api_router.include_router(analyze_router, tags=["analyze"])
api_router.include_router(generate_router, tags=["generate"])


@api_router.get("/styles")
async def get_styles():
    """Return the list of available art styles for the Style Gallery."""
    return [
        {
            "id": s.id,
            "name": s.name,
            "description": s.description,
            "thumbnail": s.thumbnail,
        }
        for s in STYLES.values()
    ]
