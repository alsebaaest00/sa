"""Projects and statistics management for Streamlit UI"""

import streamlit as st

from sa.utils import project_manager


def init_session_state():
    """Initialize session state"""
    if "current_project_id" not in st.session_state:
        st.session_state.current_project_id = None
    if "refresh_projects" not in st.session_state:
        st.session_state.refresh_projects = False


def show_projects_management():
    """Show projects management interface"""
    st.header("📁 إدارة المشاريع")

    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 المشاريع", "➕ مشروع جديد", "📊 الإحصائيات"])

    with tab1:
        show_projects_list()

    with tab2:
        show_create_project()

    with tab3:
        show_statistics()


def show_projects_list():
    """Display list of projects"""
    st.subheader("قائمة المشاريع")

    projects = project_manager.list_projects()

    if not projects:
        st.info("لا توجد مشاريع بعد. قم بإنشاء مشروع جديد!")
        return

    # Create columns for project cards
    for project in projects:
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            with st.container(border=True):
                st.write(f"**{project['name']}**")
                st.caption(project.get("description", "بدون وصف"))

                # Show project info
                created = project["created_at"]
                st.caption(f"📅 أنشئ: {created[:10]}")

                # Get generations count
                generations = project_manager.get_generations(project["id"])
                st.caption(f"📦 {len(generations)} عملية")

        with col2:
            if st.button("📂 فتح", key=f"open_{project['id']}"):
                st.session_state.current_project_id = project["id"]
                st.rerun()

        with col3:
            if st.button("🗑️", key=f"delete_{project['id']}"):
                project_manager.delete_project(project["id"])
                st.session_state.refresh_projects = True
                st.rerun()

    # Show current project details if selected
    if st.session_state.current_project_id:
        st.divider()
        show_project_details(st.session_state.current_project_id)


def show_project_details(project_id: int):
    """Show detailed project view"""
    project = project_manager.get_project(project_id)

    if not project:
        st.error("المشروع غير موجود")
        return

    st.subheader(f"📂 {project['name']}")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**الوصف:**")
        st.write(project.get("description", "بدون وصف"))

    with col2:
        st.write("**المعلومات:**")
        st.write(f"- أنشئ: {project['created_at'][:10]}")
        st.write(f"- آخر تحديث: {project['updated_at'][:10]}")

    # Show generations
    st.write("---")
    st.write("**العمليات:**")

    generations = project_manager.get_generations(project_id)

    if generations:
        for gen in generations:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.write(f"**{gen['type'].upper()}**: {gen['prompt'][:50]}...")
                    st.caption(f"📁 {gen['file_path']}")
                    st.caption(f"⏱️ {gen['duration']:.2f}s • {gen['created_at'][:19]}")

                with col2:
                    if st.button("📥", key=f"gen_{gen['id']}", help="تحميل"):
                        st.info("سيتم التحميل قريباً!")
    else:
        st.info("لا توجد عمليات في هذا المشروع")

    # Export button
    if st.button("💾 تصدير المشروع"):
        export_data = project_manager.export_project(project_id)
        st.download_button(
            label="تحميل JSON",
            data=export_data,
            file_name=f"{project['name']}.json",
            mime="application/json",
        )


def show_create_project():
    """Show create project form"""
    st.subheader("➕ إنشاء مشروع جديد")

    with st.form("create_project_form"):
        name = st.text_input("اسم المشروع", placeholder="مثال: فيديو الترويج")
        description = st.text_area("الوصف", placeholder="وصف المشروع...")

        submitted = st.form_submit_button("✅ إنشاء المشروع", type="primary")

        if submitted:
            if not name:
                st.error("الرجاء إدخال اسم المشروع")
            else:
                project_id = project_manager.create_project(name, description)
                st.success(f"✅ تم إنشاء المشروع برقم #{project_id}")
                st.session_state.current_project_id = project_id
                st.rerun()


def show_statistics():
    """Show statistics dashboard"""
    st.subheader("📊 الإحصائيات")

    # Get statistics
    stats = project_manager.get_statistics()
    all_stats = project_manager.get_all_statistics()

    # Show today's stats
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("صور", stats.get("images_count", 0), "📷")

    with col2:
        st.metric("فيديوهات", stats.get("videos_count", 0), "🎬")

    with col3:
        st.metric("صوتيات", stats.get("audio_count", 0), "🎤")

    with col4:
        st.metric("الوقت (دقائق)", round(stats.get("total_time", 0) / 60, 2), "⏱️")

    st.divider()

    # Show all projects count
    projects = project_manager.list_projects()
    st.metric("إجمالي المشاريع", len(projects))

    st.divider()

    # Show statistics over time
    if all_stats:
        st.write("**الإحصائيات اليومية:**")

        # Prepare data for chart
        dates = [stat["date"] for stat in all_stats[:10]]
        images = [stat["images_count"] for stat in all_stats[:10]]
        videos = [stat["videos_count"] for stat in all_stats[:10]]

        # Create chart data
        chart_data = {"التاريخ": dates, "صور": images, "فيديوهات": videos}

        st.bar_chart(chart_data, x="التاريخ")

    else:
        st.info("لا توجد إحصائيات بعد. ابدأ بإنشاء محتوى!")
