#!/bin/bash
# تشغيل SA Platform API

set -e

echo "🚀 Starting SA Platform API..."
echo "================================"

# تفعيل البيئة الافتراضية
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# التحقق من التبعيات
echo "📦 Checking dependencies..."
poetry install --no-interaction

# تحميل متغيرات البيئة
if [ -f ".env" ]; then
    echo "✅ Loading environment variables from .env"
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️  No .env file found. Some features may not work."
fi

# إنشاء مجلد outputs
mkdir -p outputs
mkdir -p logs

echo ""
echo "🌐 API will be available at:"
echo "   - Main: http://localhost:8000"
echo "   - Docs: http://localhost:8000/docs"
echo "   - Health: http://localhost:8000/api/v1/health"
echo ""
echo "Press Ctrl+C to stop"
echo "================================"

# تشغيل API
poetry run uvicorn sa.api:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload \
    --log-level info
