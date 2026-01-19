# 🎨 SA - منصة تحويل النصوص إلى وسائط متعددة

[![CI](https://github.com/alsebaaest00/sa/actions/workflows/python-ci.yml/badge.svg)](https://github.com/alsebaaest00/sa/actions/workflows/python-ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

منصة قوية وذكية لتحويل النصوص إلى صور وفيديوهات مع إضافة الصوت والموسيقى باستخدام الذكاء الاصطناعي.

> 🚀 **[بداية سريعة في 3 خطوات →](QUICKSTART.md)** | 📖 **[دليل الاستخدام الكامل →](USAGE.md)**

## ✨ المميزات

- 🖼️ **توليد الصور من النص**: إنشاء صور عالية الجودة باستخدام AI
- 🎬 **توليد الفيديو**: تحويل النصوص إلى فيديوهات أو إنشاء عروض شرائح
- 🎤 **تحويل النص إلى صوت**: صوت طبيعي بلغات متعددة
- 🎵 **إضافة الموسيقى**: دمج الأصوات المحيطة والخلفية الموسيقية
- 💡 **اقتراحات ذكية**: تحسين النصوص وتوليد أفكار جديدة
- 🎯 **مشاريع متكاملة**: إنشاء فيديوهات كاملة بسيناريو تلقائي

## 🚀 التثبيت السريع

```bash
# استنساخ المشروع
git clone https://github.com/alsebaaest00/sa.git
cd sa

# تثبيت التبعيات
poetry install

# إعداد متغيرات البيئة
cp .env.example .env
# عدّل .env وأضف مفاتيح API
```

## 🎯 الاستخدام

### تشغيل واجهة الويب

```bash
poetry run streamlit run src/sa/ui/app.py
```

ثم افتح المتصفح على: `http://localhost:8501`

### الاستخدام البرمجي

#### مثال بسيط - توليد صورة
```python
from sa.generators import ImageGenerator

# إنشاء مولد الصور
img_gen = ImageGenerator(api_key="your_replicate_token")

# توليد صورة
image_url = img_gen.generate("منظر طبيعي خلاب عند الغروب")
print(f"الصورة: {image_url}")
```

#### مثال متقدم - استخدام الميزات الجديدة 🎯

```python
from sa.generators import VideoGenerator, ImageGenerator, AudioGenerator

# 1. توليد فيديو مع التخزين المؤقت والتقدم
video_gen = VideoGenerator(api_key="your_replicate_token")

def on_progress(message):
    print(f"📹 {message}")

video_url = video_gen.generate_from_text(
    "قطة تلعب في حديقة مشمسة",
    duration=5,
    use_cache=True,  # استخدام الذاكرة المؤقتة
    progress_callback=on_progress  # متابعة التقدم
)

# عرض الإحصائيات
stats = video_gen.get_statistics()
print(f"✅ Generated: {stats['generated']}, Cached: {stats['cached']}")

# 2. توليد صور متعددة وتحميلها
img_gen = ImageGenerator(api_key="your_replicate_token")

# التحقق من النص أولاً
validation = img_gen.validate_prompt("غروب جميل")
if validation["valid"]:
    # توليد مع cache
    urls = [img_gen.generate("غروب جميل", use_cache=True) for _ in range(3)]

    # تحميل دفعة واحدة
    local_paths = img_gen.batch_download(urls, "outputs/images/")
    print(f"📥 تم تحميل {len(local_paths)} صورة")

# 3. تحويل نص إلى صوت مع التحقق
audio_gen = AudioGenerator(elevenlabs_key="your_key")

# التحقق من النص
text = "مرحباً بكم في منصة SA للذكاء الاصطناعي"
validation = audio_gen.validate_text(text)
print(f"📊 الكلمات: {validation['word_count']}, المدة المقدرة: {validation['estimated_duration']}s")

# توليد مع متابعة
audio_path = audio_gen.generate_speech(
    text,
    voice="Rachel",
    use_cache=True,
    progress_callback=lambda msg: print(f"🎤 {msg}")
)

# عرض إحصائيات Fallback
stats = audio_gen.get_statistics()
print(f"🔄 Fallback used: {stats['fallback_used']} times")
```

#### مثال: مشروع فيديو كامل
```python
from sa.generators import VideoGenerator, AudioGenerator
from sa.utils import SuggestionEngine

# 1. تحسين الفكرة
engine = SuggestionEngine(api_key="your_openai_key")
improved_prompt = engine.improve_prompt("قصة عن المستقبل", media_type="video")

# 2. توليد الفيديو
video_gen = VideoGenerator(api_key="your_replicate_token")
video_url = video_gen.generate_from_text(improved_prompt, use_cache=True)

# 3. إضافة التعليق الصوتي
audio_gen = AudioGenerator(elevenlabs_key="your_elevenlabs_key")
narration = audio_gen.generate_speech(
    "هذه رؤية للمستقبل حيث التكنولوجيا تخدم الإنسانية",
    use_cache=True
)

# 4. دمج الصوت مع الفيديو (إذا كان محلياً)
# final_video = video_gen.add_audio("video.mp4", narration, "final.mp4")
```

#### نصائح الاستخدام الأمثل 💡

```python
# ✅ استخدم التحقق قبل التوليد
validation = generator.validate_prompt("your text")
if not validation["valid"]:
    print(f"❌ مشاكل: {validation['issues']}")
    print(f"💡 اقتراحات: {validation['suggestions']}")

# ✅ استخدم الـ cache للطلبات المكررة
result = generator.generate("same prompt", use_cache=True)

# ✅ راقب الإحصائيات لتحسين الأداء
stats = generator.get_statistics()
cache_hit_rate = stats['cached'] / (stats['generated'] + stats['cached'])
print(f"📈 Cache hit rate: {cache_hit_rate:.1%}")

# ✅ امسح الـ cache عند الحاجة
cleared = generator.clear_cache()
print(f"🗑️ تم مسح {cleared} عنصر من الذاكرة")
```

## 📖 التوثيق

### API Keys المطلوبة

#### 1. Replicate (مطلوب للصور والفيديو)
- التسجيل: [replicate.com](https://replicate.com)
- الحصول على Token من [Settings](https://replicate.com/account)

#### 2. OpenAI (للاقتراحات الذكية)
- التسجيل: [platform.openai.com](https://platform.openai.com)
- إنشاء API Key من [Dashboard](https://platform.openai.com/api-keys)

#### 3. ElevenLabs (للصوت عالي الجودة - اختياري)
- التسجيل: [elevenlabs.io](https://elevenlabs.io)
- يمكن استخدام gTTS المجاني كبديل

## 🧪 الاختبارات

```bash
# تشغيل جميع الاختبارات
poetry run pytest

# تشغيل مع تقرير التغطية
poetry run pytest --cov=sa

# فحص جودة الكود
poetry run black --check .
poetry run ruff check .
```

## 📝 الترخيص

هذا المشروع مرخص تحت [MIT License](LICENSE).

## 🙏 شكر وتقدير

- [Replicate](https://replicate.com) - لنماذج AI
- [OpenAI](https://openai.com) - للاقتراحات الذكية
- [ElevenLabs](https://elevenlabs.io) - للصوت عالي الجودة
- [Streamlit](https://streamlit.io) - لواجهة المستخدم

---

**صُنع بـ ❤️ باستخدام Python و AI**
