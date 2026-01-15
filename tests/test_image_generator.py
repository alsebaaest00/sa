"""Tests for ImageGenerator"""

import pytest
from sa.generators.image_generator import ImageGenerator


def test_image_generator_init():
    """Test ImageGenerator initialization"""
    generator = ImageGenerator()
    assert generator is not None


def test_enhance_prompt():
    """Test prompt enhancement"""
    generator = ImageGenerator()
    prompt = "a beautiful sunset"
    enhanced = generator.enhance_prompt(prompt)

    assert "sunset" in enhanced.lower()
    assert len(enhanced) > len(prompt)


def test_get_suggestions():
    """Test prompt suggestions"""
    generator = ImageGenerator()
    prompt = "a cat"
    suggestions = generator.get_suggestions(prompt)

    assert len(suggestions) > 0
    assert all("cat" in s.lower() for s in suggestions)
