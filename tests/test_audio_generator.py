"""Tests for AudioGenerator"""

import pytest
from sa.generators.audio_generator import AudioGenerator


def test_audio_generator_init():
    """Test AudioGenerator initialization"""
    generator = AudioGenerator()
    assert generator is not None


def test_get_available_voices():
    """Test getting available voices"""
    generator = AudioGenerator()
    voices = generator.get_available_voices()

    assert len(voices) > 0
    assert isinstance(voices, list)
