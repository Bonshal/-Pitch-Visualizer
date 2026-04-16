"""Abstract base class for all image generation providers.

Every provider must implement generate_text_to_image().
generate_with_references() defaults to text-only fallback for providers
that don't natively support multi-image reference conditioning.
"""

from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class ImageProvider(ABC):
    """Common interface for all image generation backends."""

    @abstractmethod
    async def generate_text_to_image(
        self,
        prompt: str,
        width: int = 1440,
        height: int = 810,
    ) -> str:
        """Generate an image from a prompt. Returns image URL."""
        ...

    async def generate_with_references(
        self,
        prompt: str,
        reference_images: list[str],
        width: int = 1440,
        height: int = 810,
    ) -> str:
        """Generate with reference images for character consistency.

        Default implementation: ignores references and falls back to
        pure text-to-image. Providers that support multi-reference
        conditioning should override this method.
        """
        logger.info(
            "%s does not support multi-reference generation — falling back to text-to-image.",
            self.__class__.__name__,
        )
        return await self.generate_text_to_image(prompt, width, height)


class ProviderError(Exception):
    """Raised when a provider returns an error response."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code
