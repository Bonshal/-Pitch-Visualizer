"""Google Nano Banana — Gemini Image Generation models.

Nano Banana is Google DeepMind's family of image generation models
accessed via the Gemini API:
  - gemini-2.5-flash-image-preview  (Nano Banana, fast)
  - gemini-3.1-flash-image-preview  (Nano Banana 2, balanced)
  - gemini-3-pro-image-preview       (Nano Banana Pro, highest quality)

Supports multi-image reference (up to 14 images).
Uses the google-genai SDK which is already installed.
"""

import base64
import io
import logging

from app.services.providers.base import ImageProvider, ProviderError

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "gemini-2.0-flash-preview-image-generation"


class NanoBananaProvider(ImageProvider):
    """Google Nano Banana (Gemini Image) provider."""

    def __init__(self, api_key: str, model: str = DEFAULT_MODEL):
        self.api_key = api_key
        self.model   = model

    def _get_client(self):
        try:
            from google import genai
            return genai.Client(api_key=self.api_key)
        except ImportError:
            raise ProviderError("google-genai is not installed. Run: uv pip install google-genai")

    async def generate_text_to_image(self, prompt: str, width: int = 1440, height: int = 810) -> str:
        """Generate image from text prompt, return base64 data URL."""
        try:
            from google import genai
            from google.genai import types

            client = self._get_client()

            response = await client.aio.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"],
                    response_mime_type="image/jpeg",
                ),
            )

            # Extract the image part from the response
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    b64 = base64.b64encode(part.inline_data.data).decode("utf-8")
                    mime = part.inline_data.mime_type or "image/jpeg"
                    data_url = f"data:{mime};base64,{b64}"
                    logger.info("Nano Banana image generated — model=%s", self.model)
                    return data_url

            raise ProviderError("Nano Banana returned no image in response.")

        except ProviderError:
            raise
        except Exception as e:
            error_msg = str(e)
            if "API_KEY_INVALID" in error_msg or "401" in error_msg:
                raise ProviderError("Invalid Google AI API key.", 401)
            if "RESOURCE_EXHAUSTED" in error_msg or "429" in error_msg:
                raise ProviderError("Google AI quota exceeded — try again shortly.", 429)
            raise ProviderError(f"Nano Banana error: {error_msg}")

    async def generate_with_references(
        self,
        prompt: str,
        reference_images: list[str],
        width: int = 1440,
        height: int = 810,
    ) -> str:
        """Multi-image reference generation — Nano Banana supports up to 14 refs."""
        try:
            from google import genai
            from google.genai import types
            import httpx

            client = self._get_client()

            # Build content parts: reference images + text prompt
            parts = []

            for img_url in reference_images[:14]:
                if img_url.startswith("data:"):
                    # Already a data URL (from Bedrock or previous Nano Banana call)
                    header, b64data = img_url.split(",", 1)
                    mime = header.split(":")[1].split(";")[0]
                    img_bytes = base64.b64decode(b64data)
                else:
                    # Fetch from URL
                    async with httpx.AsyncClient() as http:
                        resp = await http.get(img_url, timeout=15)
                        img_bytes = resp.content
                        mime = resp.headers.get("content-type", "image/jpeg").split(";")[0]

                parts.append(
                    types.Part(
                        inline_data=types.Blob(data=img_bytes, mime_type=mime)
                    )
                )

            # Add the text prompt
            parts.append(types.Part(text=prompt))

            response = await client.aio.models.generate_content(
                model=self.model,
                contents=[types.Content(role="user", parts=parts)],
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"],
                    response_mime_type="image/jpeg",
                ),
            )

            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    b64 = base64.b64encode(part.inline_data.data).decode("utf-8")
                    mime = part.inline_data.mime_type or "image/jpeg"
                    data_url = f"data:{mime};base64,{b64}"
                    logger.info(
                        "Nano Banana multi-ref image generated — %d refs, model=%s",
                        len(reference_images),
                        self.model,
                    )
                    return data_url

            raise ProviderError("Nano Banana returned no image in multi-reference response.")

        except ProviderError:
            raise
        except Exception as e:
            raise ProviderError(f"Nano Banana multi-reference error: {str(e)}")
