"""Tests for the API endpoints"""

import pytest
from fastapi.testclient import TestClient
from sa.api import app


@pytest.fixture(scope="module")
def client():
    """Create test client"""
    return TestClient(app)


def test_root(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "SA Platform API"
    assert data["status"] == "running"
    assert "docs" in data


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "services" in data
    assert "image_generation" in data["services"]
    assert "audio_generation" in data["services"]
    assert "video_generation" in data["services"]
    assert "ai_suggestions" in data["services"]


def test_config_status(client):
    """Test configuration status endpoint"""
    response = client.get("/api/v1/config/status")
    assert response.status_code == 200
    data = response.json()
    assert "api_keys" in data
    assert "output_dir" in data
    assert "assets_dir" in data


def test_list_outputs(client):
    """Test listing outputs endpoint"""
    response = client.get("/api/v1/outputs")
    assert response.status_code == 200
    data = response.json()
    assert "images" in data
    assert "videos" in data
    assert "audio" in data
    assert isinstance(data["images"], list)
    assert isinstance(data["videos"], list)
    assert isinstance(data["audio"], list)


def test_image_generation_without_api_key(client):
    """Test image generation fails without API key"""
    response = client.post(
        "/api/v1/images/generate",
        json={
            "prompt": "test image",
            "width": 512,
            "height": 512,
            "num_outputs": 1,
        },
    )
    # Might be 503 if no API key configured
    assert response.status_code in [200, 503]


def test_audio_generation(client):
    """Test audio generation endpoint"""
    response = client.post(
        "/api/v1/audio/generate",
        json={"text": "test audio", "voice": "Adam", "language": "ar"},
    )
    # Should work with gTTS fallback
    assert response.status_code in [200, 503]


def test_get_nonexistent_image(client):
    """Test getting nonexistent image"""
    response = client.get("/api/v1/images/nonexistent.png")
    assert response.status_code == 404


def test_get_nonexistent_audio(client):
    """Test getting nonexistent audio"""
    response = client.get("/api/v1/audio/nonexistent.mp3")
    assert response.status_code == 404


def test_get_nonexistent_video(client):
    """Test getting nonexistent video"""
    response = client.get("/api/v1/videos/nonexistent.mp4")
    assert response.status_code == 404


def test_delete_nonexistent_file(client):
    """Test deleting nonexistent file"""
    response = client.delete("/api/v1/outputs/nonexistent.txt")
    assert response.status_code == 404


def test_improve_prompt_without_api_key(client):
    """Test prompt improvement without API key"""
    response = client.post(
        "/api/v1/suggestions/improve",
        json={"prompt": "test prompt", "content_type": "image"},
    )
    # Might be 503 if OpenAI key not configured
    assert response.status_code in [200, 503]


def test_generate_variations_without_api_key(client):
    """Test generating variations without API key"""
    response = client.post(
        "/api/v1/suggestions/variations",
        json={"prompt": "test prompt", "count": 3},
    )
    # Might be 503 if OpenAI key not configured
    assert response.status_code in [200, 503]


def test_generate_script_without_api_key(client):
    """Test script generation without API key"""
    response = client.post(
        "/api/v1/suggestions/script",
        json={"idea": "test idea", "num_scenes": 2},
    )
    # Might be 503 if OpenAI key not configured
    assert response.status_code in [200, 503]


def test_video_generation_with_invalid_images(client):
    """Test video generation with invalid image paths"""
    response = client.post(
        "/api/v1/videos/generate",
        json={
            "image_paths": ["nonexistent1.png", "nonexistent2.png"],
            "duration_per_image": 3,
        },
    )
    # Should fail because images don't exist
    assert response.status_code in [404, 500]


def test_api_docs_available(client):
    """Test that API documentation is available"""
    # Test OpenAPI docs
    response = client.get("/docs")
    assert response.status_code == 200

    # Test ReDoc
    response = client.get("/redoc")
    assert response.status_code == 200


def test_invalid_image_size(client):
    """Test image generation with invalid size"""
    response = client.post(
        "/api/v1/images/generate",
        json={
            "prompt": "test image",
            "width": 10000,  # Too large
            "height": 10000,
            "num_outputs": 1,
        },
    )
    # Should fail validation
    assert response.status_code == 422


def test_invalid_num_outputs(client):
    """Test image generation with invalid num_outputs"""
    response = client.post(
        "/api/v1/images/generate",
        json={
            "prompt": "test image",
            "width": 512,
            "height": 512,
            "num_outputs": 10,  # Too many
        },
    )
    # Should fail validation
    assert response.status_code == 422
