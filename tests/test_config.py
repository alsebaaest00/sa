"""Tests for configuration"""

from sa.utils.config import Config, config


def test_config_init():
    """Test Config initialization"""
    test_config = Config()
    assert test_config is not None
    assert test_config.output_dir == "outputs"
    assert test_config.assets_dir == "assets"


def test_config_validation():
    """Test config validation"""
    validation = config.validate()
    assert isinstance(validation, dict)
    assert "openai" in validation
    assert "replicate" in validation
    assert "elevenlabs" in validation
    assert "paths" in validation
