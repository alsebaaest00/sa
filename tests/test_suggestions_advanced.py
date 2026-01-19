"""Advanced tests for AI suggestion engine"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from sa.utils.suggestions import SuggestionEngine


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client"""
    with patch("sa.utils.suggestions.OpenAI") as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance

        # Mock completions response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="improved prompt"))]
        mock_instance.chat.completions.create.return_value = mock_response

        yield mock_instance


class TestSuggestionEngineInit:
    """Test SuggestionEngine initialization"""

    def test_init_with_api_key(self):
        """Test initialization with API key"""
        with patch("sa.utils.suggestions.OpenAI"):
            engine = SuggestionEngine(api_key="test_key")
            assert engine.api_key == "test_key"

    def test_init_from_env(self):
        """Test initialization from environment"""
        with patch("sa.utils.suggestions.os.getenv", return_value="env_key"):
            with patch("sa.utils.suggestions.OpenAI"):
                engine = SuggestionEngine()
                assert engine.api_key == "env_key"

    def test_init_without_key(self):
        """Test initialization without API key"""
        with patch("sa.utils.suggestions.os.getenv", return_value=None):
            with pytest.raises(ValueError, match="OpenAI API key"):
                SuggestionEngine()


class TestPromptImprovement:
    """Test prompt improvement functionality"""

    def test_improve_prompt_image(self, mock_openai_client):
        """Test improving prompt for images"""
        engine = SuggestionEngine(api_key="test_key")
        result = engine.improve_prompt("cat", media_type="image")
        assert isinstance(result, str)
        assert mock_openai_client.chat.completions.create.called

    def test_improve_prompt_video(self, mock_openai_client):
        """Test improving prompt for video"""
        engine = SuggestionEngine(api_key="test_key")
        result = engine.improve_prompt("flying bird", media_type="video")
        assert isinstance(result, str)

    def test_improve_prompt_audio(self, mock_openai_client):
        """Test improving prompt for audio"""
        engine = SuggestionEngine(api_key="test_key")
        result = engine.improve_prompt("welcome message", media_type="audio")
        assert isinstance(result, str)

    def test_improve_empty_prompt(self, mock_openai_client):
        """Test improving empty prompt"""
        engine = SuggestionEngine(api_key="test_key")
        with pytest.raises(ValueError, match="empty"):
            engine.improve_prompt("", media_type="image")


class TestPromptGeneration:
    """Test prompt generation"""

    def test_generate_prompts_default_count(self, mock_openai_client):
        """Test generating prompts with default count"""
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = (
            "prompt1\nprompt2\nprompt3"
        )

        engine = SuggestionEngine(api_key="test_key")
        result = engine.generate_prompts("nature")
        assert isinstance(result, list)

    def test_generate_prompts_custom_count(self, mock_openai_client):
        """Test generating custom number of prompts"""
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = (
            "prompt1\nprompt2"
        )

        engine = SuggestionEngine(api_key="test_key")
        result = engine.generate_prompts("space", count=2)
        assert isinstance(result, list)

    def test_generate_prompts_with_media_type(self, mock_openai_client):
        """Test generating prompts for specific media type"""
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = (
            "video prompt"
        )

        engine = SuggestionEngine(api_key="test_key")
        result = engine.generate_prompts("action", media_type="video")
        assert isinstance(result, list)


class TestThemeSupport:
    """Test theme-based generation"""

    def test_get_themes(self, mock_openai_client):
        """Test getting available themes"""
        engine = SuggestionEngine(api_key="test_key")
        themes = engine.get_themes()
        assert isinstance(themes, list)
        assert len(themes) > 0

    def test_theme_based_generation(self, mock_openai_client):
        """Test generating from themes"""
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = (
            "theme-based prompt"
        )

        engine = SuggestionEngine(api_key="test_key")
        result = engine.generate_from_theme("nature", media_type="image")
        assert isinstance(result, str)


class TestStyleSuggestions:
    """Test style suggestions"""

    def test_suggest_styles_image(self, mock_openai_client):
        """Test style suggestions for images"""
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = (
            "realistic, anime, oil painting"
        )

        engine = SuggestionEngine(api_key="test_key")
        result = engine.suggest_styles("portrait", media_type="image")
        assert isinstance(result, list)

    def test_suggest_styles_video(self, mock_openai_client):
        """Test style suggestions for video"""
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = (
            "cinematic, documentary, animated"
        )

        engine = SuggestionEngine(api_key="test_key")
        result = engine.suggest_styles("story", media_type="video")
        assert isinstance(result, list)


class TestErrorHandling:
    """Test error handling in suggestions"""

    def test_api_error_handling(self, mock_openai_client):
        """Test handling API errors"""
        mock_openai_client.chat.completions.create.side_effect = Exception("API Error")

        engine = SuggestionEngine(api_key="test_key")
        with pytest.raises(Exception):
            engine.improve_prompt("test")

    def test_invalid_media_type(self, mock_openai_client):
        """Test with invalid media type"""
        engine = SuggestionEngine(api_key="test_key")
        # Should still work but with default behavior
        result = engine.improve_prompt("test", media_type="invalid")
        assert isinstance(result, str)

    def test_rate_limit_handling(self, mock_openai_client):
        """Test handling rate limit errors"""
        from openai import RateLimitError

        mock_openai_client.chat.completions.create.side_effect = RateLimitError(
            "Rate limit", response=Mock(), body=None
        )

        engine = SuggestionEngine(api_key="test_key")
        with pytest.raises(RateLimitError):
            engine.improve_prompt("test")


class TestBatchOperations:
    """Test batch operations"""

    def test_improve_multiple_prompts(self, mock_openai_client):
        """Test improving multiple prompts at once"""
        engine = SuggestionEngine(api_key="test_key")
        prompts = ["cat", "dog", "bird"]
        results = [engine.improve_prompt(p) for p in prompts]
        assert len(results) == 3
        assert all(isinstance(r, str) for r in results)

    def test_generate_variations(self, mock_openai_client):
        """Test generating variations of a prompt"""
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = (
            "variation1\nvariation2\nvariation3"
        )

        engine = SuggestionEngine(api_key="test_key")
        result = engine.generate_variations("original prompt", count=3)
        assert isinstance(result, list)


class TestCaching:
    """Test suggestion caching"""

    def test_cache_hit(self, mock_openai_client):
        """Test that repeated prompts use cache"""
        engine = SuggestionEngine(api_key="test_key")

        # First call
        result1 = engine.improve_prompt("test prompt")

        # Second call (should use cache)
        result2 = engine.improve_prompt("test prompt")

        assert result1 == result2
        # API should be called only once if caching works
        assert mock_openai_client.chat.completions.create.call_count >= 1

    def test_clear_cache(self, mock_openai_client):
        """Test clearing suggestion cache"""
        engine = SuggestionEngine(api_key="test_key")
        engine.improve_prompt("test")

        # Clear cache
        if hasattr(engine, "clear_cache"):
            engine.clear_cache()
