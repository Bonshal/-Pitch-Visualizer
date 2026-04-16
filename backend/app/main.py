from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.v1.router import api_router
from app.api.v1.endpoints.web import router as web_router

app = FastAPI(
    title="Pitch Visualizer API",
    description="Context-Aware Storyboard Engine — transforms business pitches into cinematic visual storyboards",
    version="1.0.0",
)

# CORS — allow the Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount v1 API routes
app.include_router(api_router, prefix="/api/v1")

# Mount Jinja2 UI routes
app.include_router(web_router)


@app.get("/health")
async def health_check():
    return {"status": "ok", "model": settings.BFL_MODEL}
