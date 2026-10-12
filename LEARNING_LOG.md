# Learning Log - Finance AI Agent

- **Dev:** Nguyễn Ngọc Tú (MIS Năm 3)
- **Target:** Intern AI Engineer / SE
- **Repo:** https://github.com/NguyenNgocTu041105/finance-ai-agent

---

### 12/10/2026: Multi-Model Fallback & Xử lý lỗi hệ thống

- **Thời gian:** ~3h
- **Mục tiêu:** Dùng LiteLLM kết nối Gemini, Groq, OpenRouter để tự động chuyển model khi lỗi.
- **Vấn đề 1 (Lỗi 404):** Groq gỡ `llama-3.3-70b-versatile`, OpenRouter cắt bản `:free`.
  - *Xử lý:* Đưa toàn bộ tên model ra file `.env` để cấu hình linh hoạt, không hardcode trong code.
- **Vấn đề 2 (Lỗi 503):** Server Gemini bị quá tải tạm thời, không phải hết token.
  - *Xử lý:* Thêm logic retry thông minh (Exponential Backoff): chỉ retry lỗi tạm thời (503, timeout), gặp lỗi vĩnh viễn (401, 404) thì ngắt và fallback ngay sang model khác.
- **Vấn đề 3 (Mất env):** `load_dotenv()` không nhận diện được file `.env` khi chạy từ thư mục gốc.
  - *Xử lý:* Đổi sang `Path(__file__).resolve().parent / ".env"`.
- **Kết quả:** Fallback hoạt động, chat không bị gián đoạn khi 1 model lỗi.
- **Next:** Function Calling với vnstock.

---

### 11/10/2026: Khởi tạo Project & Setup ban đầu

- **Thời gian:** ~2h
- **Mục tiêu:** Dựng môi trường, kết nối Git và test Gemini API.
- **Đã làm:**
  - Setup repo GitHub, cấu hình `venv`, `.gitignore` và `.env` để bảo mật API Key.
  - Viết `gemini_chat.py` kết nối thành công với `gemini-3.8-flash`.
- **Vấn đề (Lỗi 429):** Gemini Free Tier bị giới hạn request/ngày, dính `RESOURCE_EXHAUSTED` sau khoảng 20 lượt chat.
  - *Bài học:* Bắt buộc phải có giải pháp Multi-Model Fallback để hệ thống không bị gián đoạn.
- **Kết quả:** Gemini chạy được nhưng bị giới hạn quota.
- **Next:** Nghiên cứu Multi-Model Fallback.