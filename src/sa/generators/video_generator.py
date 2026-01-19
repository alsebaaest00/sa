"""Text-to-Video Generator with caching and validation"""

import hashlib
import json
import logging
import os
from collections.abc import Callable
from pathlib import Path
from typing import Any

from moviepy.editor import (
    AudioFileClip,
    CompositeAudioClip,
    ImageClip,
    VideoFileClip,
    concatenate_videoclips,
)

# Configure logging
logger = logging.getLogger(__name__)

# Check Replicate availability
try:
    import replicate

    REPLICATE_AVAILABLE = True
except ImportError:
    replicate = None  # type: ignore
    REPLICATE_AVAILABLE = False
    logger.warning("Replicate not available")


class VideoGenerator:
    """Generate videos from text prompts and combine with audio"""

    def __init__(self, api_key: str | None = None, cache_dir: str = "outputs/video_cache"):
        """
        Initialize the video generator

        Args:
            api_key: API key for video generation API
            cache_dir: Directory for caching generated videos
        """
        self.api_key = api_key or os.getenv("REPLICATE_API_TOKEN")
        if self.api_key:
            os.environ["REPLICATE_API_TOKEN"] = self.api_key

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

    def _get_cache_key(self, prompt: str, params: dict[str, Any]) -> str:
        """Generate cache key from prompt and parameters"""
        key_data = f"{prompt}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def clear_cache(self) -> int:
        """Clear all cached videos"""
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
    def validate_prompt(prompt: str) -> dict[str, Any]:
        """Validate video prompt

        Args:
            prompt: The prompt to validate

        Returns:
            Dictionary with validation results
        """
        issues = []
        suggestions = []

        if not prompt or not prompt.strip():
            issues.append("Prompt is empty")
        elif len(prompt) < 10:
            issues.append("Prompt is too short (minimum 10 characters)")
            suggestions.append("Add more details about scene, lighting, camera angle")

        if len(prompt) > 500:
            issues.append("Prompt is too long (maximum 500 characters)")
            suggestions.append("Focus on key visual elements")

        # Check for quality keywords
        quality_keywords = ["cinematic", "high quality", "4k", "detailed", "smooth"]
        has_quality = any(kw in prompt.lower() for kw in quality_keywords)
        if not has_quality:
            suggestions.append("Consider adding quality keywords like 'cinematic' or '4k'")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "suggestions": suggestions,
            "length": len(prompt),
        }

    def generate_from_text(
        self,
        prompt: str,
        duration: int = 5,
        fps: int = 24,
        use_cache: bool = True,
        progress_callback: Callable[[str], None] | None = None,
    ) -> str | None:
        """
        Generate video from text prompt with caching

        Args:
            prompt: Text description of the video
            duration: Video duration in seconds
            fps: Frames per second
            use_cache: Whether to use cached results
            progress_callback: Optional callback for progress updates

        Returns:
            Video URL or None if failed
        """
        # Validate prompt
        validation = self.validate_prompt(prompt)
        if not validation["valid"]:
            logger.error(f"Invalid prompt: {validation['issues']}")
            self.stats["failed"] += 1
            return None

        # Check cache
        params = {"duration": duration, "fps": fps}
        cache_key = self._get_cache_key(prompt, params)

        if use_cache and cache_key in self._cache:
            logger.info(f"Using cached video for prompt: {prompt[:50]}...")
            self.stats["cached"] += 1
            if progress_callback:
                progress_callback("Retrieved from cache")
            cached_result: str | None = self._cache[cache_key]  # type: ignore
            return cached_result

        if not REPLICATE_AVAILABLE:
            logger.error("Replicate API not available")
            self.stats["failed"] += 1
            return None

        try:
            if progress_callback:
                progress_callback("Generating video...")

            output = replicate.run(
                "anotherjesse/zeroscope-v2-xl",
                input={"prompt": prompt, "num_frames": duration * fps},
            )

            # Handle output safely
            result: str | None = None
            if isinstance(output, str):
                result = output
            elif hasattr(output, "__iter__"):
                output_list = list(output)
                result = output_list[0] if output_list else None

            if result:
                self._cache[cache_key] = result
                self._save_cache_index()
                self.stats["generated"] += 1
                logger.info(f"Video generated successfully: {result}")
                if progress_callback:
                    progress_callback("Video generation complete")
            else:
                self.stats["failed"] += 1
                logger.error("No output from video generation")

            return result
        except Exception as e:
            logger.error(f"Error generating video: {e}")
            self.stats["failed"] += 1
            if progress_callback:
                progress_callback(f"Error: {str(e)}")
            return None

    def create_slideshow(
        self,
        image_paths: list[str],
        duration_per_image: int = 3,
        output_path: str = "output.mp4",
        fps: int = 24,
        progress_callback: Callable[[str], None] | None = None,
    ) -> str | None:
        """
        Create slideshow video from images with validation

        Args:
            image_paths: List of image file paths
            duration_per_image: Duration for each image in seconds
            output_path: Path to save the video
            fps: Frames per second
            progress_callback: Optional callback for progress updates

        Returns:
            Path to created video or None if failed
        """
        # Validate inputs
        if not image_paths:
            logger.error("No images provided for slideshow")
            self.stats["failed"] += 1
            return None

        if duration_per_image < 1:
            logger.error(f"Invalid duration: {duration_per_image}")
            self.stats["failed"] += 1
            return None

        # Check if images exist
        valid_paths = []
        for img_path in image_paths:
            if os.path.exists(img_path):
                valid_paths.append(img_path)
            else:
                logger.warning(f"Image not found: {img_path}")

        if not valid_paths:
            logger.error("No valid images found")
            self.stats["failed"] += 1
            return None

        try:
            if progress_callback:
                progress_callback(f"Creating slideshow with {len(valid_paths)} images...")

            clips = []
            for i, img_path in enumerate(valid_paths):
                if progress_callback:
                    progress_callback(f"Processing image {i+1}/{len(valid_paths)}")
                clip = ImageClip(img_path, duration=duration_per_image)
                clips.append(clip)

            if progress_callback:
                progress_callback("Concatenating clips...")
            video = concatenate_videoclips(clips, method="compose")

            if progress_callback:
                progress_callback("Writing video file...")
            video.write_videofile(output_path, fps=fps, logger=None)

            self.stats["generated"] += 1
            logger.info(f"Slideshow created: {output_path}")
            if progress_callback:
                progress_callback("Slideshow complete")
            return output_path
        except Exception as e:
            logger.error(f"Error creating slideshow: {e}")
            self.stats["failed"] += 1
            if progress_callback:
                progress_callback(f"Error: {str(e)}")
            return None

    def add_audio(
        self,
        video_path: str,
        audio_path: str,
        output_path: str = "output_with_audio.mp4",
        progress_callback: Callable[[str], None] | None = None,
    ) -> str | None:
        """
        Add audio to video with validation

        Args:
            video_path: Path to video file
            audio_path: Path to audio file
            output_path: Path to save the output
            progress_callback: Optional callback for progress updates

        Returns:
            Path to video with audio or None if failed
        """
        # Validate inputs
        if not os.path.exists(video_path):
            logger.error(f"Video not found: {video_path}")
            self.stats["failed"] += 1
            return None

        if not os.path.exists(audio_path):
            logger.error(f"Audio not found: {audio_path}")
            self.stats["failed"] += 1
            return None

        try:
            if progress_callback:
                progress_callback("Loading video and audio...")

            video = VideoFileClip(video_path)
            audio = AudioFileClip(audio_path)

            # Trim audio to video length or loop it
            if progress_callback:
                progress_callback("Adjusting audio duration...")

            if audio.duration < video.duration:
                # Loop audio by concatenating
                loops_needed = int(video.duration / audio.duration) + 1
                audio_clips = [audio] * loops_needed
                from moviepy.audio.AudioClip import concatenate_audioclips

                audio = concatenate_audioclips(audio_clips)
                audio = audio.subclip(0, video.duration)
            else:
                audio = audio.subclip(0, video.duration)

            if progress_callback:
                progress_callback("Adding audio to video...")
            video = video.set_audio(audio)

            if progress_callback:
                progress_callback("Writing output file...")
            video.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)

            self.stats["generated"] += 1
            logger.info(f"Audio added successfully: {output_path}")
            if progress_callback:
                progress_callback("Audio addition complete")
            return output_path
        except Exception as e:
            logger.error(f"Error adding audio: {e}")
            self.stats["failed"] += 1
            if progress_callback:
                progress_callback(f"Error: {str(e)}")
            return None

    def add_background_sounds(
        self,
        video_path: str,
        voice_audio: str,
        background_audio: str,
        background_volume: float = 0.3,
        output_path: str = "output_mixed.mp4",
        progress_callback: Callable[[str], None] | None = None,
    ) -> str | None:
        """
        Mix voice and background audio and add to video with validation

        Args:
            video_path: Path to video file
            voice_audio: Path to voice audio file
            background_audio: Path to background audio file
            background_volume: Volume level for background (0.0 to 1.0)
            output_path: Path to save the output
            progress_callback: Optional callback for progress updates

        Returns:
            Path to video with mixed audio or None if failed
        """
        # Validate inputs
        if not os.path.exists(video_path):
            logger.error(f"Video not found: {video_path}")
            self.stats["failed"] += 1
            return None

        if not os.path.exists(voice_audio):
            logger.error(f"Voice audio not found: {voice_audio}")
            self.stats["failed"] += 1
            return None

        if not os.path.exists(background_audio):
            logger.error(f"Background audio not found: {background_audio}")
            self.stats["failed"] += 1
            return None

        if not 0.0 <= background_volume <= 1.0:
            logger.error(f"Invalid volume: {background_volume}")
            self.stats["failed"] += 1
            return None

        try:
            if progress_callback:
                progress_callback("Loading video and audio files...")

            video = VideoFileClip(video_path)
            voice = AudioFileClip(voice_audio)
            background = AudioFileClip(background_audio)

            # Adjust background volume using fx method
            if progress_callback:
                progress_callback("Adjusting volume levels...")
            from moviepy.audio.fx.volumex import volumex

            background = background.fx(volumex, background_volume)

            # Loop background to match video duration
            if progress_callback:
                progress_callback("Processing audio durations...")

            if background.duration < video.duration:
                loops_needed = int(video.duration / background.duration) + 1
                bg_clips = [background] * loops_needed
                from moviepy.audio.AudioClip import concatenate_audioclips

                background = concatenate_audioclips(bg_clips)
                background = background.subclip(0, video.duration)
            else:
                background = background.subclip(0, video.duration)

            # Mix voice and background
            if voice.duration < video.duration:
                voice = voice.set_duration(video.duration)

            if progress_callback:
                progress_callback("Mixing audio tracks...")
            mixed_audio = CompositeAudioClip([voice, background])
            video = video.set_audio(mixed_audio)

            if progress_callback:
                progress_callback("Writing final video...")
            video.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)

            self.stats["generated"] += 1
            logger.info(f"Audio mixed successfully: {output_path}")
            if progress_callback:
                progress_callback("Audio mixing complete")
            return output_path
        except Exception as e:
            logger.error(f"Error mixing audio: {e}")
            self.stats["failed"] += 1
            if progress_callback:
                progress_callback(f"Error: {str(e)}")
            return None

    def enhance_prompt(self, prompt: str) -> str:
        """
        Enhance prompt for better video generation

        Args:
            prompt: Original prompt

        Returns:
            Enhanced prompt
        """
        return f"{prompt}, cinematic, smooth motion, high quality, 4k"
