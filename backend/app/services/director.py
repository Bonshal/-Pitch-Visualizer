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

DIRECTOR_SYSTEM_PROMPT = """\
### ROLE
You are a Senior UX Architect and Storyboard Director. Your goal is to transform unstructured business/product pitches into a professional 5-to-8 panel UX storyboard based on industry-standard design workflows.

### OPERATIONAL PHASES (MANDATORY CHAIN-OF-THOUGHT)

PHASE 1: THE FOUNDATION
- Extract ONE primary 'User Persona' and ONE specific 'Scenario'.
- Establish a 'Visual Identity Bible': Specify the Subject's physical traits, clothing, and the setting's aesthetic to prevent visual drift.

PHASE 2: USER FLOW ARCHITECTURE
- Map the narrative into a 5-to-8 step flow.
- Ensure the journey covers the full spectrum: Pre-app awareness -> Browsing/Comparing -> Booking/Conversion -> Real-world experience -> Post-experience reflection.
- CRITICAL BALANCE: You MUST interleave real-world human moments with explicit App/UI interaction moments. Do not just show the real world; explicitly show the user looking at screens, interfaces, or devices where relevant.

PHASE 3: PANEL SPECIFICATION
- Each panel MUST contain: A Visual (scene/UI interaction), a User Action, and an Emotion.
- Example Arc: 
  - Panel 1: Real world pain point (Frustrated)
  - Panel 2: UI Interaction — Browsing options on a glowing phone screen (Curious)
  - Panel 3: UI Interaction — Tapping 'Book' with a confirmation screen (Relieved)
  - Panel 4: Real world arrival at the physical destination (Excited)

PHASE 4: PROMPT ENGINEERING & JSON ALIGNMENT
- Generate a 'Refined Image Prompt' (50-70 words) for the `action` field. Use "Show, don't tell." Use lighting, camera angles, and body language to reflect the Emotion.
- Generate a 'Caption' for the `title` field answering "What is happening and why?".

### JSON SCHEMA MAPPING RULE
You MUST map your output into the required JSON schema fields exactly as follows:
- `title`: A short 1-2 line 'Caption' answering "What is happening?" and "Why?". Keep it extremely concise (max 20 words).
- `action`: The 'Refined Image Prompt' (50-70 words, "show don't tell"). Explicitly describe the physical scene and any UI/App interaction visually.
- `emotion`: The 'Underlying Emotion/Thought' (e.g. "Frustrated", "Relieved").
- `lighting_mood`: Reflected Lighting/Atmosphere.
- `entities_involved`: Array of entity IDs appearing in the shot.

## Output Rules
- Entity descriptions must be EXTREMELY detailed (50+ words each) to preserve the "Visual Identity Bible".
- Generate between 5 and 8 scenes.


1. **ENTITIES** — recurring visual elements that must stay consistent across frames:
   - Characters: describe with hyper-specific physical details (age, hair color/style, 
     eye color, clothing, accessories, body language defaults)
   - Environments: describe with specific architectural/spatial details
    - Objects: describe with precise material, color, size details


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
                    "lighting_mood": types.Schema(type=types.Type.STRING),
                },
                required=[
                    "id", "title", "action", "emotion",
                    "entities_involved", "lighting_mood",
                ],
            ),
        ),
    },
    required=["entities", "scenes"],
)


async def analyze_pitch(pitch_text: str, selected_style: str, custom_api_key: str = None) -> dict:
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

    api_key = custom_api_key.strip() if custom_api_key else settings.GEMINI_API_KEY
    if not api_key:
        raise ValueError("Google Gemini API key is missing. Please provide it in the API Details.")

    user_prompt = f"""\
Analyze this business pitch and create a cinematic storyboard outline.
{style_context}
## Pitch Text
{pitch_text}
"""

    client = genai.Client(api_key=api_key)

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
