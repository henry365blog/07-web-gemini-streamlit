# 📋 Tính năng của ứng dụng Gemini Prompt Lab

## 🧱 Thông tin cơ bản
- Dự án: Gemini CLI & Web Prompt Lab
- Phiên bản hiện tại: v2.2
- Tác giả: Henry Võ

## 🎯 Chức năng chính

### Giao diện Web (Streamlit)
- [x] Nhập prompt văn bản tùy ý
- [x] Điều chỉnh độ sáng tạo (temperature)
- [x] Nhập tên người dùng (không cần tài khoản)
- [x] Gửi prompt tới Gemini API (Google Generative AI)
- [x] Hiển thị kết quả rõ ràng
- [x] Copy nhanh nội dung trả về
- [x] Tải kết quả dưới dạng file `.txt` có timestamp

### Ghi log
- [x] Lưu lịch sử theo từng user/ngày
- [x] Ghi thông tin prompt, response, thời gian, độ sáng tạo
- [ ] (Todo) Hiển thị lịch sử gần đây trong giao diện Web

### Bảo mật
- [x] Không lưu key trong mã nguồn
- [x] Dùng biến môi trường hoặc secrets.toml

## ☁️ Deploy
- [x] Triển khai miễn phí trên Streamlit Cloud
- [ ] (Option) Replit, Render, GCP (triển khai nâng cao)

## 📌 Ghi chú mở rộng
- [ ] Cho phép nhiều lượt chat (multi-turn)
- [ ] Giao diện lịch sử, lọc từ khóa
- [ ] Ghim prompt yêu thích, export log

---

✅ Cập nhật lần cuối: 2025-04-21
