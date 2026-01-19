"""Streamlit web interface for the SA platform"""

import os
from datetime import datetime

import streamlit as st

from sa.ui.templates import show_templates_and_tips

# Set page config
st.set_page_config(
    page_title="SA - منصة تحويل النصوص",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import generators and utilities
try:
    from sa.generators import AudioGenerator, ImageGenerator, VideoGenerator
    from sa.utils import SuggestionEngine, config
except ImportError:
    st.error("⚠️ خطأ في استيراد المكونات. تأكد من تثبيت جميع التبعيات.")
    st.stop()


def init_session_state():
    """Initialize session state variables"""
    if "generated_images" not in st.session_state:
        st.session_state.generated_images = []
    if "generated_videos" not in st.session_state:
        st.session_state.generated_videos = []
    if "generated_audio" not in st.session_state:
        st.session_state.generated_audio = []
    if "project_script" not in st.session_state:
        st.session_state.project_script = []


def main():
    """Main application"""
    init_session_state()

    # Header
    st.title("🎨 SA - منصة تحويل النصوص إلى وسائط متعددة")
    st.markdown("---")

    # Sidebar for API configuration
    with st.sidebar:
        st.header("⚙️ الإعدادات")

        # API Keys section
        with st.expander("🔑 مفاتيح API", expanded=False):
            openai_key = st.text_input(
                "OpenAI API Key",
                type="password",
                value=config.openai_api_key or "",
                help="مطلوب للاقتراحات الذكية",
            )
            replicate_key = st.text_input(
                "Replicate API Token",
                type="password",
                value=config.replicate_api_key or "",
                help="مطلوب لتوليد الصور والفيديو",
            )
            elevenlabs_key = st.text_input(
                "ElevenLabs API Key",
                type="password",
                value=config.elevenlabs_api_key or "",
                help="مطلوب لتحويل النص إلى صوت عالي الجودة",
            )

            if st.button("💾 حفظ المفاتيح"):
                config.openai_api_key = openai_key
                config.replicate_api_key = replicate_key
                config.elevenlabs_api_key = elevenlabs_key
                st.success("✅ تم حفظ المفاتيح!")

        # Validation status
        st.subheader("📊 حالة الإعداد")
        validation = config.validate()
        st.write("OpenAI:", "✅" if validation["openai"] else "❌")
        st.write("Replicate:", "✅" if validation["replicate"] else "❌")
        st.write("ElevenLabs:", "✅" if validation["elevenlabs"] else "❌")

        st.markdown("---")
        st.markdown("### 📚 الدليل السريع")
        st.info("""
        1. أضف مفاتيح API في الأعلى
        2. اختر نوع المحتوى من التبويبات
        3. أدخل النص أو الوصف
        4. استخدم الاقتراحات الذكية
        5. اضغط على زر التوليد
        """)

    # Main tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "🖼️ توليد الصور",
            "🎬 توليد الفيديو",
            "🎤 توليد الصوت",
            "🎯 مشروع كامل",
            "📂 المعرض",
            "📚 القوالس والنصائح",
        ]
    )

    # Tab 1: Image Generation
    with tab1:
        st.header("🖼️ توليد الصور من النص")

        col1, col2 = st.columns([2, 1])

        with col1:
            prompt = st.text_area(
                "📝 اكتب وصف الصورة",
                height=100,
                placeholder="مثال: منظر طبيعي خلاب لشروق الشمس فوق الجبال...",
            )

            negative_prompt = st.text_input(
                "🚫 ما تريد تجنبه (اختياري)", placeholder="مثال: ضبابية، جودة منخفضة..."
            )

        with col2:
            width = st.selectbox("العرض", [512, 768, 1024], index=2)
            height = st.selectbox("الارتفاع", [512, 768, 1024], index=2)
            num_images = st.slider("عدد الصور", 1, 4, 1)

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button("✨ تحسين الوصف", use_container_width=True):
                if prompt and config.openai_api_key:
                    with st.spinner("جاري تحسين الوصف..."):
                        engine = SuggestionEngine(config.openai_api_key)
                        improved = engine.improve_prompt(prompt, "image")
                        st.session_state.improved_prompt = improved
                        st.success("تم التحسين!")
                        st.write(improved)
                else:
                    st.warning("أدخل نص ومفتاح OpenAI")

        with col_b:
            if st.button("💡 اقتراحات", use_container_width=True):
                if prompt and config.openai_api_key:
                    with st.spinner("جاري التفكير..."):
                        engine = SuggestionEngine(config.openai_api_key)
                        suggestions = engine.generate_variations(prompt, 3)
                        st.write("### اقتراحات:")
                        for i, sug in enumerate(suggestions, 1):
                            st.write(f"{i}. {sug}")

        with col_c:
            if st.button("🎨 توليد الصورة", type="primary", use_container_width=True):
                if not prompt:
                    st.error("الرجاء إدخال وصف للصورة")
                elif not config.replicate_api_key:
                    st.error("الرجاء إضافة مفتاح Replicate API")
                else:
                    with st.spinner("🎨 جاري توليد الصورة..."):
                        generator = ImageGenerator(config.replicate_api_key)

                        # Use improved prompt if available
                        final_prompt = st.session_state.get("improved_prompt", prompt)

                        images = generator.generate(
                            prompt=final_prompt,
                            negative_prompt=negative_prompt,
                            width=width,
                            height=height,
                            num_outputs=num_images,
                        )

                        if images:
                            st.success(f"✅ تم توليد {len(images)} صورة!")

                            # Save and display images
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            for i, img_url in enumerate(images):
                                save_path = f"{config.output_dir}/image_{timestamp}_{i}.png"
                                saved = generator.download_image(img_url, save_path)

                                if saved:
                                    st.session_state.generated_images.append(saved)
                                    st.image(saved, caption=f"صورة {i+1}")
                        else:
                            st.error("فشل توليد الصورة")

    # Tab 2: Video Generation
    with tab2:
        st.header("🎬 توليد الفيديو")

        video_mode = st.radio("اختر طريقة التوليد:", ["من نص مباشر", "عرض شرائح من صور"])

        if video_mode == "من نص مباشر":
            video_prompt = st.text_area(
                "📝 وصف الفيديو",
                height=100,
                placeholder="مثال: فيديو لموجات البحر الهادئة...",
            )
            duration = st.slider("المدة (ثواني)", 3, 10, 5)

            if st.button("🎬 توليد الفيديو", type="primary"):
                if not video_prompt:
                    st.error("أدخل وصف الفيديو")
                elif not config.replicate_api_key:
                    st.error("أضف مفتاح Replicate API")
                else:
                    with st.spinner("جاري توليد الفيديو... قد يستغرق دقيقة"):
                        generator = VideoGenerator(config.replicate_api_key)
                        video_url = generator.generate_from_text(video_prompt, duration)

                        if video_url:
                            st.success("✅ تم توليد الفيديو!")
                            st.video(video_url)
                        else:
                            st.error("فشل توليد الفيديو")

        elif video_mode == "عرض شرائح من صور":
            st.info("قم بتوليد صور أولاً من تبويب 'توليد الصور'")

            if st.session_state.generated_images:
                st.write(f"لديك {len(st.session_state.generated_images)} صورة")

                duration_per_image = st.slider("مدة كل صورة (ثواني)", 2, 5, 3)

                if st.button("📹 إنشاء عرض الشرائح"):
                    with st.spinner("جاري إنشاء الفيديو..."):
                        generator = VideoGenerator()
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        output_path = f"{config.output_dir}/slideshow_{timestamp}.mp4"

                        video_path = generator.create_slideshow(
                            st.session_state.generated_images,
                            duration_per_image,
                            output_path,
                        )

                        if video_path:
                            st.success("✅ تم إنشاء الفيديو!")
                            st.video(video_path)
                            st.session_state.generated_videos.append(video_path)
            else:
                st.warning("لا توجد صور متاحة")

    # Tab 3: Audio Generation
    with tab3:
        st.header("🎤 تحويل النص إلى صوت")

        text_to_speech = st.text_area(
            "📝 النص المراد تحويله لصوت", height=150, placeholder="اكتب النص هنا..."
        )

        col1, col2 = st.columns(2)
        with col1:
            voice_name = st.selectbox("اختر الصوت", ["Adam", "Bella", "Antoni", "Rachel", "Domi"])

        with col2:
            audio_model = st.selectbox(
                "نموذ الصوت", ["eleven_multilingual_v2", "eleven_monolingual_v1"]
            )

        if st.button("🎤 توليد الصوت", type="primary"):
            if not text_to_speech:
                st.error("أدخل نص")
            else:
                with st.spinner("جاري توليد الصوت..."):
                    generator = AudioGenerator(config.elevenlabs_api_key)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_path = f"{config.output_dir}/audio_{timestamp}.mp3"

                    audio_path = generator.generate_speech(
                        text_to_speech, voice_name, audio_model, output_path
                    )

                    if audio_path and os.path.exists(audio_path):
                        st.success("✅ تم توليد الصوت!")
                        st.audio(audio_path)
                        st.session_state.generated_audio.append(audio_path)
                    else:
                        st.error("فشل توليد الصوت")

    # Tab 4: Complete Project
    with tab4:
        st.header("🎯 إنشاء مشروع كامل")
        st.write("قم بإنشاء فيديو كامل مع صور وصوت وموسيقى")

        project_idea = st.text_area(
            "💡 فكرة المشروع",
            height=100,
            placeholder="مثال: فيديو عن جمال الطبيعة في فصل الربيع...",
        )

        if st.button("✨ توليد سيناريو", use_container_width=True):
            if project_idea and config.openai_api_key:
                with st.spinner("جاري إنشاء السيناريو..."):
                    engine = SuggestionEngine(config.openai_api_key)
                    script = engine.generate_script_from_idea(project_idea)
                    st.session_state.project_script = script

                    st.success("✅ تم إنشاء السيناريو!")
                    for i, scene in enumerate(script, 1):
                        with st.expander(f"المشهد {i}"):
                            st.write("**المرئيات:**", scene["visual"])
                            st.write("**النص:**", scene["narration"])
            else:
                st.warning("أدخل فكرة المشروع ومفتاح OpenAI")

        if st.session_state.project_script:
            st.divider()
            st.subheader("🎬 تنفيذ المشروع")
            st.info("قريباً: ستقوم المنصة بتوليد كل المكونات تلقائياً")

    # Tab 5: Gallery
    with tab5:
        st.header("📂 معرض الأعمال")

        st.subheader("🖼️ الصور")
        if st.session_state.generated_images:
            cols = st.columns(3)
            for i, img_path in enumerate(st.session_state.generated_images):
                with cols[i % 3]:
                    st.image(img_path, use_container_width=True)
                    with open(img_path, "rb") as f:
                        st.download_button(
                            "⬇️ تحميل",
                            data=f.read(),
                            file_name=os.path.basename(img_path),
                            key=f"img_{i}",
                        )
        else:
            st.info("لا توجد صور بعد")

        st.divider()
        st.subheader("🎬 الفيديوهات")
        if st.session_state.generated_videos:
            for i, video_path in enumerate(st.session_state.generated_videos):
                st.video(video_path)
                with open(video_path, "rb") as f:
                    st.download_button(
                        "⬇️ تحميل",
                        data=f.read(),
                        file_name=os.path.basename(video_path),
                        key=f"vid_{i}",
                    )
        else:
            st.info("لا توجد فيديوهات بعد")

        st.divider()
        st.subheader("🎤 الصوتيات")
        if st.session_state.generated_audio:
            for i, audio_path in enumerate(st.session_state.generated_audio):
                st.audio(audio_path)
                with open(audio_path, "rb") as f:
                    st.download_button(
                        "⬇️ تحميل",
                        data=f.read(),
                        file_name=os.path.basename(audio_path),
                        key=f"aud_{i}",
                    )
        else:
            st.info("لا توجد صوتيات بعد")

    # Tab 6: Templates and Tips
    with tab6:
        show_templates_and_tips()


if __name__ == "__main__":
    main()
