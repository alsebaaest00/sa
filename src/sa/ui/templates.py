"""UI for templates and quick references"""

import streamlit as st

from sa.utils.templates import BestPractices, ContentTips, QuickReferences, Templates


def show_templates_and_tips():
    """Show templates and quick references section"""
    st.header("📚 القوالب والمراجع السريعة")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📋 القوالب", "💡 النصائح", "🎤 الأصوات", "✨ أفضل الممارسات"]
    )

    with tab1:
        show_templates()

    with tab2:
        show_tips()

    with tab3:
        show_voices()

    with tab4:
        show_best_practices()


def show_templates():
    """Display available templates"""
    st.subheader("📋 قوالب جاهزة")
    st.write("اختر قالباً جاهزاً لتسريع عملية الإنشاء")

    templates = Templates.list_templates()

    cols = st.columns(2)
    for idx, template in enumerate(templates):
        with cols[idx % 2]:
            with st.container(border=True):
                st.markdown(f"### {template['name']}")
                st.write(f"*{template['description']}*")

                if st.button(f"استخدام {template['name']}", key=f"template_{template['id']}"):
                    template_data = Templates.get_template(template["id"])
                    st.session_state.template_data = template_data
                    st.session_state.selected_template = template["name"]
                    st.success(f"تم اختيار {template['name']}")

    # Show selected template details
    if "selected_template" in st.session_state:
        st.divider()
        st.subheader(f"✨ {st.session_state.selected_template}")

        template_data = st.session_state.template_data

        with st.expander("🖼️ نص الصورة المقترح"):
            st.text_area(
                "نص الصورة:",
                value=template_data.get("image_prompt", ""),
                height=100,
                disabled=True,
            )

        with st.expander("🎬 نص الفيديو المقترح"):
            st.text_area(
                "نص الفيديو:",
                value=template_data.get("video_prompt", ""),
                height=100,
                disabled=True,
            )

        with st.expander("🎤 النص الصوتي المقترح"):
            st.text_area(
                "النص الصوتي:",
                value=template_data.get("audio_text", ""),
                height=100,
                disabled=True,
            )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("نسخ النصوص"):
                st.session_state.image_prompt = template_data.get("image_prompt", "")
                st.session_state.video_prompt = template_data.get("video_prompt", "")
                st.session_state.audio_text = template_data.get("audio_text", "")
                st.success("✅ تم نسخ النصوص")

        with col2:
            if st.button("مسح الاختيار"):
                if "selected_template" in st.session_state:
                    del st.session_state.selected_template
                if "template_data" in st.session_state:
                    del st.session_state.template_data
                st.rerun()


def show_tips():
    """Display content creation tips"""
    st.subheader("💡 نصائح الإنشاء")

    tip_category = st.selectbox(
        "اختر نوع المحتوى:",
        ["image", "video", "audio"],
        format_func=lambda x: {
            "image": "🖼️ الصور",
            "video": "🎬 الفيديو",
            "audio": "🎤 الصوت",
        }[x],
    )

    tips = ContentTips.get_tips(tip_category)

    st.markdown("### نصائح مهمة:")
    for i, tip in enumerate(tips, 1):
        st.markdown(f"{i}. {tip}")

    # Show best practices
    st.divider()
    st.markdown("### 📖 اقرأ المزيد:")

    practice_type = st.selectbox(
        "اختر موضوع الممارسة:",
        ["naming", "organization", "quality"],
        format_func=lambda x: {
            "naming": "تسمية المشاريع",
            "organization": "تنظيم المشاريع",
            "quality": "ضمان الجودة",
        }[x],
    )

    practice = BestPractices.get_practice(practice_type)
    st.markdown(f"#### {practice['description']}")

    for tip in practice["tips"]:
        st.markdown(f"- {tip}")


def show_voices():
    """Display voice options and tips"""
    st.subheader("🎤 الأصوات المتاحة")

    voices = QuickReferences.list_voices()

    col1, col2 = st.columns(2)

    for idx, voice in enumerate(voices):
        with col1 if idx % 2 == 0 else col2:
            with st.container(border=True):
                st.markdown(f"### {voice['name']}")
                st.markdown(f"**النوع:** {voice['gender']}")
                st.markdown(f"**الأسلوب:** {voice['tone']}")
                st.markdown(f"**السرعة:** {voice['speed']}")

                if st.button(f"اختر {voice['name']}", key=f"voice_{voice['name']}"):
                    st.session_state.selected_voice = voice["name"]
                    st.success(f"تم اختيار صوت {voice['name']}")

    # Prompt suggestions
    st.divider()
    st.subheader("📝 اقتراحات النصوص")

    category = st.selectbox(
        "اختر فئة:",
        ["photography", "illustration", "animation"],
        format_func=lambda x: {
            "photography": "📸 التصوير",
            "illustration": "🎨 الرسومات",
            "animation": "✨ الرسوم المتحركة",
        }[x],
    )

    suggestions = QuickReferences.get_prompt_suggestions(category)

    for i, suggestion in enumerate(suggestions, 1):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"{i}. {suggestion}")
        with col2:
            if st.button("📋", key=f"copy_{category}_{i}", help="نسخ"):
                st.session_state.image_prompt = suggestion
                st.toast("✅ تم النسخ!")


def show_best_practices():
    """Display best practices guide"""
    st.subheader("✨ أفضل الممارسات")

    st.markdown("""
    اتبع هذه الممارسات لضمان جودة المشاريع:
    """)

    practices_to_show = ["naming", "organization", "quality"]

    for practice_name in practices_to_show:
        practice = BestPractices.get_practice(practice_name)

        with st.expander(f"📌 {practice['description']}"):
            for i, tip in enumerate(practice["tips"], 1):
                st.markdown(f"{i}. {tip}")

    # Quick checklist
    st.divider()
    st.subheader("✅ قائمة التحقق")

    checklist = {
        "هل اخترت القالب المناسب؟": False,
        "هل تابعت نصائح الإنشاء؟": False,
        "هل راجعت النتائج؟": False,
        "هل وثقت المشروع؟": False,
        "هل احتفظت بنسخة احتياطية؟": False,
    }

    checked = 0
    for item, _ in checklist.items():
        if st.checkbox(item):
            checked += 1

    if checked > 0:
        progress = checked / len(checklist)
        st.progress(progress)
        st.caption(f"تقدم: {checked}/{len(checklist)}")
