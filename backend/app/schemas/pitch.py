"""Pydantic schemas for the Analyze pipeline."""

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """Request body for POST /api/v1/analyze."""

    pitch_text: str = Field(
        ...,
        min_length=20,
        max_length=10000,
        description="The raw business pitch or narrative text to analyze.",
    )
    selected_style: str = Field(
        ...,
        description="The ID of the selected art style from the Style Gallery.",
    )


class AnalyzeResponse(BaseModel):
    """Response body for POST /api/v1/analyze — the Director's structured outline."""

    entities: list[dict] = Field(
        ..., description="List of extracted entities (characters, environments, objects)."
    )
    scenes: list[dict] = Field(
        ..., description="List of cinematic scene beats in narrative order."
    )
    selected_style: str = Field(
        ..., description="Echo of the selected style ID for downstream use."
    )
