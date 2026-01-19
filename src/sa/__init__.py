"""sa package"""

__version__ = "0.1.0"
__author__ = "alsebaaest00"
__description__ = "منصة تحويل النصوص إلى صور وفيديوهات مع إضافة الصوت"

from .generators import AudioGenerator, ImageGenerator, VideoGenerator
from .utils import Config, SuggestionEngine, config

__all__ = [
    "ImageGenerator",
    "VideoGenerator",
    "AudioGenerator",
    "SuggestionEngine",
    "config",
    "Config",
]
