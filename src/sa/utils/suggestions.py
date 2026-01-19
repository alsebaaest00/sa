"""AI-powered suggestion system for content generation"""

import os
from typing import Any

try:
    from openai import OpenAI

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None  # type: ignore


class SuggestionEngine:
    """Generate smart suggestions for prompts and improvements"""

    def __init__(self, api_key: str | None = None):
        """
        Initialize the suggestion engine

        Args:
            api_key: OpenAI API key
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = None
        self._cache: dict[str, Any] = {}

        if self.api_key and OPENAI_AVAILABLE:
            try:
                self.client = OpenAI(api_key=self.api_key)
            except Exception as e:
                print(f"Failed to initialize OpenAI client: {e}")
                self.client = None

    def improve_prompt(self, prompt: str, content_type: str = "image") -> str:
        """
        Improve user prompt using AI

        Args:
            prompt: Original user prompt
            content_type: Type of content (image, video, audio)

        Returns:
            Improved prompt
        """
        # Check cache
        cache_key = f"improve_{content_type}_{prompt[:50]}"
        if cache_key in self._cache:
            cached_result: str = self._cache[cache_key]  # type: ignore
            return cached_result

        if not self.client:
            return self._fallback_improve(prompt, content_type)

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            f"You are an expert in creating detailed prompts for "
                            f"{content_type} generation. Improve the user's prompt "
                            f"to be more detailed and effective. Keep it concise."
                        ),
                    },
                    {"role": "user", "content": f"Improve this prompt: {prompt}"},
                ],
                max_tokens=200,
                temperature=0.7,
            )
            content = response.choices[0].message.content
            result = str(content.strip() if content else "")
            self._cache[cache_key] = result
            return result
        except Exception as e:
            print(f"Error improving prompt: {e}")
            return self._fallback_improve(prompt, content_type)

    def _fallback_improve(self, prompt: str, content_type: str) -> str:
        """Fallback improvement without API"""
        enhancements = {
            "image": "detailed, high quality, professional, 8k resolution",
            "video": "cinematic, smooth motion, high quality, 4k",
            "audio": "clear, professional quality, well-paced",
        }
        return f"{prompt}, {enhancements.get(content_type, 'high quality')}"

    def generate_variations(self, prompt: str, count: int = 5) -> list[str]:
        """
        Generate prompt variations

        Args:
            prompt: Base prompt
            count: Number of variations to generate (max 10)

        Returns:
            List of prompt variations
        """
        # Validate input
        if not prompt or not prompt.strip():
            return self._fallback_variations("creative scene", count)

        count = min(count, 10)  # Limit to 10 variations

        if not self.client:
            return self._fallback_variations(prompt, count)

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Generate creative variations of the given prompt. "
                            "Each variation should be on a new line and numbered."
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"Generate {count} variations of: {prompt}",
                    },
                ],
                max_tokens=300,
                temperature=0.8,
            )
            content = response.choices[0].message.content
            if not content:
                return self._fallback_variations(prompt, count)

            # Clean and parse variations
            variations = []
            for line in content.strip().split("\n"):
                line = line.strip()
                # Remove numbering (1., 2., etc.)
                if line and line[0].isdigit():
                    line = line.split(".", 1)[-1].strip()
                if line:
                    variations.append(line)

            return variations[:count] if variations else self._fallback_variations(prompt, count)
        except Exception as e:
            print(f"Error generating variations: {e}")
            return self._fallback_variations(prompt, count)

    def _fallback_variations(self, prompt: str, count: int) -> list[str]:
        """Generate variations without API"""
        styles = [
            "realistic style",
            "artistic style",
            "modern style",
            "classic style",
            "minimalist style",
            "detailed style",
        ]
        return [f"{prompt} in {style}" for style in styles[:count]]

    def suggest_next_scene(self, current_scene: str) -> list[str]:
        """
        Suggest next scenes for video storytelling

        Args:
            current_scene: Description of current scene

        Returns:
            List of suggested next scenes
        """
        try:
            if not self.client:
                return ["Continue the scene", "Fade to next location", "Close-up shot"]

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a creative storyteller. " "Suggest logical next scenes."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Current scene: {current_scene}\n" f"Suggest 3 possible next scenes:"
                        ),
                    },
                ],
                max_tokens=200,
            )
            content = response.choices[0].message.content
            if not content:
                return []
            return [line.strip() for line in content.strip().split("\n") if line.strip()]
        except Exception as e:
            print(f"Error suggesting scenes: {e}")
            return [
                f"Continue from: {current_scene}",
                "Transition to a different location",
                "Close-up detail from the scene",
            ]

    def suggest_music_mood(self, scene_description: str) -> dict[str, str]:
        """
        Suggest appropriate music mood for a scene

        Args:
            scene_description: Description of the scene

        Returns:
            Dictionary with mood, tempo, and genre suggestions
        """
        try:
            if not self.client:
                return {"mood": "neutral", "tempo": "medium", "genre": "ambient"}

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Suggest appropriate background music characteristics.",
                    },
                    {
                        "role": "user",
                        "content": f"Scene: {scene_description}\nSuggest: mood, tempo, genre",
                    },
                ],
                max_tokens=100,
            )
            content = response.choices[0].message.content
            if not content:
                return {"mood": "calm", "tempo": "medium", "genre": "ambient"}
            content_str = content.strip()

            # Parse response
            lines = content_str.lower().split("\n")
            result = {"mood": "calm", "tempo": "medium", "genre": "ambient"}

            for line in lines:
                if "mood" in line:
                    result["mood"] = line.split(":")[-1].strip()
                elif "tempo" in line:
                    result["tempo"] = line.split(":")[-1].strip()
                elif "genre" in line:
                    result["genre"] = line.split(":")[-1].strip()

            return result
        except Exception as e:
            print(f"Error suggesting music: {e}")
            return {"mood": "calm", "tempo": "medium", "genre": "ambient"}

    def generate_script_from_idea(self, idea: str, num_scenes: int = 5) -> list[dict[str, str]]:
        """
        Generate a complete script from an idea

        Args:
            idea: Basic story idea
            num_scenes: Number of scenes to generate

        Returns:
            List of scene dictionaries with text and visuals
        """
        try:
            if not self.client:
                return self._fallback_script(idea, num_scenes)

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Create a video script with scene descriptions " "and narration."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Create a {num_scenes}-scene video script for: {idea}\n"
                            f"Format each scene as: Scene X: [visual description] | "
                            f"Narration: [text]"
                        ),
                    },
                ],
                max_tokens=500,
            )
            content = response.choices[0].message.content
            if not content:
                return []
            content = content.strip()

            # Parse scenes
            scenes = []
            for line in content.split("\n"):
                if "|" in line and ":" in line:
                    parts = line.split("|")
                    visual = parts[0].split(":", 1)[-1].strip()
                    narration = parts[1].split(":", 1)[-1].strip()
                    scenes.append({"visual": visual, "narration": narration})

            return scenes if scenes else self._fallback_script(idea)
        except Exception as e:
            print(f"Error generating script: {e}")
            return self._fallback_script(idea)

    def _fallback_script(self, idea: str, num_scenes: int = 5) -> list[dict[str, str]]:
        """Generate basic script without API"""
        base_scenes = [
            {
                "visual": f"Opening scene: {idea}",
                "narration": f"Introduction to {idea}",
            },
            {"visual": f"Main content about {idea}", "narration": "Main story unfolds"},
            {"visual": "Climax or key moment", "narration": "The most important part"},
            {"visual": "Resolution", "narration": "How things conclude"},
            {"visual": "Closing scene", "narration": "Final thoughts"},
        ]
        return base_scenes[:num_scenes]

    def clear_cache(self) -> None:
        """Clear the internal cache"""
        self._cache.clear()

    def get_cache_size(self) -> int:
        """Get the number of cached items"""
        return len(self._cache)

    def validate_prompt(self, prompt: str) -> dict[str, Any]:
        """
        Validate and analyze a prompt

        Args:
            prompt: Prompt to validate

        Returns:
            Dictionary with validation results
        """
        suggestions: list[str] = []
        prompt_length = len(prompt)
        word_count = len(prompt.split())

        if prompt_length < 10:
            suggestions.append("Prompt is too short. Add more details.")
        if word_count < 3:
            suggestions.append("Use at least 3 words for better results.")
        if prompt_length > 500:
            suggestions.append("Prompt might be too long. Consider shortening.")

        result = {
            "valid": bool(prompt and prompt.strip()),
            "length": prompt_length,
            "word_count": word_count,
            "has_details": word_count > 5,
            "suggestions": suggestions,
        }

        return result
