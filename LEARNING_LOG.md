# 📘 LEARNING LOG - AI ENGINEER JOURNEY

> **Người học:** Nguyễn Ngọc Tú
> **Bắt đầu:** 2026-10-11
> **Mục tiêu:** Intern SE 3.0 / AI Engineer vào năm 4
> **Thời gian học:** 2-3 tiếng/ngày

---

## 📊 TỔNG QUAN TIẾN ĐỘ

| Giai đoạn | Trạng thái | Bắt đầu | Hoàn thành |
| :--- | :--- | :--- | :--- |
| 0. Nền tảng sinh tồn | ⏸️ | | |
| 1. LLM API & Fallback | 🔄 | 2026-10-11 | |
| 2. RAG nâng cao cho BCTC | ⏸️ | | |
| 3. AI Agent & Observability | ⏸️ | | |
| 4. Backend FastAPI | ⏸️ | | |
| 5. Frontend React | ⏸️ | | |
| 6. Tích hợp & Hoàn thiện | ⏸️ | | |
| 7. Docker, CI/CD & Deploy | ⏸️ | | |
| 8. Nâng cao & Backtesting | ⏸️ | | |

---

## 📅 NHẬT KÝ CHI TIẾT

<!-- Ghi log mới NHẤT lên trên cùng, theo mẫu dưới đây -->

### 2026-10-11 (Thứ Bảy) - Buổi 1.1, 1.2, 1.3

**⏱️ Thời gian:** 2.5 tiếng
**🎯 Mục tiêu buổi:** Setup project và chạy Gemini API lần đầu

**✅ Đã làm:**
- Tạo project tại `D:\AI_Projects\finance-ai-agent\backend`
- Tạo virtual environment với `python -m venv venv`
- Cài `google-genai`, `python-dotenv`, `litellm`
- Tạo file `.env`, `.gitignore`, `gemini_chat.py`
- Chạy thử Gemini API

**❌ Lỗi gặp phải:**
- `bash: D:: command not found` → Do dùng Git Bash, phải dùng `cd /d/AI_Projects` thay vì `D:`
- `404 NOT_FOUND model gemini-2.5-flash` → Google đã khóa model cũ cho tài khoản mới

**💡 Bài học rút ra:**
- Git Bash khác CMD/PowerShell: dùng `/d/` thay vì `D:`
- Activate venv trong Git Bash: `source venv/Scripts/activate`
- Model Gemini cũ có thể bị khóa bất kỳ lúc nào → cần Multi-Model Fallback

**❓ Câu hỏi cần giải đáp:**
- Làm sao để tự động phát hiện model nào còn khả dụng?
- LiteLLM có hỗ trợ auto-detect model không?

**➡️ Bước tiếp theo:**
- Đổi model sang `gemini-3.8-flash`
- Chạy thử lại `python gemini_chat.py`
- Sang Buổi 2: Multi-Model Fallback với LiteLLM

---