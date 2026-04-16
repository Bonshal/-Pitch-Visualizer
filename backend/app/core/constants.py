"""Constants for cinematic direction and prompt engineering."""

# Cinematic shot types the Director LLM can assign
CINEMATIC_SHOTS = [
    "Extreme Wide Shot",
    "Wide Shot",
    "Full Shot",
    "Medium Wide Shot",
    "Medium Shot",
    "Medium Close-Up",
    "Close-Up",
    "Extreme Close-Up",
    "Over-the-Shoulder",
    "Low Angle",
    "High Angle",
    "Dutch Angle",
    "Bird's Eye View",
    "Point of View",
]

# Emotional beats for narrative arc guidance
EMOTION_PALETTE = [
    "frustration",
    "confusion",
    "curiosity",
    "discovery",
    "hope",
    "determination",
    "breakthrough",
    "relief",
    "confidence",
    "triumph",
    "collaboration",
    "vision",
]

# Lighting moods the Director can assign
LIGHTING_MOODS = [
    "harsh fluorescent overhead, cold blue tones",
    "warm golden hour sunlight, long shadows",
    "soft diffused studio light, neutral tones",
    "dramatic single-source spotlight, deep shadows",
    "cool moonlit ambiance, silver undertones",
    "neon-lit urban glow, saturated colors",
    "overcast flat light, muted palette",
    "sunrise warmth, optimistic orange-pink hues",
]
