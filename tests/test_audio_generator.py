"""Tests for AudioGenerator"""

import os
import tempfile
from unittest.mock import Mock, patch

import pytest
from sa.generators.audio_generator import AudioGenerator


@pytest.fixture
def audio_generator():
    """Create audio generator instance for testing"""
    return AudioGenerator(api_key="test_key")


@pytest.fixture
def audio_generator_no_key():
    """Create audio generator without API key"""
    return AudioGenerator()


@pytest.fixture
def temp_audio_file():
    """Create a temporary audio file for testing"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".mp3", delete=False) as f:
        f.write("fake audio data")
        yield f.name
    if os.path.exists(f.name):
        os.unlink(f.name)


class TestAudioGeneratorInit:
    """Test AudioGenerator initialization"""

    def test_audio_generator_init(self):
        """Test AudioGenerator initialization"""
        generator = AudioGenerator()
        assert generator is not None

    def test_init_with_api_key(self):
        """Test initialization with API key"""
        generator = AudioGenerator(api_key="test_key_123")
        assert generator.api_key == "test_key_123"

    def test_init_without_api_key(self):
        """Test initialization without API key"""
        with patch.dict(os.environ, {"ELEVENLABS_API_KEY": "env_key"}):
            generator = AudioGenerator()
            assert generator.api_key == "env_key"

    @patch("sa.generators.audio_generator.ELEVENLABS_AVAILABLE", False)
    def test_init_without_elevenlabs(self):
        """Test initialization when ElevenLabs is not available"""
        generator = AudioGenerator(api_key="test_key")
        assert generator.client is None


class TestGetAvailableVoices:
    """Test getting available voices"""

    def test_get_available_voices(self):
        """Test getting available voices"""
        generator = AudioGenerator()
        voices = generator.get_available_voices()

        assert len(voices) > 0
        assert isinstance(voices, list)

    def test_get_available_voices_without_client(self, audio_generator_no_key):
        """Test getting voices when client is not initialized"""
        voices = audio_generator_no_key.get_available_voices()

        assert "Adam" in voices
        assert "Bella" in voices
        assert isinstance(voices, list)

    @patch("sa.generators.audio_generator.ELEVENLABS_AVAILABLE", True)
    def test_get_available_voices_with_client(self, audio_generator):
        """Test getting voices with ElevenLabs client"""
        mock_voice = Mock()
        mock_voice.name = "TestVoice"
        mock_voices_response = Mock()
        mock_voices_response.voices = [mock_voice]

        if audio_generator.client:
            audio_generator.client.voices = Mock()
            audio_generator.client.voices.get_all = Mock(return_value=mock_voices_response)

            voices = audio_generator.get_available_voices()
            assert isinstance(voices, list)

    @patch("sa.generators.audio_generator.ELEVENLABS_AVAILABLE", True)
    def test_get_available_voices_error(self, audio_generator):
        """Test getting voices when API call fails"""
        if audio_generator.client:
            audio_generator.client.voices = Mock()
            audio_generator.client.voices.get_all = Mock(side_effect=Exception("API Error"))

        voices = audio_generator.get_available_voices()
        assert "Adam" in voices  # Should return fallback voices


class TestGenerateSpeech:
    """Test speech generation"""

    @patch("sa.generators.audio_generator.ELEVENLABS_AVAILABLE", False)
    @patch("sa.generators.audio_generator.AudioGenerator._fallback_tts")
    def test_generate_speech_fallback(self, mock_fallback, audio_generator_no_key):
        """Test speech generation using fallback"""
        mock_fallback.return_value = "output.mp3"

        result = audio_generator_no_key.generate_speech("Hello world", output_path="test.mp3")

        # Should be called with text, output_path, and progress_callback (None)
        assert mock_fallback.called
        assert result == "output.mp3"

    @patch("sa.generators.audio_generator.ELEVENLABS_AVAILABLE", True)
    def test_generate_speech_with_client(self, audio_generator):
        """Test speech generation with ElevenLabs client"""
        if audio_generator.client:
            mock_audio_data = [b"audio chunk 1", b"audio chunk 2"]
            audio_generator.client.text_to_speech = Mock()
            audio_generator.client.text_to_speech.convert = Mock(return_value=iter(mock_audio_data))

            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                output_path = f.name

            try:
                result = audio_generator.generate_speech("Test text", output_path=output_path)
                assert result == output_path
                assert os.path.exists(output_path)
            finally:
                if os.path.exists(output_path):
                    os.unlink(output_path)

    @patch("sa.generators.audio_generator.ELEVENLABS_AVAILABLE", True)
    @patch("sa.generators.audio_generator.AudioGenerator._fallback_tts")
    def test_generate_speech_error_fallback(self, mock_fallback, audio_generator):
        """Test fallback when speech generation fails"""
        if audio_generator.client:
            audio_generator.client.text_to_speech = Mock()
            audio_generator.client.text_to_speech.convert = Mock(side_effect=Exception("API Error"))

        mock_fallback.return_value = "fallback.mp3"

        audio_generator.generate_speech("Test", output_path="test.mp3")

        mock_fallback.assert_called_once()


class TestFallbackTTS:
    """Test fallback TTS"""

    def test_fallback_tts_exists(self, audio_generator):
        """Test that fallback TTS method exists"""
        assert hasattr(audio_generator, "_fallback_tts")
        assert callable(audio_generator._fallback_tts)


class TestAddBackgroundMusic:
    """Test background music mixing"""

    def test_add_background_music_method_exists(self, audio_generator):
        """Test that method exists"""
        assert hasattr(audio_generator, "add_background_music")
        assert callable(audio_generator.add_background_music)


class TestGenerateNarrationFromScript:
    """Test narration generation from script"""

    def test_generate_narration_method_exists(self, audio_generator):
        """Test that method exists"""
        assert hasattr(audio_generator, "generate_narration_from_script")
        assert callable(audio_generator.generate_narration_from_script)


class TestTextValidation:
    """Test text validation"""

    def test_validate_valid_text(self):
        """Test validation of valid text"""
        result = AudioGenerator.validate_text("This is a valid text for speech")
        assert result["valid"] is True
        assert len(result["issues"]) == 0

    def test_validate_empty_text(self):
        """Test validation of empty text"""
        result = AudioGenerator.validate_text("")
        assert result["valid"] is False
        assert "empty" in result["issues"][0].lower()

    def test_validate_short_text(self):
        """Test validation of too short text"""
        result = AudioGenerator.validate_text("Hi")
        assert result["valid"] is False
        assert "too short" in result["issues"][0].lower()

    def test_validate_long_text(self):
        """Test validation of too long text"""
        long_text = "A " * 3000
        result = AudioGenerator.validate_text(long_text)
        assert result["valid"] is False
        assert "too long" in result["issues"][0].lower()

    def test_validate_all_caps_suggestion(self):
        """Test suggestion for all caps text"""
        result = AudioGenerator.validate_text("THIS IS ALL CAPS TEXT")
        assert "suggestions" in result
        assert len(result["suggestions"]) > 0

    def test_validation_includes_metrics(self):
        """Test that validation includes text metrics"""
        result = AudioGenerator.validate_text("Hello world")
        assert "length" in result
        assert "word_count" in result
        assert result["word_count"] == 2


class TestCaching:
    """Test caching functionality"""

    def test_clear_cache(self, audio_generator):
        """Test cache clearing"""
        audio_generator._cache = {"key1": "value1", "key2": "value2"}
        cleared = audio_generator.clear_cache()

        assert cleared == 2
        assert len(audio_generator._cache) == 0

    def test_get_cache_size(self, audio_generator):
        """Test getting cache size"""
        audio_generator._cache = {"key1": "value1", "key2": "value2"}
        size = audio_generator.get_cache_size()

        assert size == 2

    @patch("sa.generators.audio_generator.ELEVENLABS_AVAILABLE", False)
    @patch("sa.generators.audio_generator.AudioGenerator._fallback_tts")
    def test_caching_works(self, mock_fallback, audio_generator):
        """Test that caching prevents duplicate API calls"""
        mock_fallback.return_value = "output.mp3"

        # Mock os.path.exists to return True for cached file
        with patch("os.path.exists", return_value=True):
            # First call - should generate and cache
            audio_generator.generate_speech("Test text", use_cache=True)
            call_count_1 = mock_fallback.call_count

            # Manually set cache to simulate successful caching
            cache_key = audio_generator._get_cache_key(
                "Test text", {"voice": "Adam", "model": "eleven_multilingual_v2"}
            )
            audio_generator._cache[cache_key] = "output.mp3"

            # Second call with same params - should use cache
            audio_generator.generate_speech("Test text", use_cache=True)
            call_count_2 = mock_fallback.call_count

            # Second call should not increase call count (used cache)
            assert call_count_2 == call_count_1
            assert audio_generator.stats["cached"] >= 1


class TestStatistics:
    """Test statistics tracking"""

    def test_get_statistics(self, audio_generator):
        """Test getting statistics"""
        stats = audio_generator.get_statistics()

        assert "generated" in stats
        assert "cached" in stats
        assert "failed" in stats
        assert "fallback_used" in stats
        assert isinstance(stats, dict)

    def test_statistics_increment_on_failure(self, audio_generator):
        """Test that statistics increment on failure"""
        initial_stats = audio_generator.get_statistics()
        audio_generator.generate_speech("", use_cache=False)  # Invalid text
        new_stats = audio_generator.get_statistics()

        assert new_stats["failed"] == initial_stats["failed"] + 1


class TestProgressCallback:
    """Test progress callback functionality"""

    @patch("sa.generators.audio_generator.ELEVENLABS_AVAILABLE", False)
    @patch("sa.generators.audio_generator.AudioGenerator._fallback_tts")
    def test_progress_callback_called(self, mock_fallback, audio_generator):
        """Test that progress callback is called"""
        mock_fallback.return_value = "output.mp3"
        progress_messages = []

        def callback(msg):
            progress_messages.append(msg)

        audio_generator.generate_speech("Test text", use_cache=False, progress_callback=callback)

        assert len(progress_messages) > 0


class TestAddBackgroundMusicValidation:
    """Test background music validation"""

    def test_add_background_music_invalid_voice_path(self, audio_generator):
        """Test with non-existent voice file"""
        result = audio_generator.add_background_music("nonexistent_voice.mp3", "music.mp3")

        assert result is None
        assert audio_generator.stats["failed"] >= 1

    def test_add_background_music_invalid_music_path(self, audio_generator, temp_audio_file):
        """Test with non-existent music file"""
        result = audio_generator.add_background_music(temp_audio_file, "nonexistent_music.mp3")

        assert result is None

    def test_add_background_music_invalid_volume(self, audio_generator, temp_audio_file):
        """Test with invalid volume"""
        result = audio_generator.add_background_music(
            temp_audio_file, temp_audio_file, music_volume=2.0  # Invalid: should be 0.0-1.0
        )

        assert result is None


class TestGenerateNarrationValidation:
    """Test narration generation validation"""

    def test_generate_narration_empty_segments(self, audio_generator):
        """Test narration with empty segments list"""
        result = audio_generator.generate_narration_from_script([])

        assert result is None
        assert audio_generator.stats["failed"] >= 1

    @patch("sa.generators.audio_generator.ELEVENLABS_AVAILABLE", False)
    @patch("sa.generators.audio_generator.AudioGenerator._fallback_tts")
    def test_generate_narration_with_progress(self, mock_fallback, audio_generator):
        """Test narration with progress callback"""
        mock_fallback.return_value = "segment.mp3"
        progress_messages = []

        def callback(msg):
            progress_messages.append(msg)

        segments = [
            {"text": "First segment", "voice": "Adam"},
            {"text": "Second segment", "voice": "Bella"},
        ]

        # This will likely fail without real audio files, but we test the callback
        audio_generator.generate_narration_from_script(segments, progress_callback=callback)

        assert len(progress_messages) > 0


class TestInvalidTextGeneration:
    """Test speech generation with invalid inputs"""

    def test_generate_with_empty_text(self, audio_generator):
        """Test generation with empty text"""
        result = audio_generator.generate_speech("", use_cache=False)

        assert result is None
        assert audio_generator.stats["failed"] >= 1

    def test_generate_with_very_short_text(self, audio_generator):
        """Test generation with very short text"""
        result = audio_generator.generate_speech("Hi", use_cache=False)

        assert result is None
