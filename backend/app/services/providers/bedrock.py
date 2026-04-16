"""AWS Bedrock provider — Stable Diffusion XL and Amazon Titan Image Generator.

Uses boto3 with user-supplied AWS credentials.
Does NOT support multi-reference conditioning — inherits text-only fallback.

Supported model IDs:
  - stability.stable-diffusion-xl-v1
  - stability.stable-image-ultra-v1:0  (most capable)
  - amazon.titan-image-generator-v1
"""

import base64
import io
import json
import logging
import uuid

from app.services.providers.base import ImageProvider, ProviderError

logger = logging.getLogger(__name__)

DEFAULT_BEDROCK_MODEL   = "stability.stable-diffusion-xl-v1"
DEFAULT_BEDROCK_REGION  = "us-east-1"


class BedrockProvider(ImageProvider):
    """AWS Bedrock provider for Stable Diffusion / Titan image generation."""

    def __init__(
        self,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        region: str = DEFAULT_BEDROCK_REGION,
        model_id: str = DEFAULT_BEDROCK_MODEL,
    ):
        self.aws_access_key_id     = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region                = region
        self.model_id              = model_id

    def _get_client(self):
        """Create a boto3 bedrock-runtime client with the user's credentials."""
        try:
            import boto3
        except ImportError:
            raise ProviderError(
                "boto3 is not installed. Run: uv pip install boto3"
            )

        return boto3.client(
            service_name          = "bedrock-runtime",
            region_name           = self.region,
            aws_access_key_id     = self.aws_access_key_id,
            aws_secret_access_key = self.aws_secret_access_key,
        )

    def _build_payload(self, prompt: str, width: int, height: int) -> dict:
        """Build the request payload for the configured model."""
        model = self.model_id.lower()

        if model.startswith("stability.sd3") or model.startswith("stability.stable-image"):
            # New Stability models (SD3, Core, Ultra)
            return {
                "prompt": prompt,
                "mode": "text-to-image",
                "aspect_ratio": "16:9",
                "output_format": "png",
            }
        elif model.startswith("stability."):
            # Legacy Stable Diffusion XL
            return {
                "text_prompts": [{"text": prompt, "weight": 1.0}],
                "cfg_scale":    7,
                "steps":        50,
                "width":        min(width, 1024),
                "height":       min(height, 1024),
                "seed":         0,
                "samples":      1,
            }
        elif model.startswith("amazon.titan"):
            # Amazon Titan Image Generator
            return {
                "taskType": "TEXT_IMAGE",
                "textToImageParams": {"text": prompt},
                "imageGenerationConfig": {
                    "numberOfImages": 1,
                    "width":  min(width, 1408),
                    "height": min(height, 768),
                    "cfgScale": 8.0,
                },
            }
        else:
            raise ProviderError(f"Unsupported Bedrock model: {self.model_id}")

    def _extract_image_bytes(self, response_body: dict) -> bytes:
        """Extract raw image bytes from the model response."""
        model = self.model_id.lower()

        if model.startswith("stability.sd3") or model.startswith("stability.stable-image"):
            # New Stability models return base64 in "image" or "images" array (base64 string directly)
            b64 = response_body.get("image")
            if not b64 and "images" in response_body:
                 b64 = response_body["images"][0]
        elif model.startswith("stability."):
            # Legacy SDXL returns inside "artifacts" -> "base64"
            b64 = response_body["artifacts"][0]["base64"]
        elif model.startswith("amazon.titan"):
            b64 = response_body["images"][0]
        else:
            raise ProviderError(f"Cannot extract image from model: {self.model_id}")

        if not b64:
             raise ProviderError("No base64 image data found in Bedrock response.")
             
        return base64.b64decode(b64)

    async def generate_text_to_image(self, prompt: str, width: int = 1440, height: int = 810) -> str:
        """Generate image, save to a temporary data URL (base64).

        Bedrock returns raw bytes. We return a base64 data URL since
        Bedrock images are not publicly accessible URLs.
        """
        import asyncio

        def _invoke():
            client  = self._get_client()
            payload = self._build_payload(prompt, width, height)
            resp    = client.invoke_model(
                modelId     = self.model_id,
                body        = json.dumps(payload),
                contentType = "application/json",
                accept      = "application/json",
            )
            body = json.loads(resp["body"].read())
            return self._extract_image_bytes(body)

        try:
            # Run the synchronous boto3 call in a thread pool
            loop       = asyncio.get_event_loop()
            img_bytes  = await loop.run_in_executor(None, _invoke)

            # Return as base64 data URL so the browser can display it directly
            b64  = base64.b64encode(img_bytes).decode("utf-8")
            data_url = f"data:image/png;base64,{b64}"
            logger.info("Bedrock image generated — %d bytes", len(img_bytes))
            return data_url

        except ProviderError:
            raise
        except Exception as e:
            raise ProviderError(f"AWS Bedrock error: {str(e)}")
