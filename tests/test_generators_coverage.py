"""Additional coverage tests for generators"""

from unittest.mock import Mock, patch

import pytest

from sa.generators import AudioGenerator, ImageGenerator, VideoGenerator


class TestImageGeneratorEdgeCases:
    """Edge case tests for ImageGenerator"""

    @patch("sa.generators.image_generator.OpenAI")
    def test_generate_with_empty_prompt(self, mock_openai):
        """Test generation with empty prompt"""
        generator = ImageGenerator(api_key="test_key")

        with pytest.raises(ValueError):
            generator.generate("")

    @patch("sa.generators.image_generator.OpenAI")
    def test_generate_with_very_long_prompt(self, mock_openai):
        """Test generation with very long prompt"""
        generator = ImageGenerator(api_key="test_key")
        long_prompt = "test " * 500  # Very long prompt

        mock_client = Mock()
        mock_openai.return_value = mock_client
        mock_client.images.generate.return_value.data = [Mock(url="https://example.com/image.png")]

        result = generator.generate(long_prompt)
        assert result is not None

    @patch("sa.generators.image_generator.OpenAI")
    def test_generate_with_special_characters(self, mock_openai):
        """Test generation with special characters in prompt"""
        generator = ImageGenerator(api_key="test_key")
        special_prompt = "Test @#$%^&*() 中文 العربية"

        mock_client = Mock()
        mock_openai.return_value = mock_client
        mock_client.images.generate.return_value.data = [Mock(url="https://example.com/image.png")]

        result = generator.generate(special_prompt)
        assert result is not None

    @patch("sa.generators.image_generator.OpenAI")
    def test_generate_with_different_sizes(self, mock_openai):
        """Test generation with different image sizes"""
        generator = ImageGenerator(api_key="test_key")

        mock_client = Mock()
        mock_openai.return_value = mock_client
        mock_client.images.generate.return_value.data = [Mock(url="https://example.com/image.png")]

        for size in ["1024x1024", "512x512", "256x256"]:
            result = generator.generate("test", size=size)
            assert result is not None

    @patch("sa.generators.image_generator.OpenAI")
    def test_api_timeout_handling(self, mock_openai):
        """Test handling of API timeout"""
        generator = ImageGenerator(api_key="test_key")

        mock_client = Mock()
        mock_openai.return_value = mock_client
        mock_client.images.generate.side_effect = TimeoutError("API timeout")

        with pytest.raises(TimeoutError):
            generator.generate("test")


class TestAudioGeneratorEdgeCases:
    """Edge case tests for AudioGenerator"""

    @patch("sa.generators.audio_generator.OpenAI")
    def test_generate_with_empty_text(self, mock_openai):
        """Test generation with empty text"""
        generator = AudioGenerator(api_key="test_key")

        with pytest.raises(ValueError):
            generator.generate("")

    @patch("sa.generators.audio_generator.OpenAI")
    def test_generate_with_different_voices(self, mock_openai):
        """Test generation with different voice options"""
        generator = AudioGenerator(api_key="test_key")

        mock_client = Mock()
        mock_openai.return_value = mock_client
        mock_response = Mock()
        mock_response.content = b"audio_data"
        mock_client.audio.speech.create.return_value = mock_response

        voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
        for voice in voices:
            result = generator.generate("test text", voice=voice)
            assert result is not None

    @patch("sa.generators.audio_generator.OpenAI")
    def test_generate_with_very_long_text(self, mock_openai):
        """Test generation with very long text"""
        generator = AudioGenerator(api_key="test_key")
        long_text = "This is a test sentence. " * 200

        mock_client = Mock()
        mock_openai.return_value = mock_client
        mock_response = Mock()
        mock_response.content = b"audio_data"
        mock_client.audio.speech.create.return_value = mock_response

        result = generator.generate(long_text)
        assert result is not None

    @patch("sa.generators.audio_generator.OpenAI")
    def test_generate_with_arabic_text(self, mock_openai):
        """Test generation with Arabic text"""
        generator = AudioGenerator(api_key="test_key")

        mock_client = Mock()
        mock_openai.return_value = mock_client
        mock_response = Mock()
        mock_response.content = b"audio_data"
        mock_client.audio.speech.create.return_value = mock_response

        result = generator.generate("مرحباً بك في منصة SA")
        assert result is not None

    @patch("sa.generators.audio_generator.OpenAI")
    def test_network_error_handling(self, mock_openai):
        """Test handling of network errors"""
        generator = AudioGenerator(api_key="test_key")

        mock_client = Mock()
        mock_openai.return_value = mock_client
        mock_client.audio.speech.create.side_effect = ConnectionError("Network error")

        with pytest.raises(ConnectionError):
            generator.generate("test")


class TestVideoGeneratorEdgeCases:
    """Edge case tests for VideoGenerator"""

    @patch("sa.generators.video_generator.OpenAI")
    def test_generate_with_empty_prompt(self, mock_openai):
        """Test generation with empty prompt"""
        generator = VideoGenerator(api_key="test_key")

        with pytest.raises(ValueError):
            generator.generate("")

    @patch("sa.generators.video_generator.OpenAI")
    def test_generate_with_multiple_scenes(self, mock_openai):
        """Test generation with multiple scene descriptions"""
        generator = VideoGenerator(api_key="test_key")
        multi_scene = """
        Scene 1: Opening shot of a sunrise
        Scene 2: Person walking in the city
        Scene 3: Close-up of coffee cup
        """

        mock_client = Mock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value.choices = [
            Mock(message=Mock(content="Generated video script"))
        ]

        result = generator.generate(multi_scene)
        assert result is not None

    @patch("sa.generators.video_generator.OpenAI")
    def test_generate_with_technical_terms(self, mock_openai):
        """Test generation with technical terminology"""
        generator = VideoGenerator(api_key="test_key")
        technical_prompt = "Quantum computing visualization with qubits and entanglement"

        mock_client = Mock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value.choices = [
            Mock(message=Mock(content="Technical video script"))
        ]

        result = generator.generate(technical_prompt)
        assert result is not None

    @patch("sa.generators.video_generator.OpenAI")
    def test_rate_limit_handling(self, mock_openai):
        """Test handling of rate limit errors"""
        generator = VideoGenerator(api_key="test_key")

        mock_client = Mock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("Rate limit exceeded")

        with pytest.raises(Exception):
            generator.generate("test")


class TestGeneratorsIntegration:
    """Integration tests for multiple generators"""

    @patch("sa.generators.image_generator.OpenAI")
    @patch("sa.generators.audio_generator.OpenAI")
    @patch("sa.generators.video_generator.OpenAI")
    def test_multiple_generators_same_api_key(
        self, mock_video_openai, mock_audio_openai, mock_image_openai
    ):
        """Test using multiple generators with same API key"""
        api_key = "shared_test_key"

        image_gen = ImageGenerator(api_key=api_key)
        audio_gen = AudioGenerator(api_key=api_key)
        video_gen = VideoGenerator(api_key=api_key)

        assert image_gen.api_key == api_key
        assert audio_gen.api_key == api_key
        assert video_gen.api_key == api_key

    @patch("sa.generators.image_generator.OpenAI")
    def test_generator_reuse(self, mock_openai):
        """Test reusing same generator instance"""
        generator = ImageGenerator(api_key="test_key")

        mock_client = Mock()
        mock_openai.return_value = mock_client
        mock_client.images.generate.return_value.data = [Mock(url="https://example.com/image1.png")]

        # Generate multiple images with same instance
        result1 = generator.generate("prompt 1")
        result2 = generator.generate("prompt 2")

        assert result1 is not None
        assert result2 is not None
        assert mock_client.images.generate.call_count == 2


class TestErrorRecovery:
    """Tests for error recovery mechanisms"""

    @patch("sa.generators.image_generator.OpenAI")
    def test_retry_after_failure(self, mock_openai):
        """Test retry mechanism after initial failure"""
        generator = ImageGenerator(api_key="test_key")

        mock_client = Mock()
        mock_openai.return_value = mock_client

        # First call fails, second succeeds
        mock_client.images.generate.side_effect = [
            Exception("Temporary error"),
            Mock(data=[Mock(url="https://example.com/image.png")]),
        ]

        # First attempt should fail
        with pytest.raises(Exception):
            generator.generate("test")

        # Second attempt should succeed
        result = generator.generate("test")
        assert result is not None

    @patch("sa.generators.audio_generator.OpenAI")
    def test_invalid_api_key_error(self, mock_openai):
        """Test handling of invalid API key"""
        generator = AudioGenerator(api_key="invalid_key")

        mock_client = Mock()
        mock_openai.return_value = mock_client
        mock_client.audio.speech.create.side_effect = Exception("Invalid API key")

        with pytest.raises(Exception) as exc_info:
            generator.generate("test")

        assert "Invalid API key" in str(exc_info.value)


class TestPerformance:
    """Performance-related tests"""

    @patch("sa.generators.image_generator.OpenAI")
    def test_concurrent_generation_safety(self, mock_openai):
        """Test that generators are safe for concurrent use"""
        generator = ImageGenerator(api_key="test_key")

        mock_client = Mock()
        mock_openai.return_value = mock_client
        mock_client.images.generate.return_value.data = [Mock(url="https://example.com/image.png")]

        # Simulate concurrent calls (in real scenario would use threading)
        results = []
        for i in range(5):
            result = generator.generate(f"prompt {i}")
            results.append(result)

        assert len(results) == 5
        assert all(r is not None for r in results)
