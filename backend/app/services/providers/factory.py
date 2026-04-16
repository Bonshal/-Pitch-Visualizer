"""Provider factory — instantiates the correct ImageProvider from user credentials."""

from app.services.providers.base import ImageProvider, ProviderError


def get_provider(name: str, credentials: dict) -> ImageProvider:
    """Return an ImageProvider instance for the given provider name and credentials."""
    name = name.lower().strip()

    if name == "bfl":
        from app.services.providers.bfl import BFLProvider
        return BFLProvider(
            api_key=credentials["api_key"],
            model=credentials.get("model", "flux-2-max"),
        )

    elif name == "openai":
        from app.services.providers.openai_provider import OpenAIProvider
        return OpenAIProvider(
            api_key=credentials["api_key"],
            model=credentials.get("model", "dall-e-3"),
        )

    elif name == "nano_banana":
        from app.services.providers.nano_banana import NanoBananaProvider
        return NanoBananaProvider(
            api_key=credentials["api_key"],
            model=credentials.get("model", "gemini-2.0-flash-preview-image-generation"),
        )

    elif name == "bedrock":
        from app.services.providers.bedrock import BedrockProvider
        return BedrockProvider(
            aws_access_key_id=credentials["aws_access_key_id"],
            aws_secret_access_key=credentials["aws_secret_access_key"],
            region=credentials.get("region", "us-east-1"),
            model_id=credentials.get("model_id", "stability.stable-diffusion-xl-v1"),
        )

    else:
        raise ProviderError(
            f"Unknown provider '{name}'. Supported: bfl, openai, nano_banana, bedrock"
        )
