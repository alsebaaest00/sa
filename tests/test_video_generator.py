"""Tests for video generator module"""

import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest
from sa.generators.video_generator import VideoGenerator


@pytest.fixture
def video_generator():
    """Create video generator instance for testing"""
    return VideoGenerator(api_key="test_key")


@pytest.fixture
def temp_image_file():
    """Create a temporary image file for testing"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".png", delete=False) as f:
        f.write("fake image data")
        yield f.name
    if os.path.exists(f.name):
        os.unlink(f.name)


@pytest.fixture
def temp_video_file():
    """Create a temporary video file for testing"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".mp4", delete=False) as f:
        f.write("fake video data")
        yield f.name
    if os.path.exists(f.name):
        os.unlink(f.name)


@pytest.fixture
def temp_audio_file():
    """Create a temporary audio file for testing"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".mp3", delete=False) as f:
        f.write("fake audio data")
        yield f.name
    if os.path.exists(f.name):
        os.unlink(f.name)


class TestVideoGeneratorInit:
    """Test VideoGenerator initialization"""

    def test_init_with_api_key(self):
        """Test initialization with API key"""
        generator = VideoGenerator(api_key="test_key_123")
        assert generator.api_key == "test_key_123"
        assert os.environ.get("REPLICATE_API_TOKEN") == "test_key_123"

    def test_init_without_api_key(self):
        """Test initialization without API key"""
        with patch.dict(os.environ, {"REPLICATE_API_TOKEN": "env_key"}):
            generator = VideoGenerator()
            assert generator.api_key == "env_key"

    def test_init_sets_environment_variable(self):
        """Test that initialization sets environment variable"""
        VideoGenerator(api_key="my_key")
        assert os.environ["REPLICATE_API_TOKEN"] == "my_key"


class TestGenerateFromText:
    """Test video generation from text"""

    @patch("sa.generators.video_generator.REPLICATE_AVAILABLE", True)
    @patch("sa.generators.video_generator.replicate.run")
    def test_generate_from_text_success(self, mock_run, video_generator):
        """Test successful video generation from text"""
        mock_run.return_value = "https://example.com/video.mp4"

        result = video_generator.generate_from_text("A beautiful sunset", use_cache=False)

        assert result == "https://example.com/video.mp4"
        mock_run.assert_called_once_with(
            "anotherjesse/zeroscope-v2-xl",
            input={"prompt": "A beautiful sunset", "num_frames": 120},
        )

    @patch("sa.generators.video_generator.REPLICATE_AVAILABLE", True)
    @patch("sa.generators.video_generator.replicate.run")
    def test_generate_from_text_with_custom_duration(self, mock_run, video_generator):
        """Test video generation with custom duration"""
        mock_run.return_value = "https://example.com/video.mp4"

        result = video_generator.generate_from_text(
            "A cat playing", duration=10, fps=30, use_cache=False
        )

        assert result == "https://example.com/video.mp4"
        mock_run.assert_called_once_with(
            "anotherjesse/zeroscope-v2-xl",
            input={"prompt": "A cat playing", "num_frames": 300},
        )

    @patch("sa.generators.video_generator.replicate.run")
    def test_generate_from_text_with_list_output(self, mock_run, video_generator):
        """Test video generation when API returns list"""
        mock_run.return_value = ["https://example.com/video1.mp4", "https://example.com/video2.mp4"]

        result = video_generator.generate_from_text("A dog running")

        assert result == "https://example.com/video1.mp4"

    @patch("sa.generators.video_generator.replicate.run")
    def test_generate_from_text_failure(self, mock_run, video_generator):
        """Test video generation failure"""
        mock_run.side_effect = Exception("API error")

        result = video_generator.generate_from_text("A bird flying")

        assert result is None


class TestCreateSlideshow:
    """Test slideshow creation from images"""

    @patch("sa.generators.video_generator.ImageClip")
    @patch("sa.generators.video_generator.concatenate_videoclips")
    def test_create_slideshow_success(
        self, mock_concat, mock_image_clip, video_generator, temp_image_file
    ):
        """Test successful slideshow creation"""
        mock_clip = MagicMock()
        mock_image_clip.return_value = mock_clip
        mock_video = MagicMock()
        mock_concat.return_value = mock_video

        image_paths = [temp_image_file, temp_image_file]
        output_path = "test_slideshow.mp4"

        result = video_generator.create_slideshow(
            image_paths, duration_per_image=5, output_path=output_path
        )

        assert result == output_path
        assert mock_image_clip.call_count == 2
        mock_concat.assert_called_once()
        mock_video.write_videofile.assert_called_once_with(output_path, fps=24, logger=None)

    @patch("sa.generators.video_generator.ImageClip")
    def test_create_slideshow_failure(self, mock_image_clip, video_generator):
        """Test slideshow creation failure"""
        mock_image_clip.side_effect = Exception("Image loading error")

        result = video_generator.create_slideshow(["fake1.png", "fake2.png"])

        assert result is None

    @patch("sa.generators.video_generator.ImageClip")
    @patch("sa.generators.video_generator.concatenate_videoclips")
    def test_create_slideshow_with_custom_duration(
        self, mock_concat, mock_image_clip, video_generator, temp_image_file
    ):
        """Test slideshow with custom duration per image"""
        mock_clip = MagicMock()
        mock_image_clip.return_value = mock_clip
        mock_video = MagicMock()
        mock_concat.return_value = mock_video

        video_generator.create_slideshow([temp_image_file], duration_per_image=10)

        mock_image_clip.assert_called_once_with(temp_image_file, duration=10)


class TestAddAudio:
    """Test adding audio to video"""

    def test_add_audio_method_exists(self, video_generator):
        """Test that method exists"""
        assert hasattr(video_generator, "add_audio")
        assert callable(video_generator.add_audio)


class TestAddBackgroundSounds:
    """Test mixing voice and background audio"""

    def test_add_background_sounds_method_exists(self, video_generator):
        """Test that method exists"""
        assert hasattr(video_generator, "add_background_sounds")
        assert callable(video_generator.add_background_sounds)


class TestEnhancePrompt:
    """Test prompt enhancement"""

    def test_enhance_prompt(self, video_generator):
        """Test prompt enhancement"""
        original = "A cat playing"
        enhanced = video_generator.enhance_prompt(original)

        assert "A cat playing" in enhanced
        assert "cinematic" in enhanced
        assert "smooth motion" in enhanced
        assert "high quality" in enhanced
        assert "4k" in enhanced

    def test_enhance_empty_prompt(self, video_generator):
        """Test enhancing empty prompt"""
        enhanced = video_generator.enhance_prompt("")

        assert "cinematic" in enhanced

    def test_enhance_long_prompt(self, video_generator):
        """Test enhancing long prompt"""
        original = "A detailed scene with mountains, rivers, and wildlife"
        enhanced = video_generator.enhance_prompt(original)

        assert original in enhanced
        assert len(enhanced) > len(original)


class TestPromptValidation:
    """Test prompt validation functionality"""

    def test_validate_prompt_valid(self):
        """Test validation of valid prompt"""
        result = VideoGenerator.validate_prompt("A beautiful sunset over mountains")

        assert result["valid"] is True
        assert len(result["issues"]) == 0
        assert result["length"] > 0

    def test_validate_prompt_empty(self):
        """Test validation of empty prompt"""
        result = VideoGenerator.validate_prompt("")

        assert result["valid"] is False
        assert "empty" in result["issues"][0].lower()

    def test_validate_prompt_too_short(self):
        """Test validation of short prompt"""
        result = VideoGenerator.validate_prompt("Sky")

        assert result["valid"] is False
        assert "too short" in result["issues"][0].lower()

    def test_validate_prompt_too_long(self):
        """Test validation of very long prompt"""
        long_prompt = "A " * 300  # 600 characters
        result = VideoGenerator.validate_prompt(long_prompt)

        assert result["valid"] is False
        assert "too long" in result["issues"][0].lower()

    def test_validate_prompt_suggestions(self):
        """Test validation suggestions for improvement"""
        result = VideoGenerator.validate_prompt("A simple scene")

        assert "suggestions" in result
        assert len(result["suggestions"]) > 0


class TestCaching:
    """Test caching functionality"""

    @patch("sa.generators.video_generator.REPLICATE_AVAILABLE", True)
    @patch("sa.generators.video_generator.replicate.run")
    def test_cache_usage(self, mock_run, video_generator):
        """Test that cache is used for duplicate requests"""
        mock_run.return_value = "https://example.com/video.mp4"

        # First call
        result1 = video_generator.generate_from_text("Test prompt", duration=3)
        # Second call with same params
        result2 = video_generator.generate_from_text("Test prompt", duration=3)

        assert result1 == result2
        assert mock_run.call_count == 1  # Should only call API once
        assert video_generator.stats["cached"] == 1

    def test_clear_cache(self, video_generator):
        """Test cache clearing"""
        video_generator._cache = {"key1": "value1", "key2": "value2"}

        cleared = video_generator.clear_cache()

        assert cleared == 2
        assert len(video_generator._cache) == 0

    def test_get_cache_size(self, video_generator):
        """Test getting cache size"""
        video_generator._cache = {"key1": "value1", "key2": "value2"}

        size = video_generator.get_cache_size()

        assert size == 2


class TestStatistics:
    """Test statistics tracking"""

    def test_get_statistics(self, video_generator):
        """Test getting statistics"""
        stats = video_generator.get_statistics()

        assert "generated" in stats
        assert "cached" in stats
        assert "failed" in stats
        assert isinstance(stats, dict)

    @patch("sa.generators.video_generator.REPLICATE_AVAILABLE", True)
    @patch("sa.generators.video_generator.replicate.run")
    def test_statistics_increment_on_success(self, mock_run, video_generator):
        """Test that statistics increment on successful generation"""
        mock_run.return_value = "https://example.com/video.mp4"

        initial_stats = video_generator.get_statistics()
        video_generator.generate_from_text("Test prompt", use_cache=False)
        new_stats = video_generator.get_statistics()

        assert new_stats["generated"] == initial_stats["generated"] + 1

    def test_statistics_increment_on_failure(self, video_generator):
        """Test that statistics increment on failure"""
        initial_stats = video_generator.get_statistics()
        video_generator.generate_from_text("", use_cache=False)  # Invalid prompt
        new_stats = video_generator.get_statistics()

        assert new_stats["failed"] == initial_stats["failed"] + 1


class TestProgressCallback:
    """Test progress callback functionality"""

    @patch("sa.generators.video_generator.REPLICATE_AVAILABLE", True)
    @patch("sa.generators.video_generator.replicate.run")
    def test_progress_callback_called(self, mock_run, video_generator):
        """Test that progress callback is called"""
        mock_run.return_value = "https://example.com/video.mp4"
        progress_messages = []

        def callback(msg):
            progress_messages.append(msg)

        video_generator.generate_from_text(
            "Test prompt", use_cache=False, progress_callback=callback
        )

        assert len(progress_messages) > 0
        assert any("Generating" in msg for msg in progress_messages)

    @patch("sa.generators.video_generator.ImageClip")
    @patch("sa.generators.video_generator.concatenate_videoclips")
    def test_slideshow_progress_callback(
        self, mock_concat, mock_image_clip, video_generator, temp_image_file
    ):
        """Test progress callback for slideshow"""
        mock_video = MagicMock()
        mock_concat.return_value = mock_video
        progress_messages = []

        def callback(msg):
            progress_messages.append(msg)

        video_generator.create_slideshow(
            [temp_image_file, temp_image_file], progress_callback=callback
        )

        assert len(progress_messages) > 0
        assert any("Creating" in msg for msg in progress_messages)
