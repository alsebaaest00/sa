"""Tests for multi-model AI support"""

import pytest

from sa.utils.ai_models import (
    ModelFactory,
    OpenAIAudioGenerator,
    OpenAIImageGenerator,
    OpenAIVideoGenerator,
)


class TestModelFactory:
    """Tests for ModelFactory"""

    def test_list_available_models(self):
        """Test listing all available models"""
        models = ModelFactory.list_available_models()

        assert "image" in models
        assert "audio" in models
        assert "video" in models

        assert "openai-dalle-3" in models["image"]
        assert "openai-tts-1" in models["audio"]
        assert "openai-gpt-4" in models["video"]

    def test_create_image_generator_dalle3(self):
        """Test creating DALL-E 3 image generator"""
        generator = ModelFactory.create_image_generator("openai-dalle-3", "test_key")

        assert isinstance(generator, OpenAIImageGenerator)
        assert generator.get_model_name() == "OpenAI dall-e-3"

    def test_create_image_generator_dalle2(self):
        """Test creating DALL-E 2 image generator"""
        generator = ModelFactory.create_image_generator("openai-dalle-2", "test_key")

        assert isinstance(generator, OpenAIImageGenerator)
        assert generator.get_model_name() == "OpenAI dall-e-2"

    def test_create_image_generator_invalid(self):
        """Test creating image generator with invalid model"""
        with pytest.raises(ValueError) as exc_info:
            ModelFactory.create_image_generator("invalid-model", "test_key")

        assert "Unsupported image model" in str(exc_info.value)

    def test_create_audio_generator_tts1(self):
        """Test creating TTS-1 audio generator"""
        generator = ModelFactory.create_audio_generator("openai-tts-1", "test_key")

        assert isinstance(generator, OpenAIAudioGenerator)
        assert generator.get_model_name() == "OpenAI tts-1"

    def test_create_audio_generator_tts1_hd(self):
        """Test creating TTS-1-HD audio generator"""
        generator = ModelFactory.create_audio_generator("openai-tts-1-hd", "test_key")

        assert isinstance(generator, OpenAIAudioGenerator)
        assert generator.get_model_name() == "OpenAI tts-1-hd"

    def test_create_audio_generator_invalid(self):
        """Test creating audio generator with invalid model"""
        with pytest.raises(ValueError) as exc_info:
            ModelFactory.create_audio_generator("invalid-model", "test_key")

        assert "Unsupported audio model" in str(exc_info.value)

    def test_create_video_generator_gpt4(self):
        """Test creating GPT-4 video generator"""
        generator = ModelFactory.create_video_generator("openai-gpt-4", "test_key")

        assert isinstance(generator, OpenAIVideoGenerator)
        assert generator.get_model_name() == "OpenAI gpt-4"

    def test_create_video_generator_gpt35(self):
        """Test creating GPT-3.5 video generator"""
        generator = ModelFactory.create_video_generator("openai-gpt-3.5", "test_key")

        assert isinstance(generator, OpenAIVideoGenerator)
        assert generator.get_model_name() == "OpenAI gpt-3.5-turbo"

    def test_create_video_generator_invalid(self):
        """Test creating video generator with invalid model"""
        with pytest.raises(ValueError) as exc_info:
            ModelFactory.create_video_generator("invalid-model", "test_key")

        assert "Unsupported video model" in str(exc_info.value)

    def test_get_model_info_dalle3(self):
        """Test getting model info for DALL-E 3"""
        info = ModelFactory.get_model_info("image", "openai-dalle-3")

        assert info["name"] == "DALL-E 3"
        assert info["provider"] == "OpenAI"
        assert info["quality"] == "High"
        assert "1024x1024" in info["sizes"]

    def test_get_model_info_tts1_hd(self):
        """Test getting model info for TTS-1-HD"""
        info = ModelFactory.get_model_info("audio", "openai-tts-1-hd")

        assert info["name"] == "TTS 1 HD"
        assert info["provider"] == "OpenAI"
        assert info["quality"] == "High"
        assert "alloy" in info["voices"]

    def test_get_model_info_runway(self):
        """Test getting model info for Runway ML"""
        info = ModelFactory.get_model_info("video", "runway-ml")

        assert info["name"] == "Runway Gen-2"
        assert info["provider"] == "Runway ML"
        assert info["quality"] == "Very High"

    def test_get_model_info_invalid(self):
        """Test getting model info for nonexistent model"""
        info = ModelFactory.get_model_info("image", "nonexistent")

        assert info["name"] == "nonexistent"
        assert info["provider"] == "Unknown"


class TestOpenAIImageGenerator:
    """Tests for OpenAIImageGenerator"""

    def test_initialization(self):
        """Test OpenAI image generator initialization"""
        generator = OpenAIImageGenerator(api_key="test_key", model="dall-e-3")

        assert generator.api_key == "test_key"
        assert generator.model == "dall-e-3"
        assert generator.get_model_name() == "OpenAI dall-e-3"

    def test_model_name_dalle2(self):
        """Test model name for DALL-E 2"""
        generator = OpenAIImageGenerator(api_key="test_key", model="dall-e-2")

        assert generator.get_model_name() == "OpenAI dall-e-2"


class TestOpenAIAudioGenerator:
    """Tests for OpenAIAudioGenerator"""

    def test_initialization(self):
        """Test OpenAI audio generator initialization"""
        generator = OpenAIAudioGenerator(api_key="test_key", model="tts-1")

        assert generator.api_key == "test_key"
        assert generator.model == "tts-1"
        assert generator.get_model_name() == "OpenAI tts-1"

    def test_model_name_tts1_hd(self):
        """Test model name for TTS-1-HD"""
        generator = OpenAIAudioGenerator(api_key="test_key", model="tts-1-hd")

        assert generator.get_model_name() == "OpenAI tts-1-hd"


class TestOpenAIVideoGenerator:
    """Tests for OpenAIVideoGenerator"""

    def test_initialization(self):
        """Test OpenAI video generator initialization"""
        generator = OpenAIVideoGenerator(api_key="test_key", model="gpt-4")

        assert generator.api_key == "test_key"
        assert generator.model == "gpt-4"
        assert generator.get_model_name() == "OpenAI gpt-4"

    def test_model_name_gpt35(self):
        """Test model name for GPT-3.5"""
        generator = OpenAIVideoGenerator(api_key="test_key", model="gpt-3.5-turbo")

        assert generator.get_model_name() == "OpenAI gpt-3.5-turbo"


class TestModelComparison:
    """Tests for comparing different models"""

    def test_compare_image_models_quality(self):
        """Test comparing image models by quality"""
        dalle3_info = ModelFactory.get_model_info("image", "openai-dalle-3")
        dalle2_info = ModelFactory.get_model_info("image", "openai-dalle-2")

        assert dalle3_info["quality"] == "High"
        assert dalle2_info["quality"] == "Good"

    def test_compare_audio_models_cost(self):
        """Test comparing audio models by cost"""
        tts1_info = ModelFactory.get_model_info("audio", "openai-tts-1")
        tts1_hd_info = ModelFactory.get_model_info("audio", "openai-tts-1-hd")

        assert tts1_info["cost"] == "$"
        assert tts1_hd_info["cost"] == "$$"

    def test_compare_video_models_speed(self):
        """Test comparing video models by speed"""
        gpt4_info = ModelFactory.get_model_info("video", "openai-gpt-4")
        gpt35_info = ModelFactory.get_model_info("video", "openai-gpt-3.5")

        assert gpt4_info["speed"] == "Medium"
        assert gpt35_info["speed"] == "Fast"


class TestModelAvailability:
    """Tests for checking model availability"""

    def test_all_image_models_available(self):
        """Test that all declared image models are available"""
        models = ModelFactory.list_available_models()["image"]

        assert len(models) >= 3
        assert "openai-dalle-3" in models
        assert "openai-dalle-2" in models
        assert "stability-ai" in models

    def test_all_audio_models_available(self):
        """Test that all declared audio models are available"""
        models = ModelFactory.list_available_models()["audio"]

        assert len(models) >= 3
        assert "openai-tts-1" in models
        assert "openai-tts-1-hd" in models
        assert "elevenlabs" in models

    def test_all_video_models_available(self):
        """Test that all declared video models are available"""
        models = ModelFactory.list_available_models()["video"]

        assert len(models) >= 3
        assert "openai-gpt-4" in models
        assert "openai-gpt-3.5" in models
        assert "runway-ml" in models


class TestModelInformation:
    """Tests for model information completeness"""

    def test_all_image_models_have_info(self):
        """Test that all image models have complete information"""
        models = ModelFactory.list_available_models()["image"]

        for model in models:
            info = ModelFactory.get_model_info("image", model)
            assert "name" in info
            assert "provider" in info

    def test_all_audio_models_have_info(self):
        """Test that all audio models have complete information"""
        models = ModelFactory.list_available_models()["audio"]

        for model in models:
            info = ModelFactory.get_model_info("audio", model)
            assert "name" in info
            assert "provider" in info

    def test_all_video_models_have_info(self):
        """Test that all video models have complete information"""
        models = ModelFactory.list_available_models()["video"]

        for model in models:
            info = ModelFactory.get_model_info("video", model)
            assert "name" in info
            assert "provider" in info
