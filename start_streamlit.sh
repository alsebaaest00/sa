#!/bin/bash
# SA Platform - Streamlit Runner
# تشغيل محسّن بدون أخطاء

echo "🚀 تشغيل منصة SA..."

# إيقاف أي Streamlit قديم
pkill -9 -f streamlit 2>/dev/null

# الانتظار قليلاً
sleep 1

# التشغيل
cd /workspaces/sa
poetry run streamlit run src/sa/ui/app.py

echo "✅ تم التشغيل بنجاح!"
