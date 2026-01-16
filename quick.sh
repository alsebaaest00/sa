#!/bin/bash

# 🚀 SA Platform - Quick Start Script

clear

cat << "EOF"
╔════════════════════════════════════════════════════════════╗
║                    🚀 SA Platform                           ║
║              Quick Start - الطريقة السهلة                 ║
╚════════════════════════════════════════════════════════════╝
EOF

echo ""
echo "ماذا تريد أن تفعل؟"
echo ""
echo "1️⃣  تشغيل كل شيء (17 خدمة)"
echo "2️⃣  تشغيل الواجهة فقط (سريع)"
echo "3️⃣  عرض جميع الروابط"
echo "4️⃣  إيقاف كل شيء"
echo "5️⃣  عرض الخدمات العاملة"
echo "6️⃣  عرض السجلات"
echo "0️⃣  خروج"
echo ""
read -p "اختر رقم (0-6): " choice

case $choice in
    1)
        echo "🚀 جاري تشغيل جميع الخدمات..."
        bash start_all_services.sh
        ;;
    2)
        echo "⚡ تشغيل الواجهة الرئيسية فقط..."
        pkill -f "streamlit.*8501" 2>/dev/null
        nohup poetry run streamlit run src/sa/ui/app.py \
            --server.port 8501 \
            --server.address 0.0.0.0 \
            --server.headless true \
            > logs/streamlit.log 2>&1 &
        sleep 3
        echo "✅ تم! افتح المنفذ 8501"
        ;;
    3)
        bash show_all_urls.sh
        ;;
    4)
        echo "🛑 جاري إيقاف جميع الخدمات..."
        bash stop_all_services.sh
        ;;
    5)
        echo "📊 الخدمات العاملة:"
        echo "────────────────────────────────"
        lsof -i -P -n | grep LISTEN | grep -E "8[0-9]{3}|5000" | awk '{print $9}' | sort -t: -k2 -n
        ;;
    6)
        echo "📋 آخر 20 سطر من السجلات:"
        echo "────────────────────────────────"
        echo ""
        echo "=== Streamlit ==="
        tail -10 logs/streamlit.log 2>/dev/null || echo "لا يوجد سجل"
        echo ""
        echo "=== FastAPI ==="
        tail -10 logs/fastapi.log 2>/dev/null || echo "لا يوجد سجل"
        ;;
    0)
        echo "👋 مع السلامة!"
        exit 0
        ;;
    *)
        echo "❌ خيار غير صحيح"
        exit 1
        ;;
esac

echo ""
echo "────────────────────────────────────────────────────────"
echo "💡 نصيحة: افتح تبويب PORTS في VS Code واضغط 🌐"
echo "────────────────────────────────────────────────────────"
