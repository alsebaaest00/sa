"""Tests for templates and quick references"""

from sa.utils.templates import BestPractices, ContentTips, QuickReferences, Templates


class TestTemplates:
    """Test templates functionality"""

    def test_get_template(self):
        """Test getting a template"""
        template = Templates.get_template("marketing")
        assert template["name"] == "🎯 قالب التسويق"
        assert "image_prompt" in template
        assert "video_prompt" in template
        assert "audio_text" in template

    def test_get_nonexistent_template(self):
        """Test getting non-existent template returns empty"""
        template = Templates.get_template("nonexistent")
        assert template["name"] == "قالب مخصص"

    def test_list_templates(self):
        """Test listing all templates"""
        templates = Templates.list_templates()
        assert len(templates) == 5
        template_names = [t["name"] for t in templates]
        assert "🎯 قالب التسويق" in template_names

    def test_get_templates_dict(self):
        """Test getting templates dictionary"""
        templates_dict = Templates.get_templates_dict()
        assert "🎯 قالب التسويق" in templates_dict
        assert templates_dict["🎯 قالب التسويق"] == "marketing"

    def test_all_templates_have_required_fields(self):
        """Test all templates have required fields"""
        for _name, template in Templates.TEMPLATES.items():
            assert "name" in template
            assert "description" in template
            assert "image_prompt" in template
            assert "video_prompt" in template
            assert "audio_text" in template


class TestQuickReferences:
    """Test quick references functionality"""

    def test_get_prompt_suggestions(self):
        """Test getting prompt suggestions"""
        suggestions = QuickReferences.get_prompt_suggestions("photography")
        assert len(suggestions) > 0
        assert isinstance(suggestions[0], str)

    def test_get_voice_info(self):
        """Test getting voice information"""
        voice_info = QuickReferences.get_voice_info("Adam")
        assert voice_info["gender"] == "ذكر"
        assert "tone" in voice_info

    def test_get_nonexistent_voice(self):
        """Test getting non-existent voice returns default"""
        voice_info = QuickReferences.get_voice_info("Unknown")
        assert voice_info["gender"] == "غير محدد"

    def test_list_voices(self):
        """Test listing all voices"""
        voices = QuickReferences.list_voices()
        assert len(voices) > 0
        voice_names = [v["name"] for v in voices]
        assert "Adam" in voice_names

    def test_all_voices_have_info(self):
        """Test all voices have required info"""
        for _name, info in QuickReferences.VOICE_SETTINGS.items():
            assert "gender" in info
            assert "tone" in info
            assert "speed" in info


class TestContentTips:
    """Test content tips functionality"""

    def test_get_image_tips(self):
        """Test getting image tips"""
        tips = ContentTips.get_tips("image")
        assert len(tips) > 0
        assert "🎨" in tips[0]

    def test_get_video_tips(self):
        """Test getting video tips"""
        tips = ContentTips.get_tips("video")
        assert len(tips) > 0
        assert "🎬" in tips[0]

    def test_get_audio_tips(self):
        """Test getting audio tips"""
        tips = ContentTips.get_tips("audio")
        assert len(tips) > 0
        assert "🎤" in tips[0]

    def test_get_nonexistent_tips(self):
        """Test getting non-existent tips returns default"""
        tips = ContentTips.get_tips("unknown")
        assert len(tips) > 0


class TestBestPractices:
    """Test best practices functionality"""

    def test_get_naming_practice(self):
        """Test getting naming practice"""
        practice = BestPractices.get_practice("naming")
        assert practice["description"] == "تسمية المشاريع والملفات"
        assert len(practice["tips"]) > 0

    def test_get_organization_practice(self):
        """Test getting organization practice"""
        practice = BestPractices.get_practice("organization")
        assert "تنظيم" in practice["description"]

    def test_get_quality_practice(self):
        """Test getting quality practice"""
        practice = BestPractices.get_practice("quality")
        assert len(practice["tips"]) > 0

    def test_all_practices_have_tips(self):
        """Test all practices have tips"""
        for _name, practice in BestPractices.PRACTICES.items():
            assert "description" in practice
            assert "tips" in practice
            assert len(practice["tips"]) > 0
