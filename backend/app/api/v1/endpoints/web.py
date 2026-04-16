"""Web UI routes using Jinja2."""

import json
import logging
import uuid
from typing import Optional

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sse_starlette.sse import EventSourceResponse

from app.core.session import MOCK_REDIS_STORE
from app.schemas.storyboard import ProviderConfig
from app.services.director import analyze_pitch
from app.services.asset_forge import generate_storyboard
from app.core.styles import STYLES

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the main input form."""
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/submit")
async def submit_pitch(
    request: Request,
    pitch: str = Form(...),
    style: str = Form(...),
    custom_style_prompt: Optional[str] = Form(""),
    provider: str = Form(...),
    api_key: Optional[str] = Form(""),
    model: Optional[str] = Form(None),
    aws_access_key_id: Optional[str] = Form(""),
    aws_secret_access_key: Optional[str] = Form(""),
    gemini_api_key: Optional[str] = Form(""),
):
    """Accept the form, create a session, redirect to loading."""
    session_id = str(uuid.uuid4())
    
    # Store request parameters
    MOCK_REDIS_STORE[session_id] = {
        "pitch": pitch,
        "style": style,
        "custom_style_prompt": custom_style_prompt,
        "provider": provider,
        "credentials": {
            "api_key": api_key,
            "model": model,
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
        },
        "gemini_api_key": gemini_api_key,
        "frames": [],
        "status": "pending"
    }
    
    return RedirectResponse(url=f"/loading/{session_id}", status_code=303)

@router.get("/loading/{session_id}", response_class=HTMLResponse)
async def loading(request: Request, session_id: str):
    """Render the loading screen which establishes SSE connection."""
    if session_id not in MOCK_REDIS_STORE:
        return RedirectResponse(url="/")
        
    return templates.TemplateResponse("loading.html", {"request": request, "session_id": session_id})

@router.get("/api/v1/generate/stream")
async def generate_stream(session_id: str):
    """SSE endpoint: runs analysis + generation, stores frames, yields progress."""
    if session_id not in MOCK_REDIS_STORE:
        return EventSourceResponse(iter([]))
        
    session_data = MOCK_REDIS_STORE[session_id]
    
    async def event_generator():
        try:
            # 1. Analyze pitch
            yield {"event": "message", "data": json.dumps({"type": "status", "message": "Analyzing pitch elements..."})}
            
            analysis = await analyze_pitch(session_data["pitch"], session_data["style"], session_data.get("gemini_api_key"))
            entities = analysis.get("entities", [])
            scenes = analysis.get("scenes", [])
            
            if not scenes:
                raise ValueError("Director failed to generate scenes.")
                
            # Parse provider config
            cred = session_data["credentials"]
            p_config = ProviderConfig(
                name=session_data["provider"],
                api_key=cred.get("api_key"),
                model=cred.get("model"),
                aws_access_key_id=cred.get("aws_access_key_id"),
                aws_secret_access_key=cred.get("aws_secret_access_key"),
            )
            
            # 2. Run Asset Forge
            # Converting dicts back to Pydantic objects for generate_storyboard
            from app.schemas.storyboard import Entity, Scene
            entity_objs = [Entity(**e) for e in entities]
            scene_objs  = [Scene(**s) for s in scenes]
            
            async for event in generate_storyboard(
                entity_objs, 
                scene_objs, 
                session_data["style"], 
                p_config, 
                session_data.get("custom_style_prompt", "")
            ):
                # Save frames to memory so we can render them later
                if event.get("type") == "frame":
                    session_data["frames"].append(event)
                    
                yield {"event": "message", "data": json.dumps(event)}
                
        except Exception as e:
            logger.exception("Stream failed")
            yield {"event": "message", "data": json.dumps({"type": "error", "message": str(e)})}
            
    return EventSourceResponse(event_generator())

@router.get("/storyboard/{session_id}", response_class=HTMLResponse)
async def storyboard_view(request: Request, session_id: str):
    """Final Jinja2 render of the generated storyboard."""
    if session_id not in MOCK_REDIS_STORE:
        return RedirectResponse(url="/")
        
    session_data = MOCK_REDIS_STORE[session_id]
    
    return templates.TemplateResponse(
        "storyboard.html", 
        {
            "request": request,
            "frames": session_data["frames"],
            "provider": session_data["provider"],
        }
    )
