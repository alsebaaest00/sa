"""Text-to-Speech Audio Generator"""

import os
from typing import Optional, Dict, Any, Literal

try:
    from elevenlabs import ElevenLabs
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False

from pydub import AudioSegment


class AudioGenerator:
    """Generate audio from text using text-to-speech"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the audio generator

        Args:
            api_key: ElevenLabs API key
        """
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        self.client = None

        if self.api_key and ELEVENLABS_AVAILABLE:
            try:
                self.client = ElevenLabs(api_key=self.api_key)
            except Exception as e:
                print(f"Failed to initialize ElevenLabs client: {e}")

    def generate_speech(
        self,
        text: str,
        voice: str = "Adam",
        model: str = "eleven_multilingual_v2",
        output_path: str = "output.mp3",
    ) -> Optional[str]:
        """
        Generate speech from text

        Args:
            text: Text to convert to speech
            voice: Voice name to use
            model: TTS model to use
            output_path: Path to save the audio

        Returns:
            Path to generated audio file or None if failed
        """
        if not self.client or not ELEVENLABS_AVAILABLE:
            print("ElevenLabs not available, using fallback TTS")
            return self._fallback_tts(text, output_path)

        try:
            audio = self.client.generate(text=text, voice=voice, model=model)

            # Save the audio
            with open(output_path, "wb") as f:
                for chunk in audio:
                    f.write(chunk)

            return output_path
        except Exception as e:
            print(f"Error generating speech: {e}")
            # Fallback to basic TTS if ElevenLabs fails
            return self._fallback_tts(text, output_path)

    def _fallback_tts(self, text: str, output_path: str) -> Optional[str]:
        """
        Fallback TTS using gTTS (free alternative)

        Args:
            text: Text to convert
            output_path: Where to save audio

        Returns:
            Path to audio file or None
        """
        try:
            from gtts import gTTS

            tts = gTTS(text=text, lang="ar", slow=False)
            tts.save(output_path)
            return output_path
        except Exception as e:
            print(f"Fallback TTS also failed: {e}")
            return None

    def get_available_voices(self) -> list[str]:
        """
        Get list of available voices

        Returns:
            List of voice names
        """
        if not self.client or not ELEVENLABS_AVAILABLE:
            return ["Adam", "Bella", "Antoni", "Rachel", "Domi"]

        try:
            voices_list = self.client.voices.get_all()
            return [voice.name for voice in voices_list.voices]
        except Exception as e:
            print(f"Error fetching voices: {e}")
            return ["Adam", "Bella", "Antoni", "Rachel", "Domi"]

    def add_background_music(
        self,
        voice_path: str,
        music_path: str,
        output_path: str = "mixed_audio.mp3",
        music_volume: float = 0.3,
    ) -> Optional[str]:
        """
        Mix voice audio with background music

        Args:
            voice_path: Path to voice audio
            music_path: Path to background music
            output_path: Path to save mixed audio
            music_volume: Volume level for music (0.0 to 1.0)

        Returns:
            Path to mixed audio or None if failed
        """
        try:
            voice = AudioSegment.from_file(voice_path)
            music = AudioSegment.from_file(music_path)

            # Adjust music volume
            music = music - (20 * (1 - music_volume))  # Convert to dB

            # Loop music to match voice length
            if len(music) < len(voice):
                times = (len(voice) // len(music)) + 1
                music = music * times

            music = music[: len(voice)]

            # Mix audio
            mixed = voice.overlay(music)
            mixed.export(output_path, format="mp3")
            return output_path
        except Exception as e:
            print(f"Error mixing audio: {e}")
            return None

    def generate_narration_from_script(
        self, script_segments: list[Dict[str, str]], output_path: str = "narration.mp3"
    ) -> Optional[str]:
        """
        Generate narration from multiple script segments

        Args:
            script_segments: List of dicts with 'text' and optional 'voice'
            output_path: Path to save the complete narration

        Returns:
            Path to narration file or None if failed
        """
        try:
            segments = []

            for i, segment in enumerate(script_segments):
                text = segment.get("text", "")
                voice = segment.get("voice", "Adam")

                temp_path = f"temp_segment_{i}.mp3"
                self.generate_speech(text, voice, output_path=temp_path)

                audio_segment = AudioSegment.from_file(temp_path)
                segments.append(audio_segment)

                # Clean up temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)

            # Combine all segments
            combined = sum(segments)
            combined.export(output_path, format="mp3")
            return output_path
        except Exception as e:
            print(f"Error creating narration: {e}")
            return None
