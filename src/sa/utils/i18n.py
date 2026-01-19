"""Multi-language support for SA platform"""

from typing import Dict, Optional


class I18n:
    """Internationalization handler"""

    TRANSLATIONS = {
        "ar": {
            # General
            "app_title": "SA - منصة تحويل النصوص",
            "app_subtitle": "منصة تحويل النصوص إلى وسائط متعددة",
            "settings": "⚙️ الإعدادات",
            "language": "اللغة",
            "api_key": "مفتاح API",
            "enter_api_key": "أدخل مفتاح OpenAI API",
            # Navigation
            "home": "🏠 الرئيسية",
            "projects": "📁 المشاريع",
            "templates": "📚 القوالب",
            "about": "ℹ️ حول",
            # Content types
            "image": "صورة",
            "video": "فيديو",
            "audio": "صوت",
            # Actions
            "generate": "توليد",
            "save": "حفظ",
            "delete": "حذف",
            "edit": "تعديل",
            "cancel": "إلغاء",
            "download": "تحميل",
            "upload": "رفع",
            # Messages
            "success": "✅ تم بنجاح!",
            "error": "❌ حدث خطأ",
            "loading": "⏳ جاري التحميل...",
            "no_data": "لا توجد بيانات",
            # Prompts
            "enter_prompt": "أدخل الوصف هنا",
            "improve_prompt": "تحسين الوصف",
            "prompt_suggestions": "اقتراحات",
            # Projects
            "project_name": "اسم المشروع",
            "project_description": "وصف المشروع",
            "create_project": "إنشاء مشروع",
            "delete_project": "حذف المشروع",
            "project_created": "تم إنشاء المشروع بنجاح",
            # Templates
            "select_template": "اختر قالباً",
            "use_template": "استخدام القالب",
            "custom_template": "قالب مخصص",
        },
        "en": {
            # General
            "app_title": "SA - Content Generation Platform",
            "app_subtitle": "Transform text into multimedia content",
            "settings": "⚙️ Settings",
            "language": "Language",
            "api_key": "API Key",
            "enter_api_key": "Enter OpenAI API Key",
            # Navigation
            "home": "🏠 Home",
            "projects": "📁 Projects",
            "templates": "📚 Templates",
            "about": "ℹ️ About",
            # Content types
            "image": "Image",
            "video": "Video",
            "audio": "Audio",
            # Actions
            "generate": "Generate",
            "save": "Save",
            "delete": "Delete",
            "edit": "Edit",
            "cancel": "Cancel",
            "download": "Download",
            "upload": "Upload",
            # Messages
            "success": "✅ Success!",
            "error": "❌ Error occurred",
            "loading": "⏳ Loading...",
            "no_data": "No data available",
            # Prompts
            "enter_prompt": "Enter your prompt here",
            "improve_prompt": "Improve prompt",
            "prompt_suggestions": "Suggestions",
            # Projects
            "project_name": "Project Name",
            "project_description": "Project Description",
            "create_project": "Create Project",
            "delete_project": "Delete Project",
            "project_created": "Project created successfully",
            # Templates
            "select_template": "Select a template",
            "use_template": "Use template",
            "custom_template": "Custom template",
        },
        "fr": {
            # General
            "app_title": "SA - Plateforme de Génération",
            "app_subtitle": "Transformez le texte en contenu multimédia",
            "settings": "⚙️ Paramètres",
            "language": "Langue",
            "api_key": "Clé API",
            "enter_api_key": "Entrez la clé API OpenAI",
            # Navigation
            "home": "🏠 Accueil",
            "projects": "📁 Projets",
            "templates": "📚 Modèles",
            "about": "ℹ️ À propos",
            # Content types
            "image": "Image",
            "video": "Vidéo",
            "audio": "Audio",
            # Actions
            "generate": "Générer",
            "save": "Enregistrer",
            "delete": "Supprimer",
            "edit": "Modifier",
            "cancel": "Annuler",
            "download": "Télécharger",
            "upload": "Charger",
            # Messages
            "success": "✅ Succès!",
            "error": "❌ Erreur",
            "loading": "⏳ Chargement...",
            "no_data": "Aucune donnée",
            # Prompts
            "enter_prompt": "Entrez votre prompt ici",
            "improve_prompt": "Améliorer le prompt",
            "prompt_suggestions": "Suggestions",
            # Projects
            "project_name": "Nom du Projet",
            "project_description": "Description du Projet",
            "create_project": "Créer un Projet",
            "delete_project": "Supprimer le Projet",
            "project_created": "Projet créé avec succès",
            # Templates
            "select_template": "Sélectionnez un modèle",
            "use_template": "Utiliser le modèle",
            "custom_template": "Modèle personnalisé",
        },
        "es": {
            # General
            "app_title": "SA - Plataforma de Generación",
            "app_subtitle": "Transforma texto en contenido multimedia",
            "settings": "⚙️ Configuración",
            "language": "Idioma",
            "api_key": "Clave API",
            "enter_api_key": "Ingrese la clave API de OpenAI",
            # Navigation
            "home": "🏠 Inicio",
            "projects": "📁 Proyectos",
            "templates": "📚 Plantillas",
            "about": "ℹ️ Acerca de",
            # Content types
            "image": "Imagen",
            "video": "Video",
            "audio": "Audio",
            # Actions
            "generate": "Generar",
            "save": "Guardar",
            "delete": "Eliminar",
            "edit": "Editar",
            "cancel": "Cancelar",
            "download": "Descargar",
            "upload": "Subir",
            # Messages
            "success": "✅ ¡Éxito!",
            "error": "❌ Error",
            "loading": "⏳ Cargando...",
            "no_data": "No hay datos",
            # Prompts
            "enter_prompt": "Ingrese su prompt aquí",
            "improve_prompt": "Mejorar prompt",
            "prompt_suggestions": "Sugerencias",
            # Projects
            "project_name": "Nombre del Proyecto",
            "project_description": "Descripción del Proyecto",
            "create_project": "Crear Proyecto",
            "delete_project": "Eliminar Proyecto",
            "project_created": "Proyecto creado exitosamente",
            # Templates
            "select_template": "Seleccione una plantilla",
            "use_template": "Usar plantilla",
            "custom_template": "Plantilla personalizada",
        },
        "de": {
            # General
            "app_title": "SA - Generierungsplattform",
            "app_subtitle": "Text in multimediale Inhalte umwandeln",
            "settings": "⚙️ Einstellungen",
            "language": "Sprache",
            "api_key": "API-Schlüssel",
            "enter_api_key": "OpenAI API-Schlüssel eingeben",
            # Navigation
            "home": "🏠 Startseite",
            "projects": "📁 Projekte",
            "templates": "📚 Vorlagen",
            "about": "ℹ️ Über",
            # Content types
            "image": "Bild",
            "video": "Video",
            "audio": "Audio",
            # Actions
            "generate": "Generieren",
            "save": "Speichern",
            "delete": "Löschen",
            "edit": "Bearbeiten",
            "cancel": "Abbrechen",
            "download": "Herunterladen",
            "upload": "Hochladen",
            # Messages
            "success": "✅ Erfolg!",
            "error": "❌ Fehler",
            "loading": "⏳ Lädt...",
            "no_data": "Keine Daten",
            # Prompts
            "enter_prompt": "Geben Sie Ihren Prompt ein",
            "improve_prompt": "Prompt verbessern",
            "prompt_suggestions": "Vorschläge",
            # Projects
            "project_name": "Projektname",
            "project_description": "Projektbeschreibung",
            "create_project": "Projekt erstellen",
            "delete_project": "Projekt löschen",
            "project_created": "Projekt erfolgreich erstellt",
            # Templates
            "select_template": "Wählen Sie eine Vorlage",
            "use_template": "Vorlage verwenden",
            "custom_template": "Benutzerdefinierte Vorlage",
        },
    }

    LANGUAGE_NAMES = {
        "ar": "🇸🇦 العربية",
        "en": "🇬🇧 English",
        "fr": "🇫🇷 Français",
        "es": "🇪🇸 Español",
        "de": "🇩🇪 Deutsch",
    }

    def __init__(self, language: str = "ar"):
        """Initialize with default language"""
        self.current_language = language if language in self.TRANSLATIONS else "ar"

    def t(self, key: str) -> str:
        """Translate a key to current language"""
        return self.TRANSLATIONS.get(self.current_language, {}).get(
            key, self.TRANSLATIONS["ar"].get(key, key)
        )

    def set_language(self, language: str):
        """Change current language"""
        if language in self.TRANSLATIONS:
            self.current_language = language

    def get_available_languages(self) -> Dict[str, str]:
        """Get list of available languages"""
        return self.LANGUAGE_NAMES

    def get_current_language(self) -> str:
        """Get current language code"""
        return self.current_language


# Global instance
_i18n = I18n()


def get_translator(language: Optional[str] = None) -> I18n:
    """Get translator instance"""
    if language:
        _i18n.set_language(language)
    return _i18n
