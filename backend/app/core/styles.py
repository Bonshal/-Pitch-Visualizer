"""Predefined art style definitions for the Style Gallery."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ArtStyle:
    id: str
    name: str
    description: str
    prompt_blueprint: str
    thumbnail: str  # filename in /style-thumbnails/


# The five curated styles
STYLES = {
    "corporate_vector": ArtStyle(
        id="corporate_vector",
        name="Corporate Vector",
        description="Clean flat illustrations with minimal shapes and a professional palette. Perfect for SaaS, fintech, and enterprise pitches.",
        prompt_blueprint="clean flat vector illustration, minimal geometric shapes, muted professional color palette, white background, modern infographic style, simple clean lines, corporate design language",
        thumbnail="corporate_vector.webp",
    ),
    "cinematic_3d": ArtStyle(
        id="cinematic_3d",
        name="Cinematic 3D",
        description="Photorealistic 3D renders with dramatic lighting and depth. Ideal for product showcases and high-impact presentations.",
        prompt_blueprint="photorealistic 3D render, cinematic dramatic lighting, shallow depth of field, volumetric fog and god rays, Unreal Engine 5 quality, film grain, anamorphic lens flare, professional color grading",
        thumbnail="cinematic_3d.webp",
    ),
    "watercolor_story": ArtStyle(
        id="watercolor_story",
        name="Watercolor Story",
        description="Soft hand-painted textures with warm earthy tones. Great for storytelling, education, and human-centered narratives.",
        prompt_blueprint="soft watercolor painting, hand-painted textures, textured cream paper, warm earthy tones, storybook illustration, loose expressive brushstrokes, gentle color bleeds, artistic and warm",
        thumbnail="watercolor_story.webp",
    ),
    "noir_neon": ArtStyle(
        id="noir_neon",
        name="Noir & Neon",
        description="High-contrast cyberpunk aesthetic with neon glows on dark surfaces. Perfect for tech, AI, and futuristic themes.",
        prompt_blueprint="high contrast noir aesthetic, vibrant neon glow lights on dark surfaces, cyberpunk atmosphere, rain-slicked reflections, moody cinematic tone, deep shadows, electric magenta and cyan accents, dark dramatic composition",
        thumbnail="noir_neon.webp",
    ),
    "retro_pixel": ArtStyle(
        id="retro_pixel",
        name="Retro Pixel",
        description="Vibrant 16-bit pixel art with nostalgic arcade charm. Ideal for gaming, social media, and playful brand stories.",
        prompt_blueprint="detailed 16-bit pixel art, vibrant retro arcade color palette, nostalgic video game aesthetic, clean precise pixel work, subtle scanline effect, dithered shading, pixel-perfect crisp edges",
        thumbnail="retro_pixel.webp",
    ),
}

STYLE_IDS = list(STYLES.keys())
