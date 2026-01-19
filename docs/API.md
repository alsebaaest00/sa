# 🚀 SA Platform API Documentation

Complete REST API documentation for the SA Platform.

## 📚 Table of Contents

- [Getting Started](#getting-started)
- [Authentication](#authentication)
- [Endpoints](#endpoints)
- [Examples](#examples)
- [Error Handling](#error-handling)
- [Rate Limits](#rate-limits)

## 🎯 Getting Started

### Base URL

```
http://localhost:8000/api/v1
```

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Quick Start

```bash
# Install dependencies
poetry install

# Set environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the server
poetry run uvicorn src.sa.api.routes:app --reload
```

## 🔐 Authentication

Currently, API keys are configured via environment variables:

```bash
REPLICATE_API_TOKEN=your_replicate_token
OPENAI_API_KEY=your_openai_key
ELEVENLABS_API_KEY=your_elevenlabs_key  # Optional
```

## 📡 Endpoints

### Health & Configuration

#### GET /health
Check API health and service availability.

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

#### GET /config/status
Get configuration status and API key validation.

---

### 🖼️ Image Generation

#### POST /images/generate
Generate images from text descriptions.

**Request:**
```json
{
  "prompt": "beautiful sunset over ocean, vibrant colors, 8k",
  "width": 512,
  "height": 512,
  "num_outputs": 1,
  "guidance_scale": 7.5
}
```

**Response:**
```json
{
  "job_id": "img_abc123",
  "status": "completed",
  "image_urls": ["http://example.com/image.jpg"],
  "message": "Image generated successfully"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/images/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "cute cat playing, studio photo",
    "width": 512,
    "height": 512
  }'
```

---

### 🎬 Video Generation

#### POST /videos/generate
Generate videos from text descriptions.

**Request:**
```json
{
  "prompt": "flying bird in slow motion",
  "duration": 5,
  "fps": 24
}
```

**Response:**
```json
{
  "job_id": "vid_xyz789",
  "status": "completed",
  "video_url": "http://example.com/video.mp4",
  "message": "Video generated successfully"
}
```

---

### 🎤 Audio Generation

#### POST /audio/generate
Convert text to speech.

**Request:**
```json
{
  "text": "Welcome to SA Platform",
  "voice": "Rachel",
  "language": "en"
}
```

**Response:**
```json
{
  "job_id": "aud_def456",
  "status": "completed",
  "audio_url": "outputs/audio_def456.mp3",
  "message": "Audio generated successfully"
}
```

---

### 💡 AI Suggestions

#### POST /suggestions/improve-prompt
Improve user prompts using AI.

**Request:**
```json
{
  "prompt": "cat",
  "media_type": "image"
}
```

**Response:**
```json
{
  "original_prompt": "cat",
  "improved_prompt": "cute fluffy cat, studio photography, detailed fur, professional lighting, 8k",
  "suggestions": ["Add details", "Specify style"]
}
```

#### POST /suggestions/generate
Generate prompt variations.

**Request:**
```json
{
  "theme": "nature",
  "count": 3,
  "media_type": "image"
}
```

**Response:**
```json
{
  "prompts": [
    "serene forest path with morning mist",
    "mountain landscape at golden hour",
    "peaceful lake reflecting sunset colors"
  ]
}
```

---

## 🔧 Complete Examples

### Python

```python
import requests

API_BASE = "http://localhost:8000/api/v1"

# Generate an image
response = requests.post(
    f"{API_BASE}/images/generate",
    json={
        "prompt": "beautiful sunset",
        "width": 512,
        "height": 512
    }
)
result = response.json()
print(f"Image URL: {result['image_urls'][0]}")

# Improve a prompt
response = requests.post(
    f"{API_BASE}/suggestions/improve-prompt",
    json={
        "prompt": "dog",
        "media_type": "image"
    }
)
improved = response.json()
print(f"Improved: {improved['improved_prompt']}")
```

### JavaScript

```javascript
const API_BASE = "http://localhost:8000/api/v1";

// Generate an image
async function generateImage() {
  const response = await fetch(`${API_BASE}/images/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      prompt: "beautiful sunset",
      width: 512,
      height: 512
    })
  });
  
  const result = await response.json();
  console.log("Image URL:", result.image_urls[0]);
}

generateImage();
```

### cURL

```bash
# Generate image
curl -X POST "http://localhost:8000/api/v1/images/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "beautiful sunset",
    "width": 512,
    "height": 512
  }'

# Improve prompt
curl -X POST "http://localhost:8000/api/v1/suggestions/improve-prompt" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "dog",
    "media_type": "image"
  }'
```

---

## ⚠️ Error Handling

### HTTP Status Codes

- `200 OK`: Request successful
- `400 Bad Request`: Invalid input
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

### Error Response Format

```json
{
  "detail": "Error message description",
  "status_code": 422
}
```

### Common Errors

#### Missing API Key
```json
{
  "detail": "Replicate API token not configured",
  "status_code": 500
}
```

#### Invalid Parameters
```json
{
  "detail": [
    {
      "loc": ["body", "width"],
      "msg": "ensure this value is less than or equal to 1024",
      "type": "value_error.number.not_le"
    }
  ]
}
```

---

## 🚦 Rate Limits

Current rate limits (can be configured):

- **Image Generation**: 10 requests/minute
- **Video Generation**: 5 requests/minute
- **Audio Generation**: 20 requests/minute
- **AI Suggestions**: 30 requests/minute

Rate limit headers:
```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 7
X-RateLimit-Reset: 1234567890
```

---

## 📝 Best Practices

### 1. Use Descriptive Prompts

✅ Good:
```json
{
  "prompt": "professional portrait of a woman, studio lighting, bokeh background, 8k"
}
```

❌ Bad:
```json
{
  "prompt": "woman"
}
```

### 2. Handle Errors Gracefully

```python
try:
    response = requests.post(url, json=data)
    response.raise_for_status()
    result = response.json()
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

### 3. Use Caching

The platform supports automatic caching for repeated requests:

```python
# Same prompt will use cached result
result1 = generate_image("sunset")
result2 = generate_image("sunset")  # ⚡ Instant from cache
```

### 4. Monitor Rate Limits

```python
response = requests.post(url, json=data)
remaining = response.headers.get('X-RateLimit-Remaining')
if int(remaining) < 3:
    print("Warning: Approaching rate limit")
```

---

## 🔗 Resources

- **GitHub**: https://github.com/alsebaaest00/sa
- **Issues**: https://github.com/alsebaaest00/sa/issues
- **Documentation**: https://github.com/alsebaaest00/sa#readme
- **Changelog**: [CHANGELOG.md](../../../CHANGELOG.md)

---

## 📄 License

MIT License - see [LICENSE](../../../LICENSE) for details.
