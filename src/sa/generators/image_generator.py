"""Text-to-Image Generator with caching, validation and progress tracking"""

import hashlib
import json
import logging
import os
from collections.abc import Callable
from io import BytesIO
from pathlib import Path
from typing import Any

import requests
from PIL import Image

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


class ImageGenerator:
    """Generate images from text prompts using AI models with caching and validation"""

    def __init__(self, api_key: str | None = None, cache_dir: str = "outputs/image_cache"):
        """
        Initialize the image generator

        Args:
            api_key: API key for Replicate (optional, uses env var if not provided)
            cache_dir: Directory for caching generated images
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
            "downloaded": 0,
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
        """Clear all cached images"""
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
    def validate_prompt(prompt: str, negative_prompt: str = "") -> dict[str, Any]:
        """Validate image generation prompt

        Args:
            prompt: The prompt to validate
            negative_prompt: The negative prompt to validate

        Returns:
            Dictionary with validation results
        """
        issues = []
        suggestions = []

        if not prompt or not prompt.strip():
            issues.append("Prompt is empty")
        elif len(prompt) < 5:
            issues.append("Prompt is too short (minimum 5 characters)")
            suggestions.append("Add more descriptive details")

        if len(prompt) > 1000:
            issues.append("Prompt is too long (maximum 1000 characters)")
            suggestions.append("Focus on key visual elements")

        if negative_prompt and len(negative_prompt) > 500:
            issues.append("Negative prompt is too long (maximum 500 characters)")

        # Check for quality keywords
        quality_keywords = ["high quality", "detailed", "professional", "8k", "4k"]
        has_quality = any(kw in prompt.lower() for kw in quality_keywords)
        if not has_quality:
            suggestions.append("Consider adding quality keywords like 'high quality' or 'detailed'")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "suggestions": suggestions,
            "prompt_length": len(prompt),
            "negative_prompt_length": len(negative_prompt),
        }

    @staticmethod
    def validate_dimensions(width: int, height: int) -> dict[str, Any]:
        """Validate image dimensions

        Args:
            width: Image width
            height: Image height

        Returns:
            Dictionary with validation results
        """
        issues = []

        if width < 256 or height < 256:
            issues.append("Dimensions too small (minimum 256x256)")

        if width > 2048 or height > 2048:
            issues.append("Dimensions too large (maximum 2048x2048)")

        if width % 64 != 0 or height % 64 != 0:
            issues.append("Dimensions should be multiples of 64")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "width": width,
            "height": height,
        }

    def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 1024,
        num_outputs: int = 1,
        model: str = "black-forest-labs/flux-schnell",
        use_cache: bool = True,
        progress_callback: Callable[[str], None] | None = None,
    ) -> list[str]:
        """
        Generate images from text prompt with caching and validation

        Args:
            prompt: Text description of the image to generate
            negative_prompt: Things to avoid in the image
            width: Image width
            height: Image height
            num_outputs: Number of images to generate
            model: AI model to use
            use_cache: Whether to use cached results
            progress_callback: Optional callback for progress updates

        Returns:
            List of image URLs
        """
        # Validate prompt
        validation = self.validate_prompt(prompt, negative_prompt)
        if not validation["valid"]:
            logger.error(f"Invalid prompt: {validation['issues']}")
            self.stats["failed"] += 1
            return []

        # Validate dimensions
        dim_validation = self.validate_dimensions(width, height)
        if not dim_validation["valid"]:
            logger.error(f"Invalid dimensions: {dim_validation['issues']}")
            self.stats["failed"] += 1
            return []

        # Validate num_outputs
        if num_outputs < 1 or num_outputs > 10:
            logger.error(f"Invalid num_outputs: {num_outputs} (must be 1-10)")
            self.stats["failed"] += 1
            return []

        # Check cache
        params = {
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height,
            "num_outputs": num_outputs,
            "model": model,
        }
        cache_key = self._get_cache_key(prompt, params)

        if use_cache and cache_key in self._cache:
            logger.info(f"Using cached images for prompt: {prompt[:50]}...")
            self.stats["cached"] += 1
            if progress_callback:
                progress_callback("Retrieved from cache")
            cached_result: list[str] = self._cache[cache_key]  # type: ignore
            return cached_result

        if not REPLICATE_AVAILABLE:
            logger.error("Replicate API not available")
            self.stats["failed"] += 1
            return []

        try:
            if progress_callback:
                progress_callback(f"Generating {num_outputs} image(s)...")

            output = replicate.run(
                model,
                input={
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "width": width,
                    "height": height,
                    "num_outputs": num_outputs,
                },
            )

            # Handle output safely
            result: list[str] = []
            if isinstance(output, list | tuple):
                result = [str(item) for item in output]
            elif isinstance(output, str):
                result = [output]
            elif hasattr(output, "__iter__"):
                result = [str(item) for item in output]

            if result:
                self._cache[cache_key] = result
                self._save_cache_index()
                self.stats["generated"] += len(result)
                logger.info(f"Generated {len(result)} image(s) successfully")
                if progress_callback:
                    progress_callback(f"Generated {len(result)} image(s) successfully")
            else:
                self.stats["failed"] += 1
                logger.error("No output from image generation")

            return result
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            self.stats["failed"] += 1
            if progress_callback:
                progress_callback(f"Error: {str(e)}")
            return []

    def enhance_prompt(self, prompt: str) -> str:
        """
        Enhance user prompt with better descriptions for AI generation

        Args:
            prompt: Original user prompt

        Returns:
            Enhanced prompt
        """
        enhancements = [
            "high quality",
            "detailed",
            "professional",
            "8k resolution",
            "photorealistic",
        ]

        return f"{prompt}, {', '.join(enhancements)}"

    def download_image(
        self,
        url: str,
        save_path: str,
        progress_callback: Callable[[str], None] | None = None,
    ) -> str | None:
        """
        Download image from URL with validation

        Args:
            url: Image URL
            save_path: Path to save the image
            progress_callback: Optional callback for progress updates

        Returns:
            Path to saved image or None if failed
        """
        # Validate URL
        if not url or not url.startswith(("http://", "https://")):
            logger.error(f"Invalid URL: {url}")
            self.stats["failed"] += 1
            return None

        # Validate save_path
        if not save_path:
            logger.error("Save path is empty")
            self.stats["failed"] += 1
            return None

        try:
            if progress_callback:
                progress_callback(f"Downloading image from {url[:50]}...")

            response = requests.get(url, timeout=30)
            response.raise_for_status()

            if progress_callback:
                progress_callback("Processing image...")

            img = Image.open(BytesIO(response.content))

            # Create directory if needed
            save_dir = Path(save_path).parent
            save_dir.mkdir(parents=True, exist_ok=True)

            img.save(save_path)
            self.stats["downloaded"] += 1
            logger.info(f"Image downloaded successfully: {save_path}")

            if progress_callback:
                progress_callback("Download complete")

            return save_path
        except Exception as e:
            logger.error(f"Error downloading image: {e}")
            self.stats["failed"] += 1
            if progress_callback:
                progress_callback(f"Error: {str(e)}")
            return None

    def get_suggestions(self, base_prompt: str, max_suggestions: int = 6) -> list[str]:
        """
        Get prompt suggestions for variations

        Args:
            base_prompt: Base prompt to build suggestions from
            max_suggestions: Maximum number of suggestions to return

        Returns:
            List of suggested prompts
        """
        if not base_prompt or not base_prompt.strip():
            logger.warning("Empty base prompt provided")
            return []

        styles = [
            "in anime style",
            "in realistic style",
            "in watercolor painting style",
            "in digital art style",
            "in 3D render style",
            "in oil painting style",
            "in cyberpunk style",
            "in fantasy art style",
            "in minimalist style",
            "in vintage style",
        ]

        suggestions = [f"{base_prompt} {style}" for style in styles[:max_suggestions]]
        logger.info(f"Generated {len(suggestions)} suggestions for: {base_prompt[:50]}...")
        return suggestions

    def batch_download(
        self,
        urls: list[str],
        output_dir: str = "outputs/images",
        progress_callback: Callable[[str], None] | None = None,
    ) -> list[str]:
        """
        Download multiple images

        Args:
            urls: List of image URLs
            output_dir: Directory to save images
            progress_callback: Optional callback for progress updates

        Returns:
            List of saved file paths
        """
        if not urls:
            logger.warning("No URLs provided for batch download")
            return []

        saved_paths = []
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        for i, url in enumerate(urls, 1):
            if progress_callback:
                progress_callback(f"Downloading image {i}/{len(urls)}...")

            filename = f"image_{i}_{hashlib.md5(url.encode()).hexdigest()[:8]}.png"
            save_path = str(output_path / filename)

            result = self.download_image(url, save_path)
            if result:
                saved_paths.append(result)

        logger.info(f"Batch download complete: {len(saved_paths)}/{len(urls)} successful")
        if progress_callback:
            progress_callback(f"Downloaded {len(saved_paths)}/{len(urls)} images")

        return saved_paths
