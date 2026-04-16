"""BFL FLUX.2 provider — multi-reference image generation.

API pattern:
  POST https://api.bfl.ai/v1/{model} → { polling_url }
  GET  {polling_url}                 → poll until status == "Ready"
  result.sample                      → image URL
"""

import asyncio
import logging

import httpx

from app.services.providers.base import ImageProvider, ProviderError

logger = logging.getLogger(__name__)

BFL_API_BASE = "https://api.bfl.ml/v1"
POLL_INTERVAL = 1.0   # seconds
POLL_TIMEOUT  = 120.0 # seconds


class BFLProvider(ImageProvider):
    """BFL FLUX — supports native multi-reference conditioning."""

    def __init__(self, api_key: str, model: str = "flux-pro-1.1"):
        self.api_key = api_key
        self.model   = model

    def _headers(self) -> dict:
        return {
            "accept": "application/json",
            "x-key": self.api_key,
            "Content-Type": "application/json",
        }

    async def _submit(self, client: httpx.AsyncClient, payload: dict) -> str:
        url  = f"{BFL_API_BASE}/{self.model}"
        resp = await client.post(url, headers=self._headers(), json=payload, timeout=30)

        if resp.status_code == 402:
            raise ProviderError("Insufficient BFL credits — top up at dashboard.bfl.ai", 402)
        if resp.status_code == 429:
            raise ProviderError("BFL rate limit exceeded — try again shortly.", 429)
        if resp.status_code >= 400:
            raise ProviderError(f"BFL error {resp.status_code}: {resp.text}", resp.status_code)

        data = resp.json()
        logger.info("BFL request submitted — id=%s", data.get("id"))
        return data["polling_url"]

    async def _poll(self, client: httpx.AsyncClient, polling_url: str) -> str:
        elapsed = 0.0
        while elapsed < POLL_TIMEOUT:
            resp   = await client.get(polling_url, headers=self._headers(), timeout=15)
            data   = resp.json()
            status = data.get("status", "Unknown")

            if status == "Ready":
                return data["result"]["sample"]
            if status in ("Error", "Failed", "Request Moderated"):
                raise ProviderError(f"BFL generation failed: {status}")

            await asyncio.sleep(POLL_INTERVAL)
            elapsed += POLL_INTERVAL

        raise ProviderError(f"BFL polling timed out after {POLL_TIMEOUT}s")

    async def generate_text_to_image(self, prompt: str, width: int = 1440, height: int = 810) -> str:
        async with httpx.AsyncClient() as client:
            polling_url = await self._submit(client, {"prompt": prompt, "width": width, "height": height})
            return await self._poll(client, polling_url)

    async def generate_with_references(
        self, prompt: str, reference_images: list[str], width: int = 1440, height: int = 810
    ) -> str:
        """FLUX.2 native multi-reference support — up to 8 reference images."""
        payload: dict = {"prompt": prompt, "width": width, "height": height}
        for i, url in enumerate(reference_images[:8]):
            key = "input_image" if i == 0 else f"input_image_{i + 1}"
            payload[key] = url

        async with httpx.AsyncClient() as client:
            polling_url = await self._submit(client, payload)
            return await self._poll(client, polling_url)
