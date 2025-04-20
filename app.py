import streamlit as st
from gemini_client import ask_gemini
from logger_json import save_history_json
from datetime import datetime

# ✅ Cấu hình trang
st.set_page_config(page_title="Gemini Web App", page_icon="✨")
st.title("✨ Gemini Prompt Web App")

# ✅ Thông tin dự án
st.markdown("""
<style>
.info-box {
    background-color: #f1f3f6;
    border-radius: 0.5rem;
    padding: 1rem;
    margin-bottom: 1rem;
}
</style>

<div class='info-box'>
    <h4>📦 Dự án: <strong>Gemini CLI & Web Prompt Lab</strong></h4>
    <p>🔢 Phiên bản: <code>v2.2</code></p>
    <p>👨‍💻 Tác giả: <strong>Henry Võ</strong></p>
</div>
""", unsafe_allow_html=True)

# ✅ Nhập tên người dùng
username = st.text_input("👤 Nhập tên người dùng (bắt buộc):", value="", key="username_input")
if not username.strip():
    st.warning("⚠️ Vui lòng nhập tên người dùng để tiếp tục.")
    st.stop()

st.markdown(f"Xin chào, **{username}**! Nhập prompt bên dưới:")

# ✅ Điều chỉnh độ sáng tạo
temperature = st.slider("🎛️ Độ sáng tạo", 0.0, 1.0, 0.7, 0.1)

# ✅ Nhập Prompt qua Form
with st.form("gemini_form", clear_on_submit=True):
    prompt = st.text_area("📝 Nhập prompt:", height=150)
    submitted = st.form_submit_button("🚀 Gửi prompt")

# ✅ Xử lý kết quả từ Gemini
if submitted:
    if prompt.strip() == "":
        st.warning("⚠️ Bạn cần nhập prompt trước khi gửi.")
    else:
        with st.spinner("⏳ Đang gửi đến Gemini..."):
            try:
                result = ask_gemini(prompt, temperature)

                st.success("✅ Kết quả trả về từ Gemini:")

                # ✅ Hiển thị kết quả có nút copy ⧉
                st.code(result, language="markdown")
                st.caption("📎 Mẹo: Bấm vào biểu tượng ⧉ góc phải để sao chép kết quả")

                # ✅ Hiển thị lại dạng không tràn dòng
                st.markdown(f"""
                <div style='white-space: pre-wrap; word-wrap: break-word; background-color: #f8f9fa; padding: 1rem; border-radius: 5px; font-family: monospace; color: #212529'>
                {result}
                </div>
                """, unsafe_allow_html=True)

                # ✅ Tạo tên file tải về
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"gemini_result_{timestamp}.txt"

                # ✅ Nút tải xuống
                st.download_button(
                    label="💾 Tải kết quả (.txt)",
                    data=result,
                    file_name=filename,
                    mime="text/plain",
                    help="Tải nội dung vừa tạo thành file văn bản"
                )

                # ✅ Ghi log JSON
                save_history_json(prompt, result, temperature, username=username)

            except Exception as e:
                st.error(f"❌ Lỗi khi gọi Gemini: {e}")
