"""Demo mode for SA platform - works without API keys"""

import io
import os

import streamlit as st
from PIL import Image, ImageDraw

st.set_page_config(
    page_title="SA - وضع التجربة",
    page_icon="🎨",
    layout="wide",
)

st.title("🎨 SA - منصة تحويل النصوص (وضع التجربة)")

st.info("""
⚠️ **وضع التجربة**: لا يتطلب مفاتيح API

للحصول على الميزات الكاملة، احصل على مفاتيح API من:
- Replicate: https://replicate.com/account/api-tokens
- OpenAI: https://platform.openai.com/api-keys
- ElevenLabs: https://elevenlabs.io (اختياري)
""")

st.divider()

tab1, tab2, tab3 = st.tabs(["🖼️ توليد صورة تجريبية", "📝 اختبار النص", "ℹ️ المعلومات"])

with tab1:
    st.header("🖼️ توليد صورة تجريبية")

    prompt = st.text_area("اكتب وصف الصورة:", placeholder="مثال: منظر طبيعي جميل...", height=100)

    if st.button("🎨 إنشاء صورة تجريبية", type="primary"):
        if prompt:
            with st.spinner("جاري الإنشاء..."):
                # Create a demo image
                img = Image.new("RGB", (512, 512), color=(73, 109, 137))
                d = ImageDraw.Draw(img)

                # Add text
                text_lines = [
                    "صورة تجريبية",
                    "",
                    "الوصف:",
                    prompt[:50] + "..." if len(prompt) > 50 else prompt,
                    "",
                    "للحصول على صور حقيقية،",
                    "أضف مفتاح Replicate API",
                ]

                y_position = 100
                for line in text_lines:
                    d.text((50, y_position), line, fill=(255, 255, 255))
                    y_position += 40

                # Display
                st.success("✅ تم الإنشاء!")
                st.image(img, caption="صورة تجريبية", width=512)

                # Save button
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                buf.seek(0)
                st.download_button(
                    "⬇️ تحميل الصورة",
                    data=buf.getvalue(),
                    file_name="demo_image.png",
                    mime="image/png",
                )
        else:
            st.warning("⚠️ أدخل وصف الصورة أولاً")

with tab2:
    st.header("📝 اختبار معالجة النص")

    text_input = st.text_area("أدخل نصاً:", placeholder="اكتب أي نص هنا...", height=150)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 تحليل"):
            if text_input:
                st.write(f"**عدد الكلمات:** {len(text_input.split())}")
                st.write(f"**عدد الأحرف:** {len(text_input)}")
                st.write(f"**عدد الأسطر:** {len(text_input.splitlines())}")

    with col2:
        if st.button("🔄 عكس"):
            if text_input:
                st.code(text_input[::-1])

    with col3:
        if st.button("🔠 كبير"):
            if text_input:
                st.code(text_input.upper())

with tab3:
    st.header("ℹ️ معلومات المنصة")

    st.markdown("""
    ### 🎯 الميزات الرئيسية:

    #### مع مفاتيح API:
    - 🖼️ **توليد الصور** (Replicate AI)
    - 🎬 **توليد الفيديو** (MoviePy)
    - 🎤 **توليد الصوت** (ElevenLabs + gTTS)
    - 💡 **الاقتراحات الذكية** (OpenAI)
    - 🎯 **5 قوالب جاهزة**
    - 📊 **إدارة المشاريع**

    #### بدون مفاتيح API (الوضع الحالي):
    - ✅ صور تجريبية
    - ✅ معالجة نصوص أساسية
    - ✅ واجهة كاملة

    ---

    ### 🔑 كيفية الحصول على المفاتيح:

    **1. Replicate API:**
    - زر: https://replicate.com
    - سجل حساب مجاني
    - Account → API Tokens

    **2. OpenAI API:**
    - زر: https://platform.openai.com
    - سجل حساب
    - API Keys → Create new

    **3. ElevenLabs (اختياري):**
    - زر: https://elevenlabs.io
    - سجل حساب
    - Profile → API Keys

    ---

    ### 📝 طريقة الاستخدام:

    1. احصل على المفاتيح من الروابط أعلاه
    2. افتح ملف `.env` في المشروع
    3. ضع المفاتيح:
       ```
       REPLICATE_API_KEY=your_key
       OPENAI_API_KEY=your_key
       ELEVENLABS_API_KEY=your_key
       ```
    4. أعد تشغيل التطبيق

    ---

    ### ✅ حالة النظام:
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        replicate_key = os.getenv("REPLICATE_API_KEY")
        if replicate_key and len(replicate_key) > 5:
            st.success("✅ Replicate API")
        else:
            st.error("❌ Replicate API")

    with col2:
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and len(openai_key) > 5:
            st.success("✅ OpenAI API")
        else:
            st.error("❌ OpenAI API")

    with col3:
        elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        if elevenlabs_key and len(elevenlabs_key) > 5:
            st.success("✅ ElevenLabs API")
        else:
            st.warning("⚠️ ElevenLabs (اختياري)")

st.divider()

st.caption("🚀 منصة SA - وضع التجربة | للحصول على الميزات الكاملة، أضف مفاتيح API")
