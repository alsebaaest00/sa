"""SA Platform API - FastAPI REST API"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sa.api.routes import get_router

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="SA Platform API",
    description="""
    # 🎨 SA Platform - AI Content Generation API
    
    منصة متكاملة لتوليد المحتوى باستخدام الذكاء الاصطناعي
    
    ## 🚀 المميزات
    
    * **🖼️ توليد الصور**: إنشاء صور عالية الجودة من النصوص
    * **🎬 توليد الفيديو**: تحويل النصوص أو الصور إلى فيديوهات
    * **🎤 تحويل النص إلى صوت**: صوت طبيعي بلغات متعددة
    * **💡 اقتراحات ذكية**: تحسين النصوص وتوليد أفكار جديدة
    
    ## 📖 البدء السريع
    
    1. احصل على API keys من:
       - [Replicate](https://replicate.com) للصور والفيديو
       - [OpenAI](https://platform.openai.com) للاقتراحات الذكية
       - [ElevenLabs](https://elevenlabs.io) للصوت (اختياري)
    
    2. قم بإعداد متغيرات البيئة في `.env`:
       ```bash
       REPLICATE_API_TOKEN=your_token
       OPENAI_API_KEY=your_key
       ELEVENLABS_API_KEY=your_key
       ```
    
    3. استخدم الـ endpoints أدناه لتوليد المحتوى!
    
    ## 🔗 روابط مفيدة
    
    * [GitHub Repository](https://github.com/alsebaaest00/sa)
    * [Full Documentation](https://github.com/alsebaaest00/sa#readme)
    * [Usage Examples](https://github.com/alsebaaest00/sa/blob/main/USAGE.md)
    
    ## 📝 ملاحظات
    
    - جميع endpoints تدعم JSON
    - معظم العمليات تتم بشكل متزامن
    - الصور والفيديوهات تُحفظ في `outputs/`
    - يمكن استخدام التخزين المؤقت (cache) لتسريع الطلبات المكررة
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "SA Platform",
        "url": "https://github.com/alsebaaest00/sa",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "Health",
            "description": "فحص صحة النظام والخدمات",
        },
        {
            "name": "Configuration",
            "description": "إدارة الإعدادات و API keys",
        },
        {
            "name": "Images",
            "description": "توليد وإدارة الصور باستخدام AI",
        },
        {
            "name": "Videos",
            "description": "توليد وإدارة الفيديوهات",
        },
        {
            "name": "Audio",
            "description": "تحويل النص إلى صوت وإدارة الملفات الصوتية",
        },
        {
            "name": "AI Suggestions",
            "description": "تحسين النصوص والحصول على اقتراحات ذكية",
        },
        {
            "name": "Utilities",
            "description": "أدوات مساعدة لإدارة المخرجات",
        },
    ],
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(get_router())


@app.get("/", tags=["General"])
async def root():
    """Root endpoint"""
    return {
        "name": "SA Platform API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/api/v1/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
