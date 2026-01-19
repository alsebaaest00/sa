"""Text-to-Speech Audio Generator with caching, validation and progress tracking"""

import hashlib
import json
import logging
import os
from collections.abc import Callable
from pathlib import Path
from typing import Any

try:
    from elevenlabs import ElevenLabs

    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False
    ElevenLabs = None  # type: ignore

from pydub import AudioSegment

# Configure logging
logger = logging.getLogger(__name__)


class AudioGenerator:
    """Generate audio from text using text-to-speech with caching and validation"""

    def __init__(self, api_key: str | None = None, cache_dir: str = "outputs/audio_cache"):
        """
        Initialize the audio generator

        Args:
            api_key: ElevenLabs API key
            cache_dir: Directory for caching generated audio
        """
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        self.client = None

        if self.api_key and ELEVENLABS_AVAILABLE and ElevenLabs is not None:
            try:
                self.client = ElevenLabs(api_key=self.api_key)
                logger.info("ElevenLabs client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize ElevenLabs client: {e}")

        # Initialize cache
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._cache: dict[str, Any] = {}
        self._load_cache_index()

        # Statistics
        self.stats = {
            "generated": 0,
            "cached": 0,
            "failed": 0,
            "fallback_used": 0,
        }

    def _load_cache_index(self) -> None:
        """Load cache index from disk"""
        index_file = self.cache_dir / "cache_index.json"
        if index_file.exists():
            try:
                with open(index_file) as f:
                    self._cache = json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load cache index: {e}")
                self._cache = {}

    def _save_cache_index(self) -> None:
        """Save cache index to disk"""
        index_file = self.cache_dir / "cache_index.json"
        try:
            with open(index_file, "w") as f:
                json.dump(self._cache, f, indent=2)
        except Exception as e:
            logger.warning(f"Failed to save cache index: {e}")

    def _get_cache_key(self, text: str, params: dict[str, Any]) -> str:
        """Generate cache key from text and parameters"""
        key_data = f"{text}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def clear_cache(self) -> int:
        """Clear all cached audio"""
        cleared = len(self._cache)
        self._cache.clear()
        self._save_cache_index()
        return cleared

    def get_cache_size(self) -> int:
        """Get number of cached items"""
        return len(self._cache)

    def get_statistics(self) -> dict[str, int]:
        """Get generation statistics"""
        return self.stats.copy()

    @staticmethod
    def validate_text(text: str) -> dict[str, Any]:
        """Validate audio generation text

        Args:
            text: The text to validate

        Returns:
            Dictionary with validation results
        """
        issues = []
        suggestions = []

        if not text or not text.strip():
            issues.append("Text is empty")
        elif len(text) < 3:
            issues.append("Text is too short (minimum 3 characters)")

        if len(text) > 5000:
            issues.append("Text is too long (maximum 5000 characters)")
            suggestions.append("Split text into multiple segments")

        # Check for potential issues
        if text.isupper():
            suggestions.append("Text in all caps may sound unnatural")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "suggestions": suggestions,
            "length": len(text),
            "word_count": len(text.split()),
        }

    def generate_speech(
        self,
        text: str,
        voice: str = "Adam",
        model: str = "eleven_multilingual_v2",
        output_path: str = "output.mp3",
        use_cache: bool = True,
        progress_callback: Callable[[str], None] | None = None,
    ) -> str | None:
        """
        Generate speech from text with caching and validation

        Args:
            text: Text to convert to speech
            voice: Voice name to use
            model: TTS model to use
            output_path: Path to save the audio
            use_cache: Whether to use cached results
            progress_callback: Optional callback for progress updates

        Returns:
            Path to generated audio file or None if failed
        """
        # Validate text
        validation = self.validate_text(text)
        if not validation["valid"]:
            logger.error(f"Invalid text: {validation['issues']}")
            self.stats["failed"] += 1
            return None

        # Check cache
        params = {"voice": voice, "model": model}
        cache_key = self._get_cache_key(text, params)

        if use_cache and cache_key in self._cache:
            cached_path = self._cache[cache_key]
            if os.path.exists(cached_path):
                logger.info(f"Using cached audio for text: {text[:50]}...")
                self.stats["cached"] += 1
                if progress_callback:
                    progress_callback("Retrieved from cache")
                cached_result: str | None = cached_path
                return cached_result

        if not self.client or not ELEVENLABS_AVAILABLE:
            logger.info("ElevenLabs not available, using fallback TTS")
            if progress_callback:
                progress_callback("Using fallback TTS...")
            return self._fallback_tts(text, output_path, progress_callback)

        try:
            if progress_callback:
                progress_callback("Generating speech with ElevenLabs...")

            # Create output directory if needed
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)

            # Use text_to_speech.convert instead of deprecated generate
            audio = self.client.text_to_speech.convert(
                text=text,
                voice_id=voice,
                model_id=model,
            )

            # Save the audio
            if progress_callback:
                progress_callback("Saving audio file...")

            with open(output_path, "wb") as f:
                for chunk in audio:
                    f.write(chunk)

            self._cache[cache_key] = output_path
            self._save_cache_index()
            self.stats["generated"] += 1
            logger.info(f"Speech generated successfully: {output_path}")

            if progress_callback:
                progress_callback("Speech generation complete")

            return output_path
        except Exception as e:
            logger.error(f"Error generating speech: {e}")
            # Fallback to basic TTS if ElevenLabs fails
            if progress_callback:
                progress_callback("Falling back to gTTS...")
            return self._fallback_tts(text, output_path, progress_callback)

    def _fallback_tts(
        self,
        text: str,
        output_path: str,
        progress_callback: Callable[[str], None] | None = None,
    ) -> str | None:
        """
        Fallback TTS using gTTS (free alternative)

        Args:
            text: Text to convert
            output_path: Where to save audio
            progress_callback: Optional callback for progress updates

        Returns:
            Path to audio file or None
        """
        try:
            from gtts import gTTS

            if progress_callback:
                progress_callback("Using gTTS fallback...")

            # Create output directory if needed
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)

            tts = gTTS(text=text, lang="ar", slow=False)
            tts.save(output_path)

            self.stats["generated"] += 1
            self.stats["fallback_used"] += 1
            logger.info(f"Fallback TTS generated: {output_path}")

            if progress_callback:
                progress_callback("Fallback TTS complete")

            return output_path
        except Exception as e:
            logger.error(f"Fallback TTS also failed: {e}")
            self.stats["failed"] += 1
            if progress_callback:
                progress_callback(f"Error: {str(e)}")
            return None

    def get_available_voices(self) -> list[str]:
        """
        Get list of available voices

        Returns:
            List of voice names
        """
        default_voices = ["Adam", "Bella", "Antoni", "Rachel", "Domi"]

        if not self.client or not ELEVENLABS_AVAILABLE:
            logger.info("Using default voice list (ElevenLabs not available)")
            return default_voices

        try:
            voices_list = self.client.voices.get_all()
            voices = [voice.name for voice in voices_list.voices if voice.name]
            logger.info(f"Retrieved {len(voices)} voices from ElevenLabs")
            return voices if voices else default_voices
        except Exception as e:
            logger.error(f"Error fetching voices: {e}")
            return default_voices

    def add_background_music(
        self,
        voice_path: str,
        music_path: str,
        output_path: str = "mixed_audio.mp3",
        music_volume: float = 0.3,
        progress_callback: Callable[[str], None] | None = None,
    ) -> str | None:
        """
        Mix voice audio with background music with validation

        Args:
            voice_path: Path to voice audio
            music_path: Path to background music
            output_path: Path to save mixed audio
            music_volume: Volume level for music (0.0 to 1.0)
            progress_callback: Optional callback for progress updates

        Returns:
            Path to mixed audio or None if failed
        """
        # Validate inputs
        if not os.path.exists(voice_path):
            logger.error(f"Voice file not found: {voice_path}")
            self.stats["failed"] += 1
            return None

        if not os.path.exists(music_path):
            logger.error(f"Music file not found: {music_path}")
            self.stats["failed"] += 1
            return None

        if not 0.0 <= music_volume <= 1.0:
            logger.error(f"Invalid music volume: {music_volume}")
            self.stats["failed"] += 1
            return None

        try:
            if progress_callback:
                progress_callback("Loading audio files...")

            voice = AudioSegment.from_file(voice_path)
            music = AudioSegment.from_file(music_path)

            if progress_callback:
                progress_callback("Adjusting music volume...")

            # Adjust music volume
            music = music - (20 * (1 - music_volume))  # Convert to dB

            # Loop music to match voice length
            if progress_callback:
                progress_callback("Syncing audio lengths...")

            if len(music) < len(voice):
                times = (len(voice) // len(music)) + 1
                music = music * times

            music = music[: len(voice)]

            # Mix audio
            if progress_callback:
                progress_callback("Mixing audio tracks...")

            mixed = voice.overlay(music)

            # Create output directory if needed
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)

            if progress_callback:
                progress_callback("Exporting mixed audio...")

            mixed.export(output_path, format="mp3")

            self.stats["generated"] += 1
            logger.info(f"Audio mixed successfully: {output_path}")

            if progress_callback:
                progress_callback("Mixing complete")

            return output_path
        except Exception as e:
            logger.error(f"Error mixing audio: {e}")
            self.stats["failed"] += 1
            if progress_callback:
                progress_callback(f"Error: {str(e)}")
            return None

    def generate_narration_from_script(
        self,
        script_segments: list[dict[str, str]],
        output_path: str = "narration.mp3",
        progress_callback: Callable[[str], None] | None = None,
    ) -> str | None:
        """
        Generate narration from multiple script segments with validation

        Args:
            script_segments: List of dicts with 'text' and optional 'voice'
            output_path: Path to save the complete narration
            progress_callback: Optional callback for progress updates

        Returns:
            Path to narration file or None if failed
        """
        # Validate inputs
        if not script_segments:
            logger.error("No script segments provided")
            self.stats["failed"] += 1
            return None

        try:
            segments: list[AudioSegment] = []
            temp_dir = Path("temp_narration")
            temp_dir.mkdir(exist_ok=True)

            for i, segment in enumerate(script_segments):
                text = segment.get("text", "")
                voice = segment.get("voice", "Adam")

                if not text:
                    logger.warning(f"Skipping empty segment {i}")
                    continue

                if progress_callback:
                    progress_callback(f"Generating segment {i+1}/{len(script_segments)}...")

                temp_path = str(temp_dir / f"segment_{i}.mp3")
                result = self.generate_speech(text, voice, output_path=temp_path, use_cache=False)

                if result and os.path.exists(result):
                    audio_segment = AudioSegment.from_file(result)
                    segments.append(audio_segment)

            if not segments:
                logger.error("No valid segments generated")
                self.stats["failed"] += 1
                return None

            # Combine all segments
            if progress_callback:
                progress_callback("Combining segments...")

            combined = segments[0]
            for segment in segments[1:]:
                combined = combined + segment

            # Create output directory if needed
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)

            if progress_callback:
                progress_callback("Exporting narration...")

            combined.export(output_path, format="mp3")

            # Clean up temp directory
            import shutil

            if temp_dir.exists():
                shutil.rmtree(temp_dir)

            self.stats["generated"] += 1
            logger.info(f"Narration created successfully: {output_path}")

            if progress_callback:
                progress_callback("Narration complete")

            return output_path
        except Exception as e:
            logger.error(f"Error creating narration: {e}")
            self.stats["failed"] += 1
            if progress_callback:
                progress_callback(f"Error: {str(e)}")
            return None
