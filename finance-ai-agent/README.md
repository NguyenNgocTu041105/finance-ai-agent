# 📈 Finance AI Agent

Dự án trợ lý AI tài chính cá nhân & phân tích báo cáo tài chính sử dụng Gemini API, LiteLLM, và các kỹ thuật RAG / AI Agent nâng cao.

## 🚀 Tính năng dự kiến & Lộ trình
- **Giai đoạn 1**: LLM API & Multi-Model Fallback (Gemini + LiteLLM)
- **Giai đoạn 2**: RAG nâng cao cho Báo cáo tài chính (BCTC)
- **Giai đoạn 3**: AI Agent & Observability
- **Giai đoạn 4**: Backend FastAPI
- **Giai đoạn 5**: Frontend React
- **Giai đoạn 6**: Tích hợp & Hoàn thiện
- **Giai đoạn 7**: Docker, CI/CD & Deploy
- **Giai đoạn 8**: Nâng cao & Backtesting

## 🛠️ Cài đặt & Khởi chạy (Backend)

1. **Clone repository:**
   ```bash
   git clone https://github.com/NguyenNgocTu041105/finance-ai-agent.git
   cd finance-ai-agent/backend
   ```

2. **Tạo virtual environment & kích hoạt:**
   ```bash
   python -m venv venv
   # Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   # Git Bash:
   source venv/Scripts/activate
   ```

3. **Cài đặt thư viện:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Cấu hình môi trường:**
   Tạo file `.env` dựa trên file mẫu `.env.example`:
   ```bash
   cp .env.example .env
   ```
   Sau đó điền `GEMINI_API_KEY` của bạn vào file `.env`.

5. **Chạy thử chatbot:**
   ```bash
   python gemini_chat.py
   ```
