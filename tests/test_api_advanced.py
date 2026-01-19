"""Advanced API endpoint tests to improve coverage"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from sa.api import app


@pytest.fixture(scope="module")
def client():
    """Create test client"""
    return TestClient(app)


class TestImageEndpoints:
    """Test image generation endpoints"""

    @patch("sa.api.routes.ImageGenerator")
    def test_generate_image_with_guidance(self, mock_gen, client):
        """Test image generation with guidance scale"""
        mock_instance = Mock()
        mock_instance.generate.return_value = "http://example.com/image.jpg"
        mock_gen.return_value = mock_instance

        response = client.post(
            "/api/v1/images/generate",
            json={
                "prompt": "beautiful sunset",
                "width": 512,
                "height": 512,
                "guidance_scale": 8.5,
                "num_outputs": 1,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data
        assert data["status"] == "completed"

    def test_get_image_job_not_found(self, client):
        """Test getting non-existent image job"""
        response = client.get("/api/v1/images/jobs/nonexistent-id")
        assert response.status_code == 404

    def test_list_images_pagination(self, client):
        """Test image listing with pagination"""
        response = client.get("/api/v1/images?limit=5&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert "images" in data
        assert "total" in data


class TestVideoEndpoints:
    """Test video generation endpoints"""

    @patch("sa.api.routes.VideoGenerator")
    def test_generate_video_from_text(self, mock_gen, client):
        """Test video generation from text"""
        mock_instance = Mock()
        mock_instance.generate_from_text.return_value = "http://example.com/video.mp4"
        mock_gen.return_value = mock_instance

        response = client.post(
            "/api/v1/videos/generate",
            json={"prompt": "flying bird", "duration": 5, "fps": 24},
        )
        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data

    @patch("sa.api.routes.VideoGenerator")
    def test_generate_video_from_images(self, mock_gen, client):
        """Test video generation from image URLs"""
        mock_instance = Mock()
        mock_instance.create_slideshow.return_value = "video.mp4"
        mock_gen.return_value = mock_instance

        response = client.post(
            "/api/v1/videos/from-images",
            json={
                "image_urls": [
                    "http://example.com/img1.jpg",
                    "http://example.com/img2.jpg",
                ],
                "duration_per_image": 3.0,
                "fps": 24,
            },
        )
        assert response.status_code == 200

    def test_get_video_job_not_found(self, client):
        """Test getting non-existent video job"""
        response = client.get("/api/v1/videos/jobs/nonexistent-id")
        assert response.status_code == 404


class TestAudioEndpoints:
    """Test audio generation endpoints"""

    @patch("sa.api.routes.AudioGenerator")
    def test_generate_speech_with_voice(self, mock_gen, client):
        """Test speech generation with specific voice"""
        mock_instance = Mock()
        mock_instance.generate_speech.return_value = "audio.mp3"
        mock_gen.return_value = mock_instance

        response = client.post(
            "/api/v1/audio/speech",
            json={"text": "Hello world", "voice": "Rachel", "language": "en"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data

    def test_get_audio_job_not_found(self, client):
        """Test getting non-existent audio job"""
        response = client.get("/api/v1/audio/jobs/nonexistent-id")
        assert response.status_code == 404

    @patch("sa.api.routes.AudioGenerator")
    def test_add_background_music(self, mock_gen, client):
        """Test adding background music to audio"""
        mock_instance = Mock()
        mock_instance.add_background_music.return_value = "final.mp3"
        mock_gen.return_value = mock_instance

        response = client.post(
            "/api/v1/audio/add-music",
            json={
                "audio_url": "http://example.com/speech.mp3",
                "music_url": "http://example.com/music.mp3",
                "music_volume": 0.3,
            },
        )
        assert response.status_code == 200


class TestSuggestionEndpoints:
    """Test AI suggestion endpoints"""

    @patch("sa.api.routes.SuggestionEngine")
    def test_improve_prompt(self, mock_engine, client):
        """Test prompt improvement"""
        mock_instance = Mock()
        mock_instance.improve_prompt.return_value = "improved prompt"
        mock_engine.return_value = mock_instance

        response = client.post(
            "/api/v1/suggestions/improve-prompt",
            json={"prompt": "cat", "media_type": "image"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "improved_prompt" in data

    @patch("sa.api.routes.SuggestionEngine")
    def test_generate_prompts(self, mock_engine, client):
        """Test prompt generation"""
        mock_instance = Mock()
        mock_instance.generate_prompts.return_value = ["prompt1", "prompt2"]
        mock_engine.return_value = mock_instance

        response = client.post(
            "/api/v1/suggestions/generate-prompts",
            json={"theme": "nature", "count": 3, "media_type": "image"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "prompts" in data

    def test_list_themes(self, client):
        """Test listing available themes"""
        response = client.get("/api/v1/suggestions/themes")
        assert response.status_code == 200
        data = response.json()
        assert "themes" in data
        assert isinstance(data["themes"], list)


class TestProjectEndpoints:
    """Test project management endpoints"""

    def test_create_project(self, client):
        """Test creating a new project"""
        response = client.post(
            "/api/v1/projects",
            json={
                "name": "Test Project",
                "description": "A test project",
                "project_type": "video",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "project_id" in data

    def test_list_projects(self, client):
        """Test listing projects"""
        response = client.get("/api/v1/projects")
        assert response.status_code == 200
        data = response.json()
        assert "projects" in data

    def test_get_project_not_found(self, client):
        """Test getting non-existent project"""
        response = client.get("/api/v1/projects/nonexistent-id")
        assert response.status_code == 404

    def test_update_project(self, client):
        """Test updating project"""
        # First create a project
        create_response = client.post(
            "/api/v1/projects",
            json={"name": "Update Test", "description": "Test", "project_type": "image"},
        )
        project_id = create_response.json()["project_id"]

        # Update it
        response = client.put(
            f"/api/v1/projects/{project_id}",
            json={"name": "Updated Name", "description": "Updated description"},
        )
        assert response.status_code == 200

    def test_delete_project(self, client):
        """Test deleting project"""
        # First create a project
        create_response = client.post(
            "/api/v1/projects",
            json={"name": "Delete Test", "description": "Test", "project_type": "audio"},
        )
        project_id = create_response.json()["project_id"]

        # Delete it
        response = client.delete(f"/api/v1/projects/{project_id}")
        assert response.status_code == 200


class TestErrorHandling:
    """Test error handling"""

    def test_invalid_endpoint(self, client):
        """Test accessing invalid endpoint"""
        response = client.get("/api/v1/invalid")
        assert response.status_code == 404

    def test_invalid_method(self, client):
        """Test using invalid HTTP method"""
        response = client.put("/api/v1/health")
        assert response.status_code == 405

    def test_missing_required_field(self, client):
        """Test request with missing required field"""
        response = client.post(
            "/api/v1/images/generate",
            json={"width": 512, "height": 512},  # Missing prompt
        )
        assert response.status_code == 422

    def test_invalid_json(self, client):
        """Test request with invalid JSON"""
        response = client.post(
            "/api/v1/images/generate",
            data="invalid json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 422
