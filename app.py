import os
import json
import streamlit as st
import google.generativeai as genai
from datetime import datetime, timedelta
from logger_json import save_history_json, read_history_json
from dotenv import load_dotenv

# 🌐 Load environment
load_dotenv()
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 📊 Load user data
USER_FILE = "admin_data/users.json"
if os.path.exists(USER_FILE):
    with open(USER_FILE, "r", encoding="utf-8") as f:
        user_data = json.load(f)
else:
    user_data = {}

# 🔑 Validate user
def validate_user(username):
    username = username.lower()
    return user_data.get(username)

# 📂 Load all history and group by time
def load_all_history(username):
    """Đọc toàn bộ history và phân nhóm Today, Yesterday, Last 7 Days."""
    history_dir = os.path.join("history", username)
    if not os.path.exists(history_dir):
        return {"Today": [], "Yesterday": [], "Last 7 Days": []}

    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    last_7_days = today - timedelta(days=7)

    groups = {
        "Today": [],
        "Yesterday": [],
        "Last 7 Days": [],
    }

    for filename in os.listdir(history_dir):
        if filename.endswith(".json"):
            date_str = filename.replace(".json", "")
            try:
                file_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                continue  # Skip file name sai định dạng

            # Phân nhóm
            if file_date == today:
                group_name = "Today"
            elif file_date == yesterday:
                group_name = "Yesterday"
            elif last_7_days <= file_date < yesterday:
                group_name = "Last 7 Days"
            else:
                continue  # Bỏ qua file quá cũ

            # Đọc file
            try:
                with open(os.path.join(history_dir, filename), "r", encoding="utf-8") as f:
                    data = json.load(f)
                    groups[group_name].extend(data)
            except json.JSONDecodeError:
                continue

    return groups

# 🌐 Page setup
st.set_page_config(page_title="Gemini Prompt Web App", page_icon="🌟", layout="wide")

# 📢 Header
st.title("🌟 Gemini Prompt Web App with RBAC")
st.caption("Trải nghiệm Gemini API qua Web App tự xây dựng")

# 📦 Sidebar info
if "username" in st.session_state:
    with st.sidebar:
        st.info("📦 Dự án: Gemini CLI & Web Prompt Lab")
        st.info("🔖 Phiên bản: v2.9.2 (Milestone 2.4)")
        st.info("👨‍🏫 Tác giả: Henry Võ")

# 🛂 Login hoặc Welcome
if "username" not in st.session_state:
    st.subheader("🔑 Đăng nhập hệ thống")

    with st.form("login_form", clear_on_submit=True):
        username_input = st.text_input("👤 Tên người dùng:")
        submitted = st.form_submit_button("🔓 Đăng nhập")

        if submitted:
            user_info = validate_user(username_input)
            if user_info:
                st.session_state.username = username_input
                st.session_state.role = user_info.get("role", "user")
                st.success(f"Xin chào {username_input} ({st.session_state.role})")
                st.rerun()
            else:
                st.error("❌ Username không tồn tại. Vui lòng liên hệ Admin!")
else:
    username = st.session_state.username
    role = st.session_state.role

    st.success(f"👋 Xin chào, {username}! (Role: {role})")

    # 📋 Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "💬 Gửi Prompt",
        "📄 Lịch sử (Ngày)",
        "🕛 Lịch sử gần đây",
        "📅 Lịch sử nhóm theo thời gian"  # <--- Tab mới milestone 2.4
    ])

    # --- Tab 1: Gửi Prompt ---
    with tab1:
        st.header("💬 Gửi Prompt tới Gemini")
        temperature = st.slider("🎛️ Độ sáng tạo", 0.0, 1.0, 0.7, step=0.01)

        if st.session_state.get("clear_prompt"):
            st.session_state["prompt_text"] = ""
            st.session_state["clear_prompt"] = False

        prompt = st.text_area("📃 Nhập nội dung prompt:", height=200, key="prompt_text")

        col1, col2 = st.columns([1, 5])
        with col1:
            send_prompt = st.button("🚀 Gửi Prompt")

        if send_prompt and prompt:
            try:
                model = genai.GenerativeModel("gemini-1.5-flash-latest")
                response = model.generate_content(prompt)
                result = response.text

                save_history_json(prompt, result, temperature, username=username)

                st.session_state["last_prompt_result"] = result
                st.session_state["clear_prompt"] = True

                st.rerun()

            except Exception as e:
                st.error(f"❌ Lỗi khi gọi Gemini: {e}")

        if "last_prompt_result" in st.session_state:
            st.success("✅ Kết quả phản hồi từ Gemini:")
            st.code(st.session_state["last_prompt_result"], language="markdown")

    # --- Tab 2: Xem Lịch sử theo ngày ---
    with tab2:
        st.header("📅 Lịch sử hỏi đáp theo ngày")
        selected_date = st.date_input("🗓️ Chọn ngày:", format="YYYY-MM-DD")
        selected_date_str = selected_date.strftime("%Y-%m-%d")

        history = read_history_json(username, selected_date_str)
        st.info(f"🔎 Tổng lượt hỏi ngày {selected_date_str}: **{len(history)}**")

        for idx, entry in enumerate(history, start=1):
            with st.expander(f"📄 Prompt #{idx} - {entry['timestamp']}"):
                st.markdown(f"**Prompt:** {entry['prompt']}")
                result_text = entry.get('result')
                if result_text:
                    st.code(result_text, language="markdown")
                else:
                    st.warning("⚠️ Prompt này chưa có kết quả trả về.")

    # --- Tab 3: Placeholder milestone 2.5 ---
    with tab3:
        st.header("🕛 Lịch sử gần đây (Coming soon 🚧)")
        st.info("🚧 Đang chuẩn bị milestone 2.5")

    # --- Tab 4: Lịch sử nhóm theo thời gian ---
    with tab4:
        st.header("📅 Lịch sử nhóm theo Today, Yesterday, Last 7 Days")
        groups = load_all_history(username)

        for group_name, prompts in groups.items():
            with st.expander(f"▶️ {group_name} ({len(prompts)} prompt)", expanded=False):
                if not prompts:
                    st.info("⛔ Không có dữ liệu.")
                else:
                    for idx, entry in enumerate(prompts, start=1):
                        st.markdown(f"**📄 Prompt #{idx} - {entry['timestamp']}**")
                        st.markdown(f"**Prompt:** {entry['prompt']}")
                        result_text = entry.get('result')
                        if result_text:
                            st.code(result_text, language="markdown")
                        else:
                            st.warning("⚠️ Prompt này chưa có kết quả trả về.")
                        st.divider()
