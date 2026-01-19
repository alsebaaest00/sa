"""Tests for ImageGenerator with comprehensive coverage"""

from unittest.mock import MagicMock, patch

import pytest
from sa.generators.image_generator import ImageGenerator


@pytest.fixture
def generator():
    """Create ImageGenerator instance"""
    return ImageGenerator()


class TestImageGeneratorInit:
    """Test ImageGenerator initialization"""

    def test_init_with_api_key(self):
        """Test initialization with API key"""
        generator = ImageGenerator(api_key="test_key")
        assert generator.api_key == "test_key"

    def test_init_without_api_key(self):
        """Test initialization without API key"""
        generator = ImageGenerator()
        assert generator is not None

    def test_init_creates_cache_dir(self):
        """Test that cache directory is created"""
        generator = ImageGenerator()
        assert generator.cache_dir.exists()

    def test_init_loads_statistics(self):
        """Test that statistics are initialized"""
        generator = ImageGenerator()
        stats = generator.get_statistics()
        assert "generated" in stats
        assert "cached" in stats
        assert "failed" in stats
        assert "downloaded" in stats


class TestPromptValidation:
    """Test prompt validation"""

    def test_validate_valid_prompt(self):
        """Test validation of valid prompt"""
        result = ImageGenerator.validate_prompt("A beautiful landscape")
        assert result["valid"] is True
        assert len(result["issues"]) == 0

    def test_validate_empty_prompt(self):
        """Test validation of empty prompt"""
        result = ImageGenerator.validate_prompt("")
        assert result["valid"] is False
        assert "empty" in result["issues"][0].lower()

    def test_validate_short_prompt(self):
        """Test validation of too short prompt"""
        result = ImageGenerator.validate_prompt("Cat")
        assert result["valid"] is False
        assert "too short" in result["issues"][0].lower()

    def test_validate_long_prompt(self):
        """Test validation of too long prompt"""
        long_prompt = "A " * 600
        result = ImageGenerator.validate_prompt(long_prompt)
        assert result["valid"] is False
        assert "too long" in result["issues"][0].lower()

    def test_validate_suggestions(self):
        """Test that validation provides suggestions"""
        result = ImageGenerator.validate_prompt("A simple scene")
        assert "suggestions" in result
        assert len(result["suggestions"]) > 0


class TestDimensionValidation:
    """Test dimension validation"""

    def test_validate_valid_dimensions(self):
        """Test validation of valid dimensions"""
        result = ImageGenerator.validate_dimensions(1024, 1024)
        assert result["valid"] is True
        assert len(result["issues"]) == 0

    def test_validate_too_small(self):
        """Test validation of too small dimensions"""
        result = ImageGenerator.validate_dimensions(128, 128)
        assert result["valid"] is False
        assert "too small" in result["issues"][0].lower()

    def test_validate_too_large(self):
        """Test validation of too large dimensions"""
        result = ImageGenerator.validate_dimensions(3000, 3000)
        assert result["valid"] is False
        assert "too large" in result["issues"][0].lower()

    def test_validate_not_multiple_of_64(self):
        """Test validation of dimensions not multiple of 64"""
        result = ImageGenerator.validate_dimensions(1000, 1000)
        assert result["valid"] is False
        assert "multiples of 64" in result["issues"][0].lower()


class TestGenerate:
    """Test image generation"""

    @patch("sa.generators.image_generator.REPLICATE_AVAILABLE", True)
    @patch("sa.generators.image_generator.replicate.run")
    def test_generate_success(self, mock_run, generator):
        """Test successful image generation"""
        mock_run.return_value = ["https://example.com/image1.png"]

        result = generator.generate("A beautiful sunset", use_cache=False)

        assert len(result) == 1
        assert "image1.png" in result[0]
        assert generator.stats["generated"] == 1

    @patch("sa.generators.image_generator.REPLICATE_AVAILABLE", True)
    @patch("sa.generators.image_generator.replicate.run")
    def test_generate_multiple_images(self, mock_run, generator):
        """Test generating multiple images"""
        mock_run.return_value = ["https://example.com/image1.png", "https://example.com/image2.png"]

        result = generator.generate("A cat", num_outputs=2, use_cache=False)

        assert len(result) == 2
        assert generator.stats["generated"] == 2

    def test_generate_invalid_prompt(self, generator):
        """Test generation with invalid prompt"""
        result = generator.generate("", use_cache=False)

        assert len(result) == 0
        assert generator.stats["failed"] >= 1

    def test_generate_invalid_dimensions(self, generator):
        """Test generation with invalid dimensions"""
        result = generator.generate("A sunset", width=100, height=100, use_cache=False)

        assert len(result) == 0
        assert generator.stats["failed"] >= 1

    def test_generate_invalid_num_outputs(self, generator):
        """Test generation with invalid num_outputs"""
        result = generator.generate("A sunset", num_outputs=20, use_cache=False)

        assert len(result) == 0
        assert generator.stats["failed"] >= 1

    @patch("sa.generators.image_generator.REPLICATE_AVAILABLE", True)
    @patch("sa.generators.image_generator.replicate.run")
    def test_generate_uses_cache(self, mock_run, generator):
        """Test that cache is used for duplicate requests"""
        mock_run.return_value = ["https://example.com/image.png"]

        # First call
        result1 = generator.generate("Test prompt", use_cache=True)
        # Second call with same params
        result2 = generator.generate("Test prompt", use_cache=True)

        assert result1 == result2
        assert mock_run.call_count == 1
        assert generator.stats["cached"] == 1

    @patch("sa.generators.image_generator.REPLICATE_AVAILABLE", True)
    @patch("sa.generators.image_generator.replicate.run")
    def test_generate_with_progress_callback(self, mock_run, generator):
        """Test generation with progress callback"""
        mock_run.return_value = ["https://example.com/image.png"]
        progress_messages = []

        def callback(msg):
            progress_messages.append(msg)

        generator.generate("Test prompt", use_cache=False, progress_callback=callback)

        assert len(progress_messages) > 0
        assert any("Generating" in msg for msg in progress_messages)


class TestCaching:
    """Test caching functionality"""

    def test_clear_cache(self, generator):
        """Test cache clearing"""
        generator._cache = {"key1": "value1", "key2": "value2"}
        cleared = generator.clear_cache()

        assert cleared == 2
        assert len(generator._cache) == 0

    def test_get_cache_size(self, generator):
        """Test getting cache size"""
        generator._cache = {"key1": "value1", "key2": "value2"}
        size = generator.get_cache_size()

        assert size == 2


class TestDownloadImage:
    """Test image downloading"""

    @patch("sa.generators.image_generator.requests.get")
    @patch("sa.generators.image_generator.Image.open")
    def test_download_success(self, mock_image, mock_get, generator, tmp_path):
        """Test successful image download"""
        mock_response = MagicMock()
        mock_response.content = b"fake image data"
        mock_get.return_value = mock_response

        mock_img = MagicMock()
        mock_image.return_value = mock_img

        save_path = str(tmp_path / "test_image.png")
        result = generator.download_image("https://example.com/image.png", save_path)

        assert result == save_path
        assert generator.stats["downloaded"] == 1

    def test_download_invalid_url(self, generator):
        """Test download with invalid URL"""
        result = generator.download_image("not_a_url", "output.png")

        assert result is None
        assert generator.stats["failed"] >= 1

    def test_download_empty_url(self, generator):
        """Test download with empty URL"""
        result = generator.download_image("", "output.png")

        assert result is None

    def test_download_empty_save_path(self, generator):
        """Test download with empty save path"""
        result = generator.download_image("https://example.com/image.png", "")

        assert result is None

    @patch("sa.generators.image_generator.requests.get")
    @patch("sa.generators.image_generator.Image.open")
    def test_download_with_progress_callback(self, mock_image, mock_get, generator, tmp_path):
        """Test download with progress callback"""
        mock_response = MagicMock()
        mock_response.content = b"fake image data"
        mock_get.return_value = mock_response

        mock_img = MagicMock()
        mock_image.return_value = mock_img

        progress_messages = []

        def callback(msg):
            progress_messages.append(msg)

        save_path = str(tmp_path / "test_image.png")
        generator.download_image(
            "https://example.com/image.png", save_path, progress_callback=callback
        )

        assert len(progress_messages) > 0


class TestBatchDownload:
    """Test batch downloading"""

    @patch("sa.generators.image_generator.requests.get")
    @patch("sa.generators.image_generator.Image.open")
    def test_batch_download_success(self, mock_image, mock_get, generator, tmp_path):
        """Test successful batch download"""
        mock_response = MagicMock()
        mock_response.content = b"fake image data"
        mock_get.return_value = mock_response

        mock_img = MagicMock()
        mock_image.return_value = mock_img

        urls = ["https://example.com/image1.png", "https://example.com/image2.png"]

        result = generator.batch_download(urls, output_dir=str(tmp_path))

        assert len(result) == 2

    def test_batch_download_empty_list(self, generator):
        """Test batch download with empty list"""
        result = generator.batch_download([])

        assert len(result) == 0


class TestEnhancePrompt:
    """Test prompt enhancement"""

    def test_enhance_prompt(self, generator):
        """Test prompt enhancement"""
        prompt = "a beautiful sunset"
        enhanced = generator.enhance_prompt(prompt)

        assert "sunset" in enhanced.lower()
        assert len(enhanced) > len(prompt)
        assert "high quality" in enhanced.lower()


class TestGetSuggestions:
    """Test prompt suggestions"""

    def test_get_suggestions(self, generator):
        """Test getting suggestions"""
        prompt = "a cat"
        suggestions = generator.get_suggestions(prompt)

        assert len(suggestions) > 0
        assert all("cat" in s.lower() for s in suggestions)

    def test_get_suggestions_with_max_limit(self, generator):
        """Test suggestions with max limit"""
        prompt = "a dog"
        suggestions = generator.get_suggestions(prompt, max_suggestions=3)

        assert len(suggestions) == 3

    def test_get_suggestions_empty_prompt(self, generator):
        """Test suggestions with empty prompt"""
        suggestions = generator.get_suggestions("")

        assert len(suggestions) == 0


class TestStatistics:
    """Test statistics tracking"""

    def test_get_statistics(self, generator):
        """Test getting statistics"""
        stats = generator.get_statistics()

        assert "generated" in stats
        assert "cached" in stats
        assert "failed" in stats
        assert "downloaded" in stats
        assert isinstance(stats, dict)
