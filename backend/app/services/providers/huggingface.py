"""Hugging Face API inference provider.

Uses the official `huggingface_hub` SDK to execute generations.
Natively leverages the new Serverless Inference Providers API,
effortlessly resolving routing to third-party GPUs (e.g. fal.ai) for gated models like FLUX.1-dev.
Returns base64 data URLs.
"""

import base64
import io
import logging

from app.services.providers.base import ImageProvider, ProviderError

logger = logging.getLogger(__name__)

# Fallback to standard SDXL if model isn't provided
DEFAULT_HF_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"


class HuggingFaceProvider(ImageProvider):
    """Hugging Face Inference API provider."""

    def __init__(self, api_key: str, model: str = DEFAULT_HF_MODEL):
        self.api_key = api_key
        self.model = model

    def _get_client(self):
        try:
            from huggingface_hub import InferenceClient
            return InferenceClient(token=self.api_key)
        except ImportError:
            raise ProviderError("huggingface_hub is not installed. Run: pip install huggingface_hub")

    async def generate_text_to_image(self, prompt: str, width: int = 1440, height: int = 810) -> str:
        """Call HF inference API using the official SDK wrapped in a thread to keep async clean."""
        import asyncio
        client = self._get_client()

        logger.info("Generating via Hugging Face SDK — model=%s", self.model)
        
        def _invoke():
            return client.text_to_image(
                prompt,
                model=self.model,
                width=min(width, 1024),
                height=min(height, 1024),
            )

        try:
            # The SDK natively handles polling, routing, and GPU fal/replicate resolution.
            # Run in a thread executor to avoid blocking the FastAPI event loop, completely bypassing the aiohttp requirement.
            loop = asyncio.get_event_loop()
            image = await loop.run_in_executor(None, _invoke)
            
            # The image object returned is a PIL.Image
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_bytes = img_byte_arr.getvalue()
            
            b64 = base64.b64encode(img_bytes).decode("utf-8")
            data_url = f"data:image/png;base64,{b64}"
            return data_url

        except Exception as e:
            error_msg = str(e)
            if "loading" in error_msg.lower():
                raise ProviderError(f"Hugging Face model {self.model} is currently loading. Please wait and try again.", 503)
            if "401" in error_msg:
                raise ProviderError("Invalid Hugging Face API key.", 401)
            raise ProviderError(f"Hugging Face SDK error: {error_msg}")
