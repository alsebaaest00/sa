"""Multi-model AI provider support for SA platform"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseImageGenerator(ABC):
    """Base class for image generators"""

    @abstractmethod
    def generate(self, prompt: str, size: str = "1024x1024", quality: str = "standard") -> str:
        """Generate an image from prompt"""
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """Get model name"""
        pass


class OpenAIImageGenerator(BaseImageGenerator):
    """OpenAI DALL-E image generator"""

    def __init__(self, api_key: str, model: str = "dall-e-3"):
        from openai import OpenAI

        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, size: str = "1024x1024", quality: str = "standard") -> str:
        """Generate image using DALL-E"""
        response = self.client.images.generate(
            model=self.model, prompt=prompt, size=size, quality=quality, n=1
        )
        return response.data[0].url

    def get_model_name(self) -> str:
        return f"OpenAI {self.model}"


class StabilityAIImageGenerator(BaseImageGenerator):
    """Stability AI image generator (Stable Diffusion)"""

    def __init__(self, api_key: str, model: str = "stable-diffusion-xl-1024-v1-0"):
        self.api_key = api_key
        self.model = model

    def generate(self, prompt: str, size: str = "1024x1024", quality: str = "standard") -> str:
        """Generate image using Stability AI"""
        # Implementation would call Stability AI API
        # This is a placeholder
        raise NotImplementedError("Stability AI integration requires API key and additional setup")

    def get_model_name(self) -> str:
        return f"Stability AI {self.model}"


class BaseAudioGenerator(ABC):
    """Base class for audio generators"""

    @abstractmethod
    def generate(self, text: str, voice: str = "alloy", speed: float = 1.0) -> bytes:
        """Generate audio from text"""
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """Get model name"""
        pass


class OpenAIAudioGenerator(BaseAudioGenerator):
    """OpenAI TTS audio generator"""

    def __init__(self, api_key: str, model: str = "tts-1"):
        from openai import OpenAI

        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, text: str, voice: str = "alloy", speed: float = 1.0) -> bytes:
        """Generate audio using OpenAI TTS"""
        response = self.client.audio.speech.create(
            model=self.model, voice=voice, input=text, speed=speed
        )
        return response.content

    def get_model_name(self) -> str:
        return f"OpenAI {self.model}"


class ElevenLabsAudioGenerator(BaseAudioGenerator):
    """ElevenLabs audio generator"""

    def __init__(self, api_key: str, model: str = "eleven_monolingual_v1"):
        self.api_key = api_key
        self.model = model

    def generate(self, text: str, voice: str = "21m00Tcm4TlvDq8ikWAM", speed: float = 1.0) -> bytes:
        """Generate audio using ElevenLabs"""
        # Implementation would call ElevenLabs API
        raise NotImplementedError("ElevenLabs integration requires API key and additional setup")

    def get_model_name(self) -> str:
        return f"ElevenLabs {self.model}"


class BaseVideoGenerator(ABC):
    """Base class for video generators"""

    @abstractmethod
    def generate(self, prompt: str, duration: int = 5) -> str:
        """Generate video from prompt"""
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """Get model name"""
        pass


class OpenAIVideoGenerator(BaseVideoGenerator):
    """OpenAI video generator (uses GPT for script generation)"""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        from openai import OpenAI

        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, duration: int = 5) -> str:
        """Generate video script using GPT"""
        system_prompt = f"""أنت مولد سكريبت فيديو احترافي.
        أنشئ سكريبت فيديو مدته {duration} ثواني بناءً على الوصف المُعطى.
        قدم وصفاً تفصيلياً للمشاهد والانتقالات والموسيقى."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content

    def get_model_name(self) -> str:
        return f"OpenAI {self.model}"


class RunwayMLVideoGenerator(BaseVideoGenerator):
    """Runway ML video generator"""

    def __init__(self, api_key: str, model: str = "gen-2"):
        self.api_key = api_key
        self.model = model

    def generate(self, prompt: str, duration: int = 5) -> str:
        """Generate video using Runway ML"""
        # Implementation would call Runway ML API
        raise NotImplementedError("Runway ML integration requires API key and setup")

    def get_model_name(self) -> str:
        return f"Runway ML {self.model}"


class ModelFactory:
    """Factory for creating generator instances"""

    IMAGE_MODELS = {
        "openai-dalle-3": OpenAIImageGenerator,
        "openai-dalle-2": lambda api_key: OpenAIImageGenerator(api_key, "dall-e-2"),  # type: ignore[misc]
        "stability-ai": StabilityAIImageGenerator,
    }

    AUDIO_MODELS = {
        "openai-tts-1": OpenAIAudioGenerator,
        "openai-tts-1-hd": lambda api_key: OpenAIAudioGenerator(api_key, "tts-1-hd"),  # type: ignore[misc]
        "elevenlabs": ElevenLabsAudioGenerator,
    }

    VIDEO_MODELS = {
        "openai-gpt-4": OpenAIVideoGenerator,
        "openai-gpt-3.5": lambda api_key: OpenAIVideoGenerator(api_key, "gpt-3.5-turbo"),  # type: ignore[misc]
        "runway-ml": RunwayMLVideoGenerator,
    }

    @staticmethod
    def create_image_generator(model_name: str, api_key: str) -> BaseImageGenerator:
        """
        Create image generator instance

        Args:
            model_name: Name of the model
            api_key: API key for the service

        Returns:
            Image generator instance

        Raises:
            ValueError: If model name is not supported
        """
        if model_name not in ModelFactory.IMAGE_MODELS:
            raise ValueError(
                f"Unsupported image model: {model_name}. "
                f"Available: {list(ModelFactory.IMAGE_MODELS.keys())}"
            )

        generator_class = ModelFactory.IMAGE_MODELS[model_name]
        return generator_class(api_key)

    @staticmethod
    def create_audio_generator(model_name: str, api_key: str) -> BaseAudioGenerator:
        """
        Create audio generator instance

        Args:
            model_name: Name of the model
            api_key: API key for the service

        Returns:
            Audio generator instance

        Raises:
            ValueError: If model name is not supported
        """
        if model_name not in ModelFactory.AUDIO_MODELS:
            raise ValueError(
                f"Unsupported audio model: {model_name}. "
                f"Available: {list(ModelFactory.AUDIO_MODELS.keys())}"
            )

        generator_class = ModelFactory.AUDIO_MODELS[model_name]
        return generator_class(api_key)

    @staticmethod
    def create_video_generator(model_name: str, api_key: str) -> BaseVideoGenerator:
        """
        Create video generator instance

        Args:
            model_name: Name of the model
            api_key: API key for the service

        Returns:
            Video generator instance

        Raises:
            ValueError: If model name is not supported
        """
        if model_name not in ModelFactory.VIDEO_MODELS:
            raise ValueError(
                f"Unsupported video model: {model_name}. "
                f"Available: {list(ModelFactory.VIDEO_MODELS.keys())}"
            )

        generator_class = ModelFactory.VIDEO_MODELS[model_name]
        return generator_class(api_key)

    @staticmethod
    def list_available_models() -> Dict[str, List[str]]:
        """
        List all available models

        Returns:
            Dictionary with model types and their available models
        """
        return {
            "image": list(ModelFactory.IMAGE_MODELS.keys()),
            "audio": list(ModelFactory.AUDIO_MODELS.keys()),
            "video": list(ModelFactory.VIDEO_MODELS.keys()),
        }

    @staticmethod
    def get_model_info(model_type: str, model_name: str) -> Dict[str, Any]:
        """
        Get information about a specific model

        Args:
            model_type: Type of model (image/audio/video)
            model_name: Name of the model

        Returns:
            Dictionary with model information
        """
        models_info = {
            "image": {
                "openai-dalle-3": {
                    "name": "DALL-E 3",
                    "provider": "OpenAI",
                    "quality": "High",
                    "speed": "Medium",
                    "cost": "$$",
                    "sizes": ["1024x1024", "1792x1024", "1024x1792"],
                },
                "openai-dalle-2": {
                    "name": "DALL-E 2",
                    "provider": "OpenAI",
                    "quality": "Good",
                    "speed": "Fast",
                    "cost": "$",
                    "sizes": ["1024x1024", "512x512", "256x256"],
                },
                "stability-ai": {
                    "name": "Stable Diffusion XL",
                    "provider": "Stability AI",
                    "quality": "High",
                    "speed": "Fast",
                    "cost": "$",
                    "sizes": ["1024x1024", "768x768", "512x512"],
                },
            },
            "audio": {
                "openai-tts-1": {
                    "name": "TTS 1",
                    "provider": "OpenAI",
                    "quality": "Good",
                    "speed": "Fast",
                    "cost": "$",
                    "voices": ["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
                },
                "openai-tts-1-hd": {
                    "name": "TTS 1 HD",
                    "provider": "OpenAI",
                    "quality": "High",
                    "speed": "Medium",
                    "cost": "$$",
                    "voices": ["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
                },
                "elevenlabs": {
                    "name": "ElevenLabs",
                    "provider": "ElevenLabs",
                    "quality": "Very High",
                    "speed": "Medium",
                    "cost": "$$$",
                    "voices": ["Custom voices available"],
                },
            },
            "video": {
                "openai-gpt-4": {
                    "name": "GPT-4 Video Script",
                    "provider": "OpenAI",
                    "quality": "High",
                    "speed": "Medium",
                    "cost": "$$",
                },
                "openai-gpt-3.5": {
                    "name": "GPT-3.5 Video Script",
                    "provider": "OpenAI",
                    "quality": "Good",
                    "speed": "Fast",
                    "cost": "$",
                },
                "runway-ml": {
                    "name": "Runway Gen-2",
                    "provider": "Runway ML",
                    "quality": "Very High",
                    "speed": "Slow",
                    "cost": "$$$",
                },
            },
        }

        return models_info.get(model_type, {}).get(
            model_name, {"name": model_name, "provider": "Unknown"}
        )  # type: ignore[return-value]
