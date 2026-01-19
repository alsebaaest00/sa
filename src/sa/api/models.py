"""Pydantic models for API requests and responses"""

from pydantic import BaseModel, Field


class ImageGenerationRequest(BaseModel):
    """Request model for image generation"""

    prompt: str = Field(..., description="Text description of the image")
    width: int = Field(1024, ge=256, le=2048, description="Image width in pixels")
    height: int = Field(1024, ge=256, le=2048, description="Image height in pixels")
    num_outputs: int = Field(1, ge=1, le=4, description="Number of images to generate")

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "A beautiful sunset over mountains, hyperrealistic, 4k",
                "width": 1024,
                "height": 1024,
                "num_outputs": 1,
            }
        }


class ImageGenerationResponse(BaseModel):
    """Response model for image generation"""

    job_id: str
    status: str
    images: list[str] | None = None
    message: str | None = None


class AudioGenerationRequest(BaseModel):
    """Request model for audio generation"""

    text: str = Field(..., description="Text to convert to speech")
    voice: str = Field("Adam", description="Voice name")
    language: str = Field("ar", description="Language code (ar, en, etc.)")

    class Config:
        json_schema_extra = {
            "example": {
                "text": "مرحباً بكم في منصة SA للذكاء الاصطناعي",
                "voice": "Adam",
                "language": "ar",
            }
        }


class AudioGenerationResponse(BaseModel):
    """Response model for audio generation"""

    job_id: str
    status: str
    audio_url: str | None = None
    message: str | None = None


class VideoGenerationRequest(BaseModel):
    """Request model for video generation"""

    image_paths: list[str] = Field(..., description="List of image file paths")
    duration_per_image: int = Field(3, ge=1, le=10, description="Duration per image in seconds")
    audio_path: str | None = Field(None, description="Optional audio track path")

    class Config:
        json_schema_extra = {
            "example": {
                "image_paths": ["outputs/img1.png", "outputs/img2.png"],
                "duration_per_image": 3,
                "audio_path": "outputs/audio.mp3",
            }
        }


class VideoGenerationResponse(BaseModel):
    """Response model for video generation"""

    job_id: str
    status: str
    video_url: str | None = None
    message: str | None = None


class PromptImprovementRequest(BaseModel):
    """Request model for prompt improvement"""

    prompt: str = Field(..., description="Original prompt")
    content_type: str = Field("image", description="Type of content: image, video, or audio")

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "a dog in a park",
                "content_type": "image",
            }
        }


class PromptImprovementResponse(BaseModel):
    """Response model for prompt improvement"""

    original: str
    improved: str


class PromptVariationsRequest(BaseModel):
    """Request model for generating prompt variations"""

    prompt: str = Field(..., description="Original prompt")
    count: int = Field(3, ge=1, le=5, description="Number of variations to generate")

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "a futuristic city",
                "count": 3,
            }
        }


class PromptVariationsResponse(BaseModel):
    """Response model for prompt variations"""

    original: str
    variations: list[str]


class ScriptGenerationRequest(BaseModel):
    """Request model for script generation"""

    idea: str = Field(..., description="Video idea or concept")
    num_scenes: int = Field(3, ge=1, le=10, description="Number of scenes to generate")

    class Config:
        json_schema_extra = {
            "example": {
                "idea": "A documentary about the beauty of nature in different seasons",
                "num_scenes": 3,
            }
        }


class Scene(BaseModel):
    """Model for a video scene"""

    visual: str
    narration: str


class ScriptGenerationResponse(BaseModel):
    """Response model for script generation"""

    idea: str
    scenes: list[Scene]


class HealthResponse(BaseModel):
    """Response model for health check"""

    status: str
    services: dict


class ConfigStatusResponse(BaseModel):
    """Response model for configuration status"""

    api_keys: dict
    output_dir: str
    assets_dir: str


class OutputsResponse(BaseModel):
    """Response model for listing outputs"""

    images: list[str]
    videos: list[str]
    audio: list[str]


class DeleteResponse(BaseModel):
    """Response model for delete operations"""

    message: str
