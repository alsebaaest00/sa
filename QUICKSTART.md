# 🚀 بدء سريع - SA Platform

## التشغيل السريع في 3 خطوات

### 1️⃣ التثبيت

```bash
poetry install
```

### 2️⃣ إعداد المفاتيح

```bash
cp .env.example .env
# ثم عدّل الملف وأضف مفاتيحك
```

### 3️⃣ التشغيل

```bash
# استخدام Makefile
make run

# أو مباشرة
poetry run streamlit run src/sa/ui/app.py
```

## 🔑 الحصول على المفاتيح

### Replicate (مطلوب)

1. سجل في [replicate.com](https://replicate.com)
2. احصل على Token من [Account](https://replicate.com/account)
3. مجاني للتجربة!

### OpenAI (اختياري)

- للاقتراحات الذكية
- من [platform.openai.com](https://platform.openai.com)

### ElevenLabs (اختياري)

- للصوت عالي الجودة
- من [elevenlabs.io](https://elevenlabs.io)
- البديل: gTTS مجاني

## 📖 المزيد من التفاصيل

- **دليل كامل:** اقرأ [USAGE.md](USAGE.md)
- **أمثلة برمجية:** انظر [examples.py](examples.py)
- **التوثيق:** راجع [README.md](README.md)

## 🧪 الأوامر المفيدة

```bash
make test          # تشغيل الاختبارات
make lint          # فحص الكود
make format        # تنسيق الكود
make clean         # تنظيف
```

---

## استمتع! 🎨
