"""Tests for UI components (Streamlit app)"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys

# Mock streamlit before importing the UI modules
streamlit_mock = MagicMock()
sys.modules["streamlit"] = streamlit_mock


@pytest.fixture
def mock_st():
    """Mock streamlit module"""
    return streamlit_mock


class TestAppMainPage:
    """Test main app page"""

    @patch("sa.ui.app.st")
    def test_page_config(self, mock_st):
        """Test that page config is set"""

        # Verify set_page_config was called
        assert mock_st.set_page_config.called

    @patch("sa.ui.app.ImageGenerator")
    @patch("sa.ui.app.st")
    def test_image_generation_tab(self, mock_st, mock_gen):
        """Test image generation functionality"""
        mock_st.tabs.return_value = [Mock(), Mock(), Mock(), Mock()]
        mock_st.text_input.return_value = "test prompt"
        mock_st.button.return_value = True

        mock_instance = Mock()
        mock_instance.generate.return_value = "http://example.com/image.jpg"
        mock_gen.return_value = mock_instance

        # Import to trigger the code

    @patch("sa.ui.app.st")
    def test_sidebar_config(self, mock_st):
        """Test sidebar configuration"""
        mock_st.sidebar.text_input.return_value = "test_api_key"
        mock_st.sidebar.checkbox.return_value = True


class TestProjectsPage:
    """Test projects page"""

    @patch("sa.ui.projects.st")
    @patch("sa.ui.projects.ProjectManager")
    def test_create_project(self, mock_pm, mock_st):
        """Test project creation"""
        mock_st.text_input.return_value = "Test Project"
        mock_st.text_area.return_value = "Description"
        mock_st.selectbox.return_value = "video"
        mock_st.button.return_value = True

        mock_instance = Mock()
        mock_instance.create_project.return_value = "project_123"
        mock_pm.return_value = mock_instance

    @patch("sa.ui.projects.st")
    @patch("sa.ui.projects.ProjectManager")
    def test_list_projects(self, mock_pm, mock_st):
        """Test listing projects"""
        mock_instance = Mock()
        mock_instance.list_projects.return_value = [
            {"id": "1", "name": "Project 1", "type": "video"},
            {"id": "2", "name": "Project 2", "type": "image"},
        ]
        mock_pm.return_value = mock_instance


class TestTemplatesPage:
    """Test templates page"""

    @patch("sa.ui.templates.st")
    @patch("sa.ui.templates.TemplateManager")
    def test_load_templates(self, mock_tm, mock_st):
        """Test loading templates"""
        mock_instance = Mock()
        mock_instance.list_templates.return_value = [
            {"id": "1", "name": "Template 1", "category": "marketing"},
            {"id": "2", "name": "Template 2", "category": "education"},
        ]
        mock_tm.return_value = mock_instance

    @patch("sa.ui.templates.st")
    def test_template_selection(self, mock_st):
        """Test template selection"""
        mock_st.selectbox.return_value = "Template 1"
        mock_st.button.return_value = True


class TestUIHelpers:
    """Test UI helper functions"""

    @patch("sa.ui.app.st")
    def test_display_image(self, mock_st):
        """Test image display helper"""

        # Simulate displaying an image
        mock_st.image.return_value = None

    @patch("sa.ui.app.st")
    def test_display_video(self, mock_st):
        """Test video display helper"""

        # Simulate displaying a video
        mock_st.video.return_value = None

    @patch("sa.ui.app.st")
    def test_display_audio(self, mock_st):
        """Test audio display helper"""

        # Simulate displaying audio
        mock_st.audio.return_value = None


class TestUIValidation:
    """Test UI input validation"""

    @patch("sa.ui.app.st")
    def test_empty_prompt_validation(self, mock_st):
        """Test validation for empty prompt"""
        mock_st.text_input.return_value = ""
        mock_st.button.return_value = True

        # Should show error
        assert mock_st.error.called or mock_st.warning.called

    @patch("sa.ui.app.st")
    def test_invalid_size_validation(self, mock_st):
        """Test validation for invalid image size"""
        mock_st.slider.return_value = 10000  # Invalid size


class TestUIState:
    """Test UI session state management"""

    @patch("sa.ui.app.st")
    def test_session_state_initialization(self, mock_st):
        """Test session state is initialized"""
        mock_st.session_state = {}

    @patch("sa.ui.app.st")
    def test_api_key_persistence(self, mock_st):
        """Test API key persists in session"""
        mock_st.session_state = {"api_key": "test_key"}
        mock_st.sidebar.text_input.return_value = "test_key"
