"""Configuration management for the application"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class Config:
    """Application configuration"""

    # API Keys
    openai_api_key: str | None = None
    replicate_api_key: str | None = None
    elevenlabs_api_key: str | None = None

    # Paths
    output_dir: str = "outputs"
    assets_dir: str = "assets"

    # Default settings
    default_image_size: tuple = (1024, 1024)
    default_video_fps: int = 24
    default_video_duration: int = 5

    # Audio settings
    default_voice: str = "Adam"
    default_audio_model: str = "eleven_multilingual_v2"

    def __post_init__(self):
        """Load values from environment if not provided"""
        self.openai_api_key = self.openai_api_key or os.getenv("OPENAI_API_KEY")
        self.replicate_api_key = self.replicate_api_key or os.getenv("REPLICATE_API_TOKEN")
        self.elevenlabs_api_key = self.elevenlabs_api_key or os.getenv("ELEVENLABS_API_KEY")

        # Create output directories
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.assets_dir, exist_ok=True)

    def validate(self) -> dict:
        """
        Validate configuration and return status

        Returns:
            Dictionary with validation results
        """
        return {
            "openai": bool(self.openai_api_key),
            "replicate": bool(self.replicate_api_key),
            "elevenlabs": bool(self.elevenlabs_api_key),
            "paths": os.path.exists(self.output_dir) and os.path.exists(self.assets_dir),
        }


# Global config instance
config = Config()
