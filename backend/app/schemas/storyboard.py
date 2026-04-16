"""Pydantic schemas for the Storyboard generation pipeline."""

from pydantic import BaseModel, Field


class Entity(BaseModel):
    id: str
    name: str
    type: str = Field(..., description="character | environment | object")
    description: str
    emotional_role: str


class Scene(BaseModel):
    id: str
    title: str
    action: str
    emotion: str
    entities_involved: list[str]
    lighting_mood: str


class ProviderConfig(BaseModel):
    """User-supplied image generation provider credentials."""

    name: str = Field(
        ...,
        description="Provider identifier: 'bfl', 'openai', 'replicate', 'bedrock'",
    )
    # Generic API key (used by BFL, OpenAI, Replicate)
    api_key: str | None = None

    # AWS Bedrock-specific fields
    aws_access_key_id:     str | None = None
    aws_secret_access_key: str | None = None
    region:                str | None = "us-east-1"
    model_id:              str | None = None   # Bedrock: model ARN / ID

    # Optional model override for any provider
    model: str | None = None


class GenerateRequest(BaseModel):
    entities:        list[Entity]
    scenes:          list[Scene]
    selected_style:  str
    provider_config: ProviderConfig


class FrameResult(BaseModel):
    scene_id:      str
    scene_title:   str
    image_url:     str
    emotion:       str
