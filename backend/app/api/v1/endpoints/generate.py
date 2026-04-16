"""POST /api/v1/generate — Storyboard production endpoint with SSE streaming."""

import json
import logging

from fastapi import APIRouter, HTTPException
from sse_starlette.sse import EventSourceResponse

from app.schemas.storyboard import GenerateRequest
from app.services.asset_forge import generate_storyboard
from app.core.styles import STYLES

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/generate")
async def generate(request: GenerateRequest):
    if request.selected_style not in STYLES:
        raise HTTPException(status_code=400, detail=f"Unknown style '{request.selected_style}'.")
    if not request.scenes:
        raise HTTPException(status_code=400, detail="At least one scene is required.")
    if not request.entities:
        raise HTTPException(status_code=400, detail="At least one entity is required.")

    async def event_generator():
        try:
            async for event in generate_storyboard(
                entities=request.entities,
                scenes=request.scenes,
                selected_style=request.selected_style,
                provider_config=request.provider_config,
            ):
                yield {"event": event.get("type", "message"), "data": json.dumps(event)}
        except Exception as e:
            logger.exception("Generation pipeline error")
            yield {
                "event": "error",
                "data":  json.dumps({"type": "error", "message": f"Pipeline error: {e}"}),
            }

    return EventSourceResponse(event_generator())
