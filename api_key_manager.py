"""إدارة مفاتيح API - واجهة سهلة لإضافة وتحديث المفاتيح"""

import os
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="إدارة مفاتيح API", page_icon="🔑", layout="centered")

st.title("🔑 إدارة مفاتيح API")
st.markdown("---")

# Path to .env file
env_file = Path("/workspaces/sa/.env")


# Read current .env
def read_env():
    """قراءة ملف .env الحالي"""
    if env_file.exists():
        with open(env_file, encoding="utf-8") as f:
            return f.read()
    return ""


def update_env_key(key_name, new_value):
    """تحديث مفتاح معين في ملف .env"""
    content = read_env()
    lines = content.split("\n")
    updated = False

    for i, line in enumerate(lines):
        if line.startswith(f"{key_name}="):
            lines[i] = f"{key_name}={new_value}"
            updated = True
            break

    if not updated:
        lines.append(f"{key_name}={new_value}")

    with open(env_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# عرض المفاتيح الحالية
st.header("📊 المفاتيح الحالية")

current_env = read_env()
current_keys = {}

for line in current_env.split("\n"):
    if "=" in line and not line.startswith("#"):
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key in ["REPLICATE_API_TOKEN", "OPENAI_API_KEY", "ELEVENLABS_API_KEY"]:
            current_keys[key] = value

# عرض حالة المفاتيح
col1, col2, col3 = st.columns(3)

with col1:
    replicate_status = (
        "✅" if current_keys.get("REPLICATE_API_TOKEN", "").startswith("r8_") else "❌"
    )
    st.metric("Replicate", replicate_status)

with col2:
    openai_status = "✅" if current_keys.get("OPENAI_API_KEY", "").startswith("sk-") else "❌"
    st.metric("OpenAI", openai_status)

with col3:
    elevenlabs_status = (
        "✅"
        if current_keys.get("ELEVENLABS_API_KEY", "")
        and current_keys.get("ELEVENLABS_API_KEY") != "your_elevenlabs_key_here"
        else "⚠️"
    )
    st.metric("ElevenLabs", elevenlabs_status)

st.markdown("---")

# نموذج إضافة/تحديث المفاتيح
st.header("🔐 تحديث المفاتيح")

tab1, tab2, tab3 = st.tabs(["🎨 Replicate", "🤖 OpenAI", "🔊 ElevenLabs"])

with tab1:
    st.subheader("مفتاح Replicate API")
    st.info("📝 للحصول على المفتاح: https://replicate.com/account/api-tokens")

    current_replicate = current_keys.get("REPLICATE_API_TOKEN", "")
    if current_replicate:
        st.code(f"المفتاح الحالي: {current_replicate[:10]}...{current_replicate[-10:]}")

    new_replicate = st.text_input(
        "المفتاح الجديد (يبدأ بـ r8_)",
        type="password",
        key="replicate",
        placeholder="r8_...",
    )

    if st.button("💾 حفظ مفتاح Replicate", type="primary"):
        if new_replicate and new_replicate.startswith("r8_"):
            update_env_key("REPLICATE_API_TOKEN", new_replicate)
            st.success("✅ تم حفظ مفتاح Replicate بنجاح!")
            st.info("⚠️ يرجى إعادة تشغيل الخدمات لتطبيق التغييرات")
        elif new_replicate:
            st.error("❌ المفتاح يجب أن يبدأ بـ r8_")
        else:
            st.warning("⚠️ الرجاء إدخال المفتاح")

with tab2:
    st.subheader("مفتاح OpenAI API")
    st.info("📝 للحصول على المفتاح: https://platform.openai.com/api-keys")

    current_openai = current_keys.get("OPENAI_API_KEY", "")
    if current_openai:
        st.code(f"المفتاح الحالي: {current_openai[:10]}...{current_openai[-10:]}")

    new_openai = st.text_input(
        "المفتاح الجديد (يبدأ بـ sk-)",
        type="password",
        key="openai",
        placeholder="sk-...",
    )

    if st.button("💾 حفظ مفتاح OpenAI", type="primary"):
        if new_openai and new_openai.startswith("sk-"):
            update_env_key("OPENAI_API_KEY", new_openai)
            st.success("✅ تم حفظ مفتاح OpenAI بنجاح!")
            st.info("⚠️ يرجى إعادة تشغيل الخدمات لتطبيق التغييرات")
        elif new_openai:
            st.error("❌ المفتاح يجب أن يبدأ بـ sk-")
        else:
            st.warning("⚠️ الرجاء إدخال المفتاح")

with tab3:
    st.subheader("مفتاح ElevenLabs API (اختياري)")
    st.info("📝 للحصول على المفتاح: https://elevenlabs.io")
    st.warning("💡 هذا المفتاح اختياري - يمكن استخدام gTTS المجاني بدلاً منه")

    current_elevenlabs = current_keys.get("ELEVENLABS_API_KEY", "")
    if current_elevenlabs and current_elevenlabs != "your_elevenlabs_key_here":
        st.code(f"المفتاح الحالي: {current_elevenlabs[:10]}...{current_elevenlabs[-10:]}")

    new_elevenlabs = st.text_input(
        "المفتاح الجديد",
        type="password",
        key="elevenlabs",
        placeholder="مفتاح ElevenLabs...",
    )

    if st.button("💾 حفظ مفتاح ElevenLabs", type="primary"):
        if new_elevenlabs:
            update_env_key("ELEVENLABS_API_KEY", new_elevenlabs)
            st.success("✅ تم حفظ مفتاح ElevenLabs بنجاح!")
            st.info("⚠️ يرجى إعادة تشغيل الخدمات لتطبيق التغييرات")
        else:
            st.warning("⚠️ الرجاء إدخال المفتاح")

st.markdown("---")

# إرشادات إعادة التشغيل
st.header("🔄 إعادة تشغيل الخدمات")

st.code(
    """
# في Terminal:
pkill -f streamlit && pkill -f uvicorn
bash quick.sh
# ثم اختر: 2 (تشغيل الواجهة فقط)
""",
    language="bash",
)

st.info("💡 أو استخدم الأزرار أدناه:")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔴 إيقاف الخدمات"):
        os.system("pkill -f 'streamlit run' && pkill -f 'uvicorn'")
        st.success("✅ تم إيقاف الخدمات")

with col2:
    if st.button("🟢 تشغيل الخدمات"):
        st.info("🔄 جاري إعادة التشغيل... (قد يستغرق 10 ثوان)")
        os.system(
            "cd /workspaces/sa && /workspaces/sa/.venv/bin/streamlit run src/sa/ui/app.py --server.port 8501 --server.address 0.0.0.0 --server.enableXsrfProtection false --server.enableCORS false > logs/streamlit.log 2>&1 &"
        )
        os.system(
            "cd /workspaces/sa && /workspaces/sa/.venv/bin/uvicorn sa.api:app --host 0.0.0.0 --port 8000 > logs/api.log 2>&1 &"
        )
        st.success("✅ تم بدء تشغيل الخدمات")
        st.info("⏳ انتظر 5 ثوان ثم افتح الواجهة الرئيسية")
