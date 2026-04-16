"""Prompt Engine — composes FLUX.2-optimized prompts for storyboard frames.

Leverages FLUX.2's structured prompting capability and combines:
  - Entity text blueprints (the "Asset Bible")
  - Scene action descriptions
  - Lighting mood
  - Style blueprint
"""

import json
import logging

from app.schemas.storyboard import Entity, Scene
from app.core.styles import STYLES, ArtStyle

logger = logging.getLogger(__name__)


def build_entity_blueprint(entity: Entity, style: ArtStyle) -> str:
    """Create a locked text blueprint for an entity — the 'Asset Bible' entry."""
    return (
        f"{entity.description}. "
        f"Rendered in {style.prompt_blueprint}."
    )


def compose_concept_prompt(entity: Entity, style: ArtStyle) -> str:
    """Compose a prompt for generating concept art of an entity."""
    if entity.type == "character":
        return (
            f"Character concept art sheet. {entity.description}. "
            f"Full body, front-facing, neutral pose, plain background, "
            f"highly detailed. {style.prompt_blueprint}."
        )
    elif entity.type == "environment":
        return (
            f"Environment concept art. {entity.description}. "
            f"Establishing wide shot, detailed architecture and atmosphere, "
            f"no characters present. {style.prompt_blueprint}."
        )
    else:  # object
        return (
            f"Detailed product/object illustration. {entity.description}. "
            f"Centered, clean background, multiple angles. "
            f"{style.prompt_blueprint}."
        )


def compose_frame_prompt(
    scene: Scene,
    entities: list[Entity],
    style: ArtStyle,
) -> str:
    """Compose the full generation prompt for a storyboard frame.

    Uses a structured / descriptive format that FLUX.2 handles well.
    """
    # Gather descriptions of involved entities
    involved = [e for e in entities if e.id in scene.entities_involved]
    entity_descriptions = ". ".join(
        f"{e.name}: {e.description}" for e in involved
    )

    # Compose the structured prompt
    prompt_parts = {
        "subject": f"{entity_descriptions}. {scene.action}",
        "background": _infer_background(scene, involved),
        "lighting": scene.lighting_mood,
        "style": style.prompt_blueprint,
        "composition": "cinematic storyboard frame, 16:9 widescreen aspect ratio, high detail",
    }

    # FLUX.2 accepts JSON structured prompts
    structured_prompt = json.dumps(prompt_parts)
    logger.debug("Frame prompt for scene %s: %s", scene.id, structured_prompt[:200])
    return structured_prompt


def _infer_background(scene: Scene, involved_entities: list[Entity]) -> str:
    """Extract background context from environment entities or scene action."""
    env_entities = [e for e in involved_entities if e.type == "environment"]
    if env_entities:
        return env_entities[0].description
    # Fall back to inferring from the action
    return f"Setting implied by the scene: {scene.action[:100]}"
