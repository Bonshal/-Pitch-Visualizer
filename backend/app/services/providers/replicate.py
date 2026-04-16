"""Replicate provider — compatible with Banana.dev successor.

Banana.dev shut down in 2023; Replicate is the standard replacement.
Uses the Replicate HTTP API to run models like SDXL or FLUX on-demand.

API pattern:
  POST https://api.replicate.com/v1/models/{owner}/{model}/predictions
  GET  https://api.replicate.com/v1/predictions/{id}  → poll until "succeeded"
  output[0]  → image URL

Default model: black-forest-labs/flux-1.1-pro
"""

import asyncio
import logging

import httpx

from app.services.providers.base import ImageProvider, ProviderError

logger = logging.getLogger(__name__)

REPLICATE_API_BASE = "https://api.replicate.com/v1"
POLL_INTERVAL = 1.0
POLL_TIMEOUT  = 120.0

# Default model — can be overridden by user
DEFAULT_MODEL = "black-forest-labs/flux-1.1-pro"


class ReplicateProvider(ImageProvider):
    """Replicate provider (Banana.dev successor) — text-to-image."""

    def __init__(self, api_key: str, model: str = DEFAULT_MODEL):
        self.api_key = api_key
        self.model   = model  # "owner/model-name" format

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type":  "application/json",
            "Prefer":        "wait",  # wait up to 60s before falling back to polling
        }

    async def _submit(self, client: httpx.AsyncClient, prompt: str, width: int, height: int) -> dict:
        """Submit prediction, return the prediction object."""
        owner, name = self.model.split("/", 1)
        url = f"{REPLICATE_API_BASE}/models/{owner}/{name}/predictions"

        payload = {
            "input": {
                "prompt": prompt,
                "width":  width,
                "height": height,
            }
        }

        resp = await client.post(url, headers=self._headers(), json=payload, timeout=70)

        if resp.status_code == 401:
            raise ProviderError("Invalid Replicate API token.", 401)
        if resp.status_code == 422:
            raise ProviderError(f"Replicate validation error: {resp.text}", 422)
        if resp.status_code >= 400:
            raise ProviderError(f"Replicate error {resp.status_code}: {resp.text}", resp.status_code)

        return resp.json()

    async def _poll(self, client: httpx.AsyncClient, prediction_id: str) -> str:
        """Poll until the prediction succeeds, return output URL."""
        elapsed = 0.0
        url = f"{REPLICATE_API_BASE}/predictions/{prediction_id}"

        while elapsed < POLL_TIMEOUT:
            resp   = await client.get(url, headers=self._headers(), timeout=15)
            data   = resp.json()
            status = data.get("status")

            if status == "succeeded":
                output = data.get("output")
                # output is either a URL string or list of URLs
                if isinstance(output, list):
                    return output[0]
                return output

            if status in ("failed", "canceled"):
                raise ProviderError(f"Replicate prediction {status}: {data.get('error')}")

            await asyncio.sleep(POLL_INTERVAL)
            elapsed += POLL_INTERVAL

        raise ProviderError(f"Replicate polling timed out after {POLL_TIMEOUT}s")

    async def generate_text_to_image(self, prompt: str, width: int = 1440, height: int = 810) -> str:
        async with httpx.AsyncClient() as client:
            prediction = await self._submit(client, prompt, width, height)

            # "Prefer: wait" may return a completed prediction immediately
            if prediction.get("status") == "succeeded":
                output = prediction.get("output")
                if isinstance(output, list):
                    return output[0]
                return output

            return await self._poll(client, prediction["id"])
