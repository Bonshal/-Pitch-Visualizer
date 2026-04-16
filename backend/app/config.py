from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables / .env file."""

    BFL_API_KEY: str
    GEMINI_API_KEY: str
    BFL_API_BASE: str = "https://api.bfl.ai/v1"
    BFL_MODEL: str = "flux-2-max"
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # Image generation defaults
    IMAGE_WIDTH: int = 1440
    IMAGE_HEIGHT: int = 810  # 16:9 cinematic ratio
    BFL_POLL_INTERVAL: float = 1.0  # seconds between polls
    BFL_POLL_TIMEOUT: float = 120.0  # max wait per image

    # CORS
    FRONTEND_URL: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
