"""Tests for SuggestionEngine"""

import os
from unittest.mock import patch

import pytest
from sa.utils.suggestions import SuggestionEngine


@pytest.fixture
def suggestion_engine():
    """Create suggestion engine instance for testing"""
    return SuggestionEngine(api_key="test_key")


@pytest.fixture
def suggestion_engine_no_key():
    """Create suggestion engine without API key"""
    return SuggestionEngine()


class TestSuggestionEngineInit:
    """Test SuggestionEngine initialization"""

    def test_init_with_api_key(self):
        """Test initialization with API key"""
        engine = SuggestionEngine(api_key="test_key_123")
        assert engine.api_key == "test_key_123"

    def test_init_without_api_key(self):
        """Test initialization without API key"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "env_key"}):
            engine = SuggestionEngine()
            assert engine.api_key == "env_key"


class TestImprovePrompt:
    """Test prompt improvement"""

    def test_improve_prompt_exists(self, suggestion_engine):
        """Test that method exists"""
        assert hasattr(suggestion_engine, "improve_prompt")
        assert callable(suggestion_engine.improve_prompt)

    def test_improve_prompt_no_client(self, suggestion_engine_no_key):
        """Test improvement without client"""
        suggestion_engine_no_key.client = None
        result = suggestion_engine_no_key.improve_prompt("Test prompt", "image")
        assert "Test prompt" in result


class TestGenerateVariations:
    """Test prompt variations generation"""

    def test_generate_variations_exists(self, suggestion_engine):
        """Test that method exists"""
        assert hasattr(suggestion_engine, "generate_variations")
        assert callable(suggestion_engine.generate_variations)

    def test_generate_variations_no_client(self, suggestion_engine_no_key):
        """Test variations without client"""
        suggestion_engine_no_key.client = None
        result = suggestion_engine_no_key.generate_variations("Test")
        assert isinstance(result, list)


class TestGenerateScriptFromIdea:
    """Test script generation from idea"""

    def test_generate_script_exists(self, suggestion_engine):
        """Test that method exists"""
        assert hasattr(suggestion_engine, "generate_script_from_idea")
        assert callable(suggestion_engine.generate_script_from_idea)

    def test_generate_script_no_client(self, suggestion_engine_no_key):
        """Test script generation without client"""
        suggestion_engine_no_key.client = None
        result = suggestion_engine_no_key.generate_script_from_idea("Test idea", num_scenes=3)
        assert isinstance(result, list)


class TestFallbackImprove:
    """Test fallback improvement method"""

    def test_fallback_improve_image(self, suggestion_engine):
        """Test fallback for image prompts"""
        result = suggestion_engine._fallback_improve("A sunset", "image")

        assert "A sunset" in result
        assert "high quality" in result or "detailed" in result

    def test_fallback_improve_video(self, suggestion_engine):
        """Test fallback for video prompts"""
        result = suggestion_engine._fallback_improve("A car", "video")

        assert "A car" in result
        assert "cinematic" in result or "smooth" in result

    def test_fallback_improve_audio(self, suggestion_engine):
        """Test fallback for audio prompts"""
        result = suggestion_engine._fallback_improve("A speech", "audio")

        assert "A speech" in result

    def test_fallback_improve_empty(self, suggestion_engine):
        """Test fallback with empty prompt"""
        result = suggestion_engine._fallback_improve("", "image")

        assert len(result) > 0


class TestFallbackVariations:
    """Test fallback variations method"""

    def test_fallback_variations(self, suggestion_engine):
        """Test fallback variations generation"""
        result = suggestion_engine._fallback_variations("Original prompt", count=3)

        assert isinstance(result, list)
        assert len(result) == 3
        for variation in result:
            assert "Original prompt" in variation

    def test_fallback_variations_custom_count(self, suggestion_engine):
        """Test fallback with custom count"""
        result = suggestion_engine._fallback_variations("Test", count=5)

        assert len(result) == 5


class TestFallbackScript:
    """Test fallback script generation"""

    def test_fallback_script_exists(self, suggestion_engine):
        """Test that method exists"""
        assert hasattr(suggestion_engine, "_fallback_script")
        assert callable(suggestion_engine._fallback_script)


class TestIntegration:
    """Integration tests"""

    def test_complete_workflow(self, suggestion_engine):
        """Test complete suggestion workflow"""
        assert suggestion_engine is not None
        assert suggestion_engine.api_key == "test_key"

    def test_clear_cache(self, suggestion_engine):
        """Test cache clearing"""
        suggestion_engine._cache["test"] = "value"
        assert suggestion_engine.get_cache_size() > 0
        suggestion_engine.clear_cache()
        assert suggestion_engine.get_cache_size() == 0

    def test_cache_size(self, suggestion_engine):
        """Test getting cache size"""
        initial_size = suggestion_engine.get_cache_size()
        suggestion_engine._cache["key1"] = "value1"
        suggestion_engine._cache["key2"] = "value2"
        assert suggestion_engine.get_cache_size() == initial_size + 2


class TestValidatePrompt:
    """Test prompt validation"""

    def test_validate_valid_prompt(self, suggestion_engine):
        """Test validating a good prompt"""
        result = suggestion_engine.validate_prompt("A beautiful sunset over the mountains")
        assert result["valid"] is True
        assert result["word_count"] > 5
        assert result["has_details"] is True

    def test_validate_short_prompt(self, suggestion_engine):
        """Test validating a short prompt"""
        result = suggestion_engine.validate_prompt("cat")
        assert result["valid"] is True
        assert "short" in str(result["suggestions"]).lower()

    def test_validate_empty_prompt(self, suggestion_engine):
        """Test validating empty prompt"""
        result = suggestion_engine.validate_prompt("")
        assert result["valid"] is False

    def test_validate_long_prompt(self, suggestion_engine):
        """Test validating very long prompt"""
        long_prompt = "word " * 200
        result = suggestion_engine.validate_prompt(long_prompt)
        assert result["length"] > 500

    def test_validate_prompt_details(self, suggestion_engine):
        """Test prompt with good details"""
        prompt = "A cinematic shot of a cat playing with a ball in a sunny garden"
        result = suggestion_engine.validate_prompt(prompt)
        assert result["has_details"] is True
        assert result["word_count"] >= 5
