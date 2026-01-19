"""Tests for multi-language support"""

from sa.utils.i18n import I18n, get_translator


class TestI18n:
    """Tests for internationalization"""

    def test_initialization_with_default_language(self):
        """Test initialization with default Arabic language"""
        i18n = I18n()
        assert i18n.get_current_language() == "ar"

    def test_initialization_with_english(self):
        """Test initialization with English"""
        i18n = I18n(language="en")
        assert i18n.get_current_language() == "en"

    def test_translate_in_arabic(self):
        """Test translation in Arabic"""
        i18n = I18n(language="ar")
        assert i18n.t("generate") == "توليد"
        assert i18n.t("save") == "حفظ"
        assert i18n.t("app_title") == "SA - منصة تحويل النصوص"

    def test_translate_in_english(self):
        """Test translation in English"""
        i18n = I18n(language="en")
        assert i18n.t("generate") == "Generate"
        assert i18n.t("save") == "Save"
        assert i18n.t("app_title") == "SA - Content Generation Platform"

    def test_translate_in_french(self):
        """Test translation in French"""
        i18n = I18n(language="fr")
        assert i18n.t("generate") == "Générer"
        assert i18n.t("save") == "Enregistrer"

    def test_translate_in_spanish(self):
        """Test translation in Spanish"""
        i18n = I18n(language="es")
        assert i18n.t("generate") == "Generar"
        assert i18n.t("save") == "Guardar"

    def test_translate_in_german(self):
        """Test translation in German"""
        i18n = I18n(language="de")
        assert i18n.t("generate") == "Generieren"
        assert i18n.t("save") == "Speichern"

    def test_switch_language(self):
        """Test switching between languages"""
        i18n = I18n(language="ar")
        assert i18n.t("generate") == "توليد"

        i18n.set_language("en")
        assert i18n.t("generate") == "Generate"

        i18n.set_language("fr")
        assert i18n.t("generate") == "Générer"

    def test_fallback_to_arabic_for_invalid_language(self):
        """Test fallback to Arabic for invalid language"""
        i18n = I18n(language="invalid")
        assert i18n.get_current_language() == "ar"

    def test_fallback_to_key_for_missing_translation(self):
        """Test fallback to key for missing translation"""
        i18n = I18n(language="ar")
        result = i18n.t("nonexistent_key")
        assert result == "nonexistent_key"

    def test_get_available_languages(self):
        """Test getting list of available languages"""
        i18n = I18n()
        languages = i18n.get_available_languages()

        assert "ar" in languages
        assert "en" in languages
        assert "fr" in languages
        assert "es" in languages
        assert "de" in languages
        assert len(languages) == 5

    def test_language_names_have_flags(self):
        """Test that language names include flag emojis"""
        i18n = I18n()
        languages = i18n.get_available_languages()

        assert "🇸🇦" in languages["ar"]
        assert "🇬🇧" in languages["en"]
        assert "🇫🇷" in languages["fr"]
        assert "🇪🇸" in languages["es"]
        assert "🇩🇪" in languages["de"]


class TestGetTranslator:
    """Tests for get_translator function"""

    def test_get_translator_default(self):
        """Test getting translator with default language"""
        translator = get_translator()
        assert translator.get_current_language() == "ar"

    def test_get_translator_with_language(self):
        """Test getting translator with specific language"""
        translator = get_translator(language="en")
        assert translator.get_current_language() == "en"

    def test_translator_is_singleton(self):
        """Test that translator returns same instance"""
        translator1 = get_translator()
        translator2 = get_translator()
        assert translator1 is translator2


class TestTranslationCompleteness:
    """Tests to ensure all languages have complete translations"""

    def test_all_languages_have_same_keys(self):
        """Test that all languages have the same translation keys"""
        i18n = I18n()
        ar_keys = set(i18n.TRANSLATIONS["ar"].keys())

        for lang_code in ["en", "fr", "es", "de"]:
            lang_keys = set(i18n.TRANSLATIONS[lang_code].keys())
            assert ar_keys == lang_keys, f"Missing keys in {lang_code}"

    def test_no_empty_translations(self):
        """Test that no translations are empty"""
        i18n = I18n()

        for lang_code, translations in i18n.TRANSLATIONS.items():
            for key, value in translations.items():
                assert value and value.strip(), f"Empty translation for {key} in {lang_code}"


class TestCommonTranslations:
    """Test common translations across all languages"""

    def test_action_buttons_translated(self):
        """Test that action button texts are translated"""
        actions = ["generate", "save", "delete", "edit", "cancel", "download"]

        for lang in ["ar", "en", "fr", "es", "de"]:
            i18n = I18n(language=lang)
            for action in actions:
                translated = i18n.t(action)
                assert translated != action  # Should be translated
                assert len(translated) > 0  # Should not be empty

    def test_navigation_items_translated(self):
        """Test that navigation items are translated"""
        nav_items = ["home", "projects", "templates", "about"]

        for lang in ["ar", "en", "fr", "es", "de"]:
            i18n = I18n(language=lang)
            for item in nav_items:
                translated = i18n.t(item)
                assert len(translated) > 0

    def test_content_types_translated(self):
        """Test that content types are translated"""
        content_types = ["image", "video", "audio"]

        for lang in ["ar", "en", "fr", "es", "de"]:
            i18n = I18n(language=lang)
            for content_type in content_types:
                translated = i18n.t(content_type)
                assert len(translated) > 0
