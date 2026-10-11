# 📘 LEARNING LOG - AI ENGINEER JOURNEY

> **Người học:** Nguyễn Ngọc Tú
> **Bắt đầu:** 2026-10-11
> **Mục tiêu:** Intern SE 3.0 / AI Engineer vào năm 4
> **Thời gian học:** 2-3 tiếng/ngày
> **Repo:** https://github.com/NguyenNgocTu041105/finance-ai-agent

---

## 📊 TỔNG QUAN TIẾN ĐỘ

| Giai đoạn | Trạng thái | Bắt đầu | Hoàn thành |
| :--- | :--- | :--- | :--- |
| 1. LLM API & Multi-Model Fallback | 🔄 | 2026-10-11 | |
| 2. RAG nâng cao cho BCTC | ⏸️ | | |
| 3. AI Agent & Observability | ⏸️ | | |
| 4. Backend FastAPI | ⏸️ | | |
| 5. Frontend React | ⏸️ | | |
| 6. Tích hợp & Hoàn thiện | ⏸️ | | |
| 7. Docker, CI/CD & Deploy | ⏸️ | | |
| 8. Nâng cao & Backtesting | ⏸️ | | |

**Tiến độ tổng:** 5/54 buổi ≈ 9%

---

## 📅 NHẬT KÝ CHI TIẾT

<!-- Ghi log mới NHẤT lên trên cùng -->

### 2026-10-11 (Thứ Bảy) - Buổi 1 đến 5

**⏱️ Tổng thời gian:** ~4 tiếng
**🎯 Mục tiêu:** Setup project, Git, chạy Gemini API

---

#### Buổi 1: Setup project + venv

**✅ Đã làm:**
- Tạo `D:\AI_Projects\finance-ai-agent\backend`
- Tạo venv với `python -m venv venv`
- Cài `google-genai`, `python-dotenv`, `litellm`

**❌ Lỗi gặp phải:**
- `bash: D:: command not found` → Git Bash dùng `cd /d/AI_Projects` thay vì `D:`

**💡 Bài học:**
- Git Bash khác CMD/PowerShell: dùng `/d/` thay vì `D:`
- Activate venv trong Git Bash: `source venv/Scripts/activate`

---

#### Buổi 2: Tạo file `.env`, `.gitignore`, `gemini_chat.py`

**✅ Đã làm:**
- Tạo `.env` chứa `GEMINI_API_KEY`
- Tạo `.gitignore` (bỏ qua `.env`, `venv/`)
- Tạo `gemini_chat.py`
- Antigravity tự động tạo thêm `.env.example`, `README.md`

**💡 Bài học:**
- Antigravity có khả năng bảo mật API key tự động (tạo `.env.example`, sửa code không hardcode key)

---

#### Buổi 3: Chạy thử Gemini API

**✅ Đã làm:**
- Chạy `python gemini_chat.py` lần đầu
- Gặp lỗi 404 model `gemini-2.5-flash`
- Đổi sang `gemini-3.8-flash` → chạy thành công

**❌ Lỗi gặp phải:**
- `404 NOT_FOUND: model gemini-2.5-flash is no longer available to new users`

**💡 Bài học:**
- Model Gemini cũ có thể bị khóa bất kỳ lúc nào
- Luôn kiểm tra model còn khả dụng trước khi viết code

---

#### Buổi 4: Setup Git + GitHub repo

**✅ Đã làm:**
- Tạo repo GitHub: `https://github.com/NguyenNgocTu041105/finance-ai-agent`
- Push commit 1: `feat: initial project setup with gemini chat bot and learning log`
- Phát hiện thư mục lồng `finance-ai-agent/finance-ai-agent/`
- Di chuyển `.git` xuống `finance-ai-agent/`
- Push commit 2: `refactor: move project files to repo root`

**❌ Lỗi gặp phải:**
- Repo GitHub có thư mục lồng do `git init` ở sai cấp
- README.md không được nhận diện vì nằm trong thư mục con

**💡 Bài học:**
- `git init` phải ở đúng cấp thư mục (không lồng)
- Cấu trúc repo chuẩn: README.md, .gitignore ở root
- Khi phát hiện sai, dùng `mv .git` để di chuyển

---

#### Buổi 5: Gặp lỗi 429 quota Gemini

**✅ Đã làm:**
- Chat được vài câu với `gemini-3.8-flash`
- Gặp lỗi 429 sau ~20 requests

**❌ Lỗi gặp phải:**
- `429 RESOURCE_EXHAUSTED: Quota exceeded, limit 20 requests/day for gemini-3.8-flash`
- Phải chờ 7h34m mới dùng lại

**💡 Bài học:**
- Gemini free tier chỉ cho **20 requests/ngày** → quá ít cho dev
- Đây chính là **lý do cần Multi-Model Fallback**
- Không nên phụ thuộc vào 1 provider duy nhất
- Cần đăng ký thêm Groq (14,400 req/ngày) và Together AI

**➡️ Bước tiếp theo:**
- Buổi 6: Đăng ký Groq API + Together AI
- Buổi 7: Viết LiteLLM fallback logic
- Buổi 8: Test fallback

---