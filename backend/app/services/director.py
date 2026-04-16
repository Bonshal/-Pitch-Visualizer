"""Director Agent — uses Gemini to analyze a pitch and extract a structured storyboard outline.

Implements the "Snow White" principle: focus on emotional user journey,
not literal depictions of abstract software features.
"""

import json
import logging

from google import genai
from google.genai import types

from app.config import settings
from app.core.constants import CINEMATIC_SHOTS, EMOTION_PALETTE, LIGHTING_MOODS
from app.core.styles import STYLES

logger = logging.getLogger(__name__)

# ── System prompt for the Director LLM ───────────────────────────────

DIRECTOR_SYSTEM_PROMPT = """\
You are a **Hollywood storyboard director** with 20 years of experience in visual storytelling.

Your job: transform a raw business pitch into a **cinematic visual narrative** — a storyboard 
that tells the story of the product through emotionally compelling scenes.

## The "Snow White" Principle
DO NOT literally depict abstract software features (e.g., "a dashboard showing data").
Instead, focus on the **EMOTIONAL JOURNEY of the user**:
- Show FRUSTRATION before the product (e.g., a person overwhelmed by paperwork)
- Show DISCOVERY and HOPE when they find the solution
- Show TRIUMPH and CONFIDENCE in the outcome

## Your Task
Given a pitch text and an art style, extract:

1. **ENTITIES** — recurring visual elements that must stay consistent across frames:
   - Characters: describe with hyper-specific physical details (age, hair color/style, 
     eye color, clothing, accessories, body language defaults)
   - Environments: describe with specific architectural/spatial details
   - Objects: describe with precise material, color, size details

2. **SCENES** — 4 to 7 cinematic beats forming a narrative arc:
   - Each scene captures ONE emotional moment
   - Assign a specific cinematic shot type for composition control
   - Assign lighting mood to reinforce the emotional tone
   - Reference which entities appear

## Available Shot Types
{shots}

## Available Emotions
{emotions}

## Available Lighting Moods
{lighting}

## Output Rules
- Entity descriptions must be EXTREMELY detailed (50+ words each)
- Scene actions must describe a SINGLE frozen moment, not a sequence
- The narrative must follow a clear emotional arc from problem → solution → triumph
- Generate between 4 and 7 scenes
- Generate between 2 and 5 entities
""".format(
    shots=", ".join(CINEMATIC_SHOTS),
    emotions=", ".join(EMOTION_PALETTE),
    lighting="\n".join(f"- {m}" for m in LIGHTING_MOODS),
)


# ── Gemini response schema ───────────────────────────────────────────

RESPONSE_SCHEMA = types.Schema(
    type=types.Type.OBJECT,
    properties={
        "entities": types.Schema(
            type=types.Type.ARRAY,
            items=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "id": types.Schema(type=types.Type.STRING),
                    "name": types.Schema(type=types.Type.STRING),
                    "type": types.Schema(
                        type=types.Type.STRING,
                        enum=["character", "environment", "object"],
                    ),
                    "description": types.Schema(type=types.Type.STRING),
                    "emotional_role": types.Schema(type=types.Type.STRING),
                },
                required=["id", "name", "type", "description", "emotional_role"],
            ),
        ),
        "scenes": types.Schema(
            type=types.Type.ARRAY,
            items=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "id": types.Schema(type=types.Type.STRING),
                    "title": types.Schema(type=types.Type.STRING),
                    "action": types.Schema(type=types.Type.STRING),
                    "emotion": types.Schema(type=types.Type.STRING),
                    "entities_involved": types.Schema(
                        type=types.Type.ARRAY,
                        items=types.Schema(type=types.Type.STRING),
                    ),
                    "cinematic_shot": types.Schema(type=types.Type.STRING),
                    "lighting_mood": types.Schema(type=types.Type.STRING),
                },
                required=[
                    "id", "title", "action", "emotion",
                    "entities_involved", "cinematic_shot", "lighting_mood",
                ],
            ),
        ),
    },
    required=["entities", "scenes"],
)


async def analyze_pitch(pitch_text: str, selected_style: str) -> dict:
    """Send pitch to Gemini and return structured storyboard outline.

    Returns dict with 'entities' and 'scenes' keys.
    """
    style = STYLES.get(selected_style)
    style_context = (
        f"\nThe visual style is: **{style.name}** — {style.description}\n"
        f"Style blueprint for prompts: {style.prompt_blueprint}\n"
        if style
        else ""
    )

    user_prompt = f"""\
Analyze this business pitch and create a cinematic storyboard outline.
{style_context}
## Pitch Text
{pitch_text}
"""

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    logger.info("Sending pitch to Gemini (%s) for analysis...", settings.GEMINI_MODEL)

    response = await client.aio.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=DIRECTOR_SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=RESPONSE_SCHEMA,
            temperature=0.8,
        ),
    )

    result = json.loads(response.text)
    logger.info(
        "Director analysis complete — %d entities, %d scenes",
        len(result.get("entities", [])),
        len(result.get("scenes", [])),
    )
    return result
