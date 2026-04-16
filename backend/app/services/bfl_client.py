"""Async client for the BFL FLUX.2 API with poll-based result retrieval.

API Pattern:
  1. POST https://api.bfl.ai/v1/{model} → {id, polling_url, cost}
  2. GET  {polling_url}                 → poll until status == "Ready"
  3. result.sample                      → temporary image URL (expires ~10 min)
"""

import asyncio
import logging

import httpx

from app.config import settings

logger = logging.getLogger(__name__)


class BFLError(Exception):
    """Raised when BFL API returns an error."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class BFLClient:
    """Async client wrapping the BFL FLUX.2 REST API."""

    def __init__(self):
        self.base_url = settings.BFL_API_BASE
        self.model = settings.BFL_MODEL
        self.api_key = settings.BFL_API_KEY
        self.poll_interval = settings.BFL_POLL_INTERVAL
        self.poll_timeout = settings.BFL_POLL_TIMEOUT

    def _headers(self) -> dict:
        return {
            "accept": "application/json",
            "x-key": self.api_key,
            "Content-Type": "application/json",
        }

    async def _submit_request(
        self, client: httpx.AsyncClient, payload: dict
    ) -> tuple[str, str]:
        """Submit a generation request, return (request_id, polling_url)."""
        url = f"{self.base_url}/{self.model}"
        logger.info("BFL submit → %s  payload keys: %s", url, list(payload.keys()))

        resp = await client.post(url, headers=self._headers(), json=payload, timeout=30)

        if resp.status_code == 402:
            raise BFLError("Insufficient BFL credits. Top up at dashboard.bfl.ai", 402)
        if resp.status_code == 429:
            raise BFLError("BFL rate limit exceeded. Try again shortly.", 429)
        if resp.status_code >= 400:
            raise BFLError(f"BFL API error {resp.status_code}: {resp.text}", resp.status_code)

        data = resp.json()
        request_id = data["id"]
        polling_url = data["polling_url"]
        cost = data.get("cost", "?")
        logger.info("BFL request submitted — id=%s  cost=%s credits", request_id, cost)
        return request_id, polling_url

    async def _poll_result(self, client: httpx.AsyncClient, polling_url: str) -> str:
        """Poll the result URL until Ready, return the image sample URL."""
        elapsed = 0.0
        while elapsed < self.poll_timeout:
            resp = await client.get(polling_url, headers=self._headers(), timeout=15)
            data = resp.json()
            status = data.get("status", "Unknown")

            if status == "Ready":
                sample_url = data["result"]["sample"]
                logger.info("BFL image ready → %s", sample_url[:80])
                return sample_url
            elif status in ("Error", "Failed", "Request Moderated"):
                raise BFLError(f"BFL generation failed: {data}")

            await asyncio.sleep(self.poll_interval)
            elapsed += self.poll_interval

        raise BFLError(f"BFL polling timed out after {self.poll_timeout}s")

    # ── Public API ──────────────────────────────────────────────────────

    async def generate_text_to_image(
        self,
        prompt: str,
        width: int | None = None,
        height: int | None = None,
        seed: int | None = None,
    ) -> str:
        """Generate an image from a text prompt only (no reference images).

        Returns the temporary image URL.
        """
        payload: dict = {
            "prompt": prompt,
            "width": width or settings.IMAGE_WIDTH,
            "height": height or settings.IMAGE_HEIGHT,
        }
        if seed is not None:
            payload["seed"] = seed

        async with httpx.AsyncClient() as client:
            _, polling_url = await self._submit_request(client, payload)
            return await self._poll_result(client, polling_url)

    async def generate_with_references(
        self,
        prompt: str,
        reference_images: list[str],
        width: int | None = None,
        height: int | None = None,
        seed: int | None = None,
    ) -> str:
        """Generate an image with multi-reference inputs for character consistency.

        reference_images: list of image URLs (concept art from previous steps).
        Maps to input_image, input_image_2, ... input_image_8.

        Returns the temporary image URL.
        """
        payload: dict = {
            "prompt": prompt,
            "width": width or settings.IMAGE_WIDTH,
            "height": height or settings.IMAGE_HEIGHT,
        }
        if seed is not None:
            payload["seed"] = seed

        # Map reference images to input_image, input_image_2, etc.
        for i, img_url in enumerate(reference_images[:8]):  # max 8 refs
            key = "input_image" if i == 0 else f"input_image_{i + 1}"
            payload[key] = img_url

        async with httpx.AsyncClient() as client:
            _, polling_url = await self._submit_request(client, payload)
            return await self._poll_result(client, polling_url)


# Module-level singleton
bfl_client = BFLClient()
