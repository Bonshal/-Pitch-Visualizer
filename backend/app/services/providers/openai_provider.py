"""OpenAI DALL-E 3 provider.

API: POST https://api.openai.com/v1/images/generations
Response returns a URL directly — no polling needed.
Does NOT support multi-reference conditioning; falls back to text-only.
"""

import logging

import httpx

from app.services.providers.base import ImageProvider, ProviderError

logger = logging.getLogger(__name__)

OPENAI_API_BASE = "https://api.openai.com/v1"

# DALL-E 3 supported sizes (must pick the closest 16:9 option)
_DALLE_SIZE = "1792x1024"  # closest to 16:9


class OpenAIProvider(ImageProvider):
    """OpenAI DALL-E 3 provider — text-to-image only (no multi-reference)."""

    def __init__(self, api_key: str, model: str = "dall-e-3"):
        self.api_key = api_key
        self.model   = model

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type":  "application/json",
        }

    async def generate_text_to_image(self, prompt: str, width: int = 1440, height: int = 810) -> str:
        # DALL-E 3 only supports fixed sizes — we use the 16:9 option
        payload = {
            "model":   self.model,
            "prompt":  prompt,
            "size":    _DALLE_SIZE,
            "quality": "hd",
            "n":       1,
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{OPENAI_API_BASE}/images/generations",
                headers=self._headers(),
                json=payload,
                timeout=60,
            )

        if resp.status_code == 401:
            raise ProviderError("Invalid OpenAI API key.", 401)
        if resp.status_code == 429:
            raise ProviderError("OpenAI rate limit or quota exceeded.", 429)
        if resp.status_code >= 400:
            err = resp.json().get("error", {}).get("message", resp.text)
            raise ProviderError(f"OpenAI error {resp.status_code}: {err}", resp.status_code)

        data = resp.json()
        url  = data["data"][0]["url"]
        logger.info("DALL-E 3 image ready → %s", url[:80])
        return url
