# SA Platform API Documentation

## 📚 نظرة عامة

API REST كاملة لمنصة SA - نظام توليد المحتوى بالذكاء الاصطناعي. يوفر endpoints لتوليد الصور، الفيديو، الصوت، وتحسين النصوص.

## 🚀 البداية السريعة

### تشغيل API

```bash
# باستخدام Poetry
poetry run uvicorn sa.api:app --host 0.0.0.0 --port 8000 --reload

# أو باستخدام Python مباشرة
python -m uvicorn sa.api:app --host 0.0.0.0 --port 8000 --reload
```

API سيعمل على: `http://localhost:8000`

### التوثيق التفاعلي

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📋 Endpoints

### 🏥 Health & Configuration

#### `GET /api/v1/health`
فحص حالة API والخدمات المتاحة

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "image_generation": true,
    "audio_generation": true,
    "video_generation": true,
    "ai_suggestions": true
  }
}
```

#### `GET /api/v1/config/status`
الحصول على حالة الإعدادات

**Response:**
```json
{
  "api_keys": {
    "openai": true,
    "replicate": true,
    "elevenlabs": false
  },
  "output_dir": "outputs",
  "assets_dir": "assets"
}
```

### 🖼️ Image Generation

#### `POST /api/v1/images/generate`
توليد صورة من نص

**Request:**
```json
{
  "prompt": "A beautiful sunset over mountains, hyperrealistic, 4k",
  "width": 1024,
  "height": 1024,
  "num_outputs": 1
}
```

**Response:**
```json
{
  "job_id": "abc-123",
  "status": "completed",
  "images": ["/api/v1/images/img_abc-123_0.png"],
  "message": "Generated 1 images"
}
```

#### `GET /api/v1/images/{filename}`
تحميل صورة

### 🎤 Audio Generation

#### `POST /api/v1/audio/generate`
تحويل نص إلى صوت

**Request:**
```json
{
  "text": "مرحباً بكم في منصة SA",
  "voice": "Adam",
  "language": "ar"
}
```

**Response:**
```json
{
  "job_id": "xyz-456",
  "status": "completed",
  "audio_url": "/api/v1/audio/audio_xyz-456.mp3",
  "message": "Audio generated successfully"
}
```

#### `GET /api/v1/audio/{filename}`
تحميل ملف صوتي

### 🎬 Video Generation

#### `POST /api/v1/videos/generate`
إنشاء فيديو من صور

**Request:**
```json
{
  "image_paths": ["outputs/img1.png", "outputs/img2.png"],
  "duration_per_image": 3,
  "audio_path": "outputs/audio.mp3"
}
```

**Response:**
```json
{
  "job_id": "def-789",
  "status": "completed",
  "video_url": "/api/v1/videos/video_def-789.mp4",
  "message": "Video generated successfully"
}
```

#### `GET /api/v1/videos/{filename}`
تحميل فيديو

### 🤖 AI Suggestions

#### `POST /api/v1/suggestions/improve`
تحسين نص باستخدام AI

**Request:**
```json
{
  "prompt": "a dog in a park",
  "content_type": "image"
}
```

**Response:**
```json
{
  "original": "a dog in a park",
  "improved": "A golden retriever playing joyfully in a sunny park, hyperrealistic photography, 4k, professional composition"
}
```

#### `POST /api/v1/suggestions/variations`
توليد تنويعات للنص

**Request:**
```json
{
  "prompt": "a futuristic city",
  "count": 3
}
```

**Response:**
```json
{
  "original": "a futuristic city",
  "variations": [
    "A cyberpunk metropolis with neon lights...",
    "An eco-friendly futuristic city...",
    "A floating futuristic city in the clouds..."
  ]
}
```

#### `POST /api/v1/suggestions/script`
توليد سكريبت فيديو من فكرة

**Request:**
```json
{
  "idea": "A documentary about nature",
  "num_scenes": 3
}
```

**Response:**
```json
{
  "idea": "A documentary about nature",
  "scenes": [
    {
      "visual": "Sunrise over a forest",
      "narration": "Nature awakens with the first light..."
    },
    {
      "visual": "Wildlife in their habitat",
      "narration": "Creatures emerge to start their day..."
    }
  ]
}
```

### 📁 Utilities

#### `GET /api/v1/outputs`
الحصول على قائمة الملفات المولدة

**Response:**
```json
{
  "images": ["img_abc-123_0.png", "img_xyz-456_0.png"],
  "videos": ["video_def-789.mp4"],
  "audio": ["audio_xyz-456.mp3"]
}
```

#### `DELETE /api/v1/outputs/{filename}`
حذف ملف

**Response:**
```json
{
  "message": "File example.png deleted successfully"
}
```

## 🔑 Authentication

حالياً، API لا يتطلب مصادقة. في الإنتاج، يجب إضافة:
- API Keys
- JWT Tokens
- Rate Limiting

## ❌ Error Handling

### Status Codes

- `200` - Success
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error
- `503` - Service Unavailable (API key not configured)

### Error Response Format

```json
{
  "detail": "Image generation service not available. Please configure REPLICATE_API_TOKEN"
}
```

## 🧪 Testing

```bash
# تشغيل جميع اختبارات API
poetry run pytest tests/test_api.py -v

# اختبار endpoint معين
poetry run pytest tests/test_api.py::test_health_check -v

# مع coverage
poetry run pytest tests/test_api.py --cov=sa.api --cov-report=html
```

## 🔧 Development

### إضافة endpoint جديد

1. أضف النموذج في `src/sa/api/models.py`
2. أضف المسار في `src/sa/api/routes.py`
3. أضف الاختبارات في `tests/test_api.py`

### مثال:

```python
# models.py
class NewFeatureRequest(BaseModel):
    data: str

# routes.py
@router.post("/new-feature")
async def new_feature(request: NewFeatureRequest):
    return {"result": "success"}
```

## 📊 Performance

- استخدم `BackgroundTasks` للعمليات الطويلة
- cache للنتائج المكررة
- قيود على حجم الملفات
- rate limiting

## 🐳 Docker

```bash
# بناء الصورة
docker build -t sa-api .

# تشغيل الحاوية
docker run -p 8000:8000 -v $(pwd)/outputs:/app/outputs sa-api
```

## 📝 Notes

- جميع الصور والفيديوهات والصوتيات تُحفظ في `outputs/`
- استخدم gTTS كبديل مجاني لـ ElevenLabs
- OpenAI مطلوب فقط لميزات AI Suggestions
- Replicate مطلوب لتوليد الصور

## 🔗 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [SA Platform GitHub](https://github.com/alsebaaest00/sa)
