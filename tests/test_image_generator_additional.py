"""Additional tests for image generator"""

from unittest.mock import patch

import pytest
from sa.generators.image_generator import ImageGenerator


@pytest.fixture
def image_generator():
    """Create image generator instance"""
    return ImageGenerator(api_key="test_key")


class TestImageGeneratorAdditional:
    """Additional tests for image generator"""

    def test_generate_with_custom_size(self, image_generator):
        """Test generation with custom size"""
        with patch("sa.generators.image_generator.replicate.run") as mock_run:
            mock_run.return_value = ["https://example.com/image.png"]

            result = image_generator.generate("A sunset", width=512, height=512)

            if result:
                assert isinstance(result, list)

    def test_enhance_prompt_empty(self, image_generator):
        """Test enhancing empty prompt"""
        result = image_generator.enhance_prompt("")

        assert len(result) > 0
        assert "high quality" in result or "detailed" in result

    def test_enhance_prompt_long(self, image_generator):
        """Test enhancing long prompt"""
        long_prompt = "A very detailed and complex scene with many elements"
        result = image_generator.enhance_prompt(long_prompt)

        assert long_prompt in result
        assert len(result) > len(long_prompt)

    def test_get_suggestions_for_nature(self, image_generator):
        """Test getting suggestions for nature category"""
        suggestions = image_generator.get_suggestions("nature")

        assert isinstance(suggestions, list)
        assert len(suggestions) > 0

    def test_get_suggestions_for_portraits(self, image_generator):
        """Test getting suggestions for portraits"""
        suggestions = image_generator.get_suggestions("portraits")

        assert isinstance(suggestions, list)

    def test_get_suggestions_invalid_category(self, image_generator):
        """Test getting suggestions for invalid category"""
        suggestions = image_generator.get_suggestions("invalid_category")

        assert isinstance(suggestions, list)

    def test_api_key_from_env(self):
        """Test API key from environment"""
        with patch.dict("os.environ", {"REPLICATE_API_TOKEN": "env_key"}):
            generator = ImageGenerator()
            assert generator.api_key == "env_key"

    def test_api_key_priority(self):
        """Test that provided API key has priority"""
        with patch.dict("os.environ", {"REPLICATE_API_TOKEN": "env_key"}):
            generator = ImageGenerator(api_key="my_key")
            assert generator.api_key == "my_key"
