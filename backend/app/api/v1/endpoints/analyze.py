"""POST /api/v1/analyze — Director LLM endpoint.

Accepts a pitch text + style selection, returns structured storyboard outline.
"""

import logging

from fastapi import APIRouter, HTTPException

from app.schemas.pitch import AnalyzeRequest, AnalyzeResponse
from app.services.director import analyze_pitch
from app.core.styles import STYLES

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    """Analyze a business pitch and return a structured storyboard outline."""

    # Validate style
    if request.selected_style not in STYLES:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown style '{request.selected_style}'. "
            f"Available: {list(STYLES.keys())}",
        )

    try:
        result = await analyze_pitch(request.pitch_text, request.selected_style)
        return AnalyzeResponse(
            entities=result["entities"],
            scenes=result["scenes"],
            selected_style=request.selected_style,
        )
    except Exception as e:
        logger.exception("Director analysis failed")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
