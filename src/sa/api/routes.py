"""API route handlers"""

import logging
import os
import uuid

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse

from sa.api.models import (
    AudioGenerationRequest,
    AudioGenerationResponse,
    ConfigStatusResponse,
    DeleteResponse,
    HealthResponse,
    ImageGenerationRequest,
    ImageGenerationResponse,
    OutputsResponse,
    PromptImprovementRequest,
    PromptImprovementResponse,
    PromptVariationsRequest,
    PromptVariationsResponse,
    Scene,
    ScriptGenerationRequest,
    ScriptGenerationResponse,
    VideoGenerationRequest,
    VideoGenerationResponse,
)
from sa.generators import AudioGenerator, ImageGenerator, VideoGenerator
from sa.utils import SuggestionEngine, config

logger = logging.getLogger(__name__)

# Create routers
router = APIRouter()
health_router = APIRouter(tags=["Health"])
config_router = APIRouter(tags=["Configuration"])
images_router = APIRouter(prefix="/images", tags=["Images"])
audio_router = APIRouter(prefix="/audio", tags=["Audio"])
videos_router = APIRouter(prefix="/videos", tags=["Videos"])
suggestions_router = APIRouter(prefix="/suggestions", tags=["AI Suggestions"])
utilities_router = APIRouter(prefix="/outputs", tags=["Utilities"])

# Initialize generators
image_generator = None
video_generator = VideoGenerator()
audio_generator = None
suggestion_engine = None

# Initialize generators with API keys if available
if config.replicate_api_key:
    image_generator = ImageGenerator(config.replicate_api_key)
    logger.info("✅ Image generator initialized")

if config.elevenlabs_api_key:
    audio_generator = AudioGenerator(config.elevenlabs_api_key)
    logger.info("✅ Audio generator initialized")
else:
    # Fallback to gTTS
    audio_generator = AudioGenerator(None)
    logger.info("✅ Audio generator initialized with gTTS fallback")

if config.openai_api_key:
    suggestion_engine = SuggestionEngine(config.openai_api_key)
    logger.info("✅ Suggestion engine initialized")


# ============= Health & Configuration Routes =============


@health_router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check API health and service availability"""
    services = {
        "image_generation": image_generator is not None,
        "audio_generation": audio_generator is not None,
        "video_generation": video_generator is not None,
        "ai_suggestions": suggestion_engine is not None,
    }

    return HealthResponse(status="healthy", services=services)


@config_router.get("/config/status", response_model=ConfigStatusResponse)
async def config_status():
    """Get configuration status"""
    validation = config.validate()
    return ConfigStatusResponse(
        api_keys=validation,
        output_dir=config.output_dir,
        assets_dir=config.assets_dir,
    )


# ============= Image Routes =============


@images_router.post("/generate", response_model=ImageGenerationResponse)
async def generate_image(request: ImageGenerationRequest, background_tasks: BackgroundTasks):
    """Generate an image from text description"""
    if not image_generator:
        raise HTTPException(
            status_code=503,
            detail="Image generation service not available. Please configure REPLICATE_API_TOKEN",
        )

    job_id = str(uuid.uuid4())

    try:
        logger.info(f"Generating image for job {job_id}: {request.prompt[:50]}...")
        images = image_generator.generate(
            prompt=request.prompt,
            width=request.width,
            height=request.height,
            num_outputs=request.num_outputs,
        )

        if not images:
            return ImageGenerationResponse(
                job_id=job_id,
                status="failed",
                message="Failed to generate image",
            )

        # Download images
        saved_images = []
        for i, image_url in enumerate(images):
            save_path = f"{config.output_dir}/img_{job_id}_{i}.png"
            if image_generator.download_image(image_url, save_path):
                saved_images.append(f"/api/v1/images/{os.path.basename(save_path)}")

        return ImageGenerationResponse(
            job_id=job_id,
            status="completed",
            images=saved_images,
            message=f"Generated {len(saved_images)} images",
        )

    except Exception as e:
        logger.error(f"Error generating image: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@images_router.get("/{filename}")
async def get_image(filename: str):
    """Download a generated image"""
    file_path = f"{config.output_dir}/{filename}"

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(file_path, media_type="image/png")


# ============= Audio Routes =============


@audio_router.post("/generate", response_model=AudioGenerationResponse)
async def generate_audio(request: AudioGenerationRequest):
    """Generate speech from text"""
    if not audio_generator:
        raise HTTPException(
            status_code=503,
            detail="Audio generation service not available",
        )

    job_id = str(uuid.uuid4())

    try:
        logger.info(f"Generating audio for job {job_id}: {request.text[:50]}...")
        output_path = f"{config.output_dir}/audio_{job_id}.mp3"

        audio = audio_generator.generate_speech(
            text=request.text,
            voice=request.voice,
            output_path=output_path,
        )

        if not audio:
            return AudioGenerationResponse(
                job_id=job_id,
                status="failed",
                message="Failed to generate audio",
            )

        return AudioGenerationResponse(
            job_id=job_id,
            status="completed",
            audio_url=f"/api/v1/audio/{os.path.basename(audio)}",
            message="Audio generated successfully",
        )

    except Exception as e:
        logger.error(f"Error generating audio: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@audio_router.get("/{filename}")
async def get_audio(filename: str):
    """Download a generated audio file"""
    file_path = f"{config.output_dir}/{filename}"

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio not found")

    return FileResponse(file_path, media_type="audio/mpeg")


# ============= Video Routes =============


@videos_router.post("/generate", response_model=VideoGenerationResponse)
async def generate_video(request: VideoGenerationRequest):
    """Create a video from images"""
    if not video_generator:
        raise HTTPException(
            status_code=503,
            detail="Video generation service not available",
        )

    job_id = str(uuid.uuid4())

    try:
        logger.info(f"Generating video for job {job_id}")

        # Verify all images exist
        for img_path in request.image_paths:
            if not os.path.exists(img_path):
                raise HTTPException(status_code=404, detail=f"Image not found: {img_path}")

        output_path = f"{config.output_dir}/video_{job_id}.mp4"

        # Create slideshow
        video = video_generator.create_slideshow(
            image_paths=request.image_paths,
            duration_per_image=request.duration_per_image,
            output_path=output_path,
        )

        if not video:
            return VideoGenerationResponse(
                job_id=job_id,
                status="failed",
                message="Failed to create video",
            )

        # Add audio if provided
        if request.audio_path and os.path.exists(request.audio_path):
            video_with_audio = video_generator.add_audio(video, request.audio_path)
            if video_with_audio:
                video = video_with_audio

        return VideoGenerationResponse(
            job_id=job_id,
            status="completed",
            video_url=f"/api/v1/videos/{os.path.basename(video)}",
            message="Video generated successfully",
        )

    except Exception as e:
        logger.error(f"Error generating video: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@videos_router.get("/{filename}")
async def get_video(filename: str):
    """Download a generated video"""
    file_path = f"{config.output_dir}/{filename}"

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Video not found")

    return FileResponse(file_path, media_type="video/mp4")


# ============= AI Suggestions Routes =============


@suggestions_router.post("/improve", response_model=PromptImprovementResponse)
async def improve_prompt(request: PromptImprovementRequest):
    """Improve a prompt using AI"""
    if not suggestion_engine:
        raise HTTPException(
            status_code=503,
            detail="AI suggestion service not available. Please configure OPENAI_API_KEY",
        )

    try:
        improved = suggestion_engine.improve_prompt(
            request.prompt,
            request.content_type,
        )

        return PromptImprovementResponse(
            original=request.prompt,
            improved=improved,
        )

    except Exception as e:
        logger.error(f"Error improving prompt: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@suggestions_router.post("/variations", response_model=PromptVariationsResponse)
async def generate_variations(request: PromptVariationsRequest):
    """Generate prompt variations"""
    if not suggestion_engine:
        raise HTTPException(
            status_code=503,
            detail="AI suggestion service not available. Please configure OPENAI_API_KEY",
        )

    try:
        variations = suggestion_engine.generate_variations(request.prompt, request.count)
        return PromptVariationsResponse(original=request.prompt, variations=variations)

    except Exception as e:
        logger.error(f"Error generating variations: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@suggestions_router.post("/script", response_model=ScriptGenerationResponse)
async def generate_script(request: ScriptGenerationRequest):
    """Generate a video script from an idea"""
    if not suggestion_engine:
        raise HTTPException(
            status_code=503,
            detail="AI suggestion service not available. Please configure OPENAI_API_KEY",
        )

    try:
        script = suggestion_engine.generate_script_from_idea(
            request.idea,
            request.num_scenes,
        )

        return ScriptGenerationResponse(
            idea=request.idea,
            scenes=[Scene(visual=s["visual"], narration=s["narration"]) for s in script],
        )

    except Exception as e:
        logger.error(f"Error generating script: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


# ============= Utility Routes =============


@utilities_router.get("", response_model=OutputsResponse)
async def list_outputs():
    """List all generated outputs"""
    try:
        outputs = {
            "images": [],
            "videos": [],
            "audio": [],
        }

        if os.path.exists(config.output_dir):
            for file in os.listdir(config.output_dir):
                file_path = os.path.join(config.output_dir, file)
                if os.path.isfile(file_path):
                    if file.endswith((".png", ".jpg", ".jpeg")):
                        outputs["images"].append(file)
                    elif file.endswith((".mp4", ".avi", ".mov")):
                        outputs["videos"].append(file)
                    elif file.endswith((".mp3", ".wav")):
                        outputs["audio"].append(file)

        return OutputsResponse(**outputs)

    except Exception as e:
        logger.error(f"Error listing outputs: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@utilities_router.delete("/{filename}", response_model=DeleteResponse)
async def delete_output(filename: str):
    """Delete a generated file"""
    file_path = f"{config.output_dir}/{filename}"

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        os.remove(file_path)
        return DeleteResponse(message=f"File {filename} deleted successfully")

    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


# Combine all routers
def get_router():
    """Get the main API router with all sub-routers"""
    main_router = APIRouter(prefix="/api/v1")

    main_router.include_router(health_router)
    main_router.include_router(config_router)
    main_router.include_router(images_router)
    main_router.include_router(audio_router)
    main_router.include_router(videos_router)
    main_router.include_router(suggestions_router)
    main_router.include_router(utilities_router)

    return main_router
