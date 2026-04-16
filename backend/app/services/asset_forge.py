"""Asset Forge — orchestrates the full storyboard generation pipeline.

Pipeline:
  1. Lock entity text blueprints
  2. Generate concept art via text-to-image
  3. Generate scene frames via multi-reference editing (or text-only fallback)
  4. Yield results as they complete (for SSE streaming)
"""

import logging
from typing import AsyncGenerator

from app.core.styles import STYLES
from app.schemas.storyboard import Entity, Scene, ProviderConfig
from app.services.providers.base import ProviderError
from app.services.providers.factory import get_provider
from app.services.prompt_engine import (
    compose_concept_prompt,
    compose_frame_prompt,
    build_entity_blueprint,
)

logger = logging.getLogger(__name__)


async def generate_storyboard(
    entities:        list[Entity],
    scenes:          list[Scene],
    selected_style:  str,
    provider_config: ProviderConfig,
) -> AsyncGenerator[dict, None]:
    """Full production pipeline — yields JSON events as frames complete.

    Event types:
      {"type": "status",  "message": "..."}
      {"type": "concept", "entity_id": "...", "entity_name": "...", "image_url": "..."}
      {"type": "frame",   "scene_id": "...", "scene_title": "...",
       "image_url": "...", "emotion": "...", "cinematic_shot": "..."}
      {"type": "complete"}
      {"type": "error",   "message": "..."}
    """
    style = STYLES.get(selected_style)
    if not style:
        yield {"type": "error", "message": f"Unknown style: {selected_style}"}
        return

    # Instantiate the correct provider from user credentials
    try:
        credentials = provider_config.model_dump(exclude_none=True)
        name = credentials.pop("name")
        provider = get_provider(name, credentials)
        yield {"type": "status", "message": f"Provider ready: {name.upper()}"}
    except ProviderError as e:
        yield {"type": "error", "message": str(e)}
        return

    # ── Step 1: Lock entity blueprints ────────────────────────────────
    yield {"type": "status", "message": "Locking entity blueprints..."}
    for entity in entities:
        build_entity_blueprint(entity, style)
        logger.info("Blueprint locked for %s", entity.name)

    # ── Step 2: Concept art ───────────────────────────────────────────
    concept_images: dict[str, str] = {}
    concept_entities = sorted(entities, key=lambda e: 0 if e.type == "character" else 1)[:3]

    for entity in concept_entities:
        yield {"type": "status", "message": f"Generating concept art for {entity.name}..."}
        try:
            prompt    = compose_concept_prompt(entity, style)
            image_url = await provider.generate_text_to_image(prompt, width=1024, height=1024)
            concept_images[entity.id] = image_url
            yield {
                "type":        "concept",
                "entity_id":   entity.id,
                "entity_name": entity.name,
                "image_url":   image_url,
            }
        except ProviderError as e:
            logger.error("Concept art failed for %s: %s", entity.name, e)
            yield {"type": "status", "message": f"⚠ Concept art skipped for {entity.name}: {e}"}

    # ── Step 3: Scene frames ──────────────────────────────────────────
    for i, scene in enumerate(scenes):
        yield {"type": "status", "message": f"Generating frame {i + 1}/{len(scenes)}: {scene.title}..."}
        try:
            prompt     = compose_frame_prompt(scene, entities, style)
            ref_images = [concept_images[eid] for eid in scene.entities_involved if eid in concept_images]

            if ref_images:
                image_url = await provider.generate_with_references(prompt, ref_images)
            else:
                image_url = await provider.generate_text_to_image(prompt)

            yield {
                "type":          "frame",
                "scene_id":      scene.id,
                "scene_title":   scene.title,
                "scene_action":  scene.action,
                "image_url":     image_url,
                "emotion":       scene.emotion,
                "cinematic_shot": scene.cinematic_shot,
                "frame_index":   i,
                "total_frames":  len(scenes),
            }
        except ProviderError as e:
            logger.error("Frame failed for scene %s: %s", scene.id, e)
            yield {"type": "error", "message": f"Frame failed for '{scene.title}': {e}"}

    yield {"type": "complete", "message": "Storyboard generation complete!"}
