# Learning Log - Finance AI Agent

- **Dev:** Nguyễn Ngọc Tú (MIS Năm 3)
- **Target:** Intern AI Engineer / SE
- **Repo:** https://github.com/NguyenNgocTu041105/finance-ai-agent

---

## 17/10/2026: Hoàn thành Buổi 10 - RAG cơ bản với LangChain

- **Mục tiêu:** Xây dựng pipeline RAG (Retrieval-Augmented Generation) cơ bản để LLM có thể đọc hiểu tài liệu nội bộ thay vì chỉ trả lời dựa trên kiến thức sẵn có.
- **Đã làm:**
  - Cài đặt thành công bộ thư viện lõi: `langchain`, `langchain-community`, `langchain-chroma`, `chromadb`, `pypdf`.
  - Viết `rag_basic.py`: Cấu trúc pipeline 5 bước chuẩn (Load -> Chunk -> Embed -> Store -> Retrieve & Generate).
  - Áp dụng **LCEL (LangChain Expression Language)** để nối prompt, LLM và output parser bằng dấu `|`.
  - Xử lý triệt để lỗi trùng lặp dữ liệu: Tự động xóa thư mục `./storage/chroma_db` trước mỗi lần chạy bằng `shutil.rmtree` (bọc try-except để tránh lỗi lock file trên Windows).
- **Thử nghiệm thực tế:**
  - Tạo file text giả lập BCTC FPT Quý 2/2026.
  - Chạy RAG hỏi "Nợ phải trả của FPT quý 2/2026 là bao nhiêu?" -> Pipeline tìm đúng chunk và trả lời chính xác "25,000 tỷ VND".
- **Lỗi gặp phải & Cách khắc phục:**
  - Lỗi `ModuleNotFoundError: langchain_chroma` -> Cài bổ sung gói `langchain-chroma` (do LangChain tách nhỏ các gói tích hợp).
  - Lỗi `404 NOT_FOUND` với `text-embedding-004` -> Google đã khai tử model này, chuyển sang `gemini-embedding-001`.
  - Lỗi `404 NOT_FOUND` với `gemini-2.5-flash` -> Chuyển sang model mới `gemini-3.8-flash`.
- **Bài học rút ra:**
  - RAG gồm 5 bước, trong đó bước **Retrieval (Tìm kiếm)** là trái tim của hệ thống.
  - `chunk_overlap` không có con số hoàn hảo tuyệt đối. Nó thường được đặt bằng 10-20% của `chunk_size` để bắc cầu ngữ cảnh.
  - Vector Embeddings là cách máy tính hiểu ngữ nghĩa (chuyển chữ thành dãy số).
- **Kết quả:** Chạy thành công RAG pipeline đầu tiên, tạo tiền đề cho việc xử lý dữ liệu phi cấu trúc.
- **Bước tiếp theo:** Bắt đầu **Buổi 11**: Đọc file PDF BCTC thật thay vì file text mẫu.

### 15/10/2026: Hoàn thành Milestone 1 - Financial Tools & Agent với Function Calling

- **Mục tiêu:** Tích hợp dữ liệu chứng khoán thật (`vnstock`) vào LLM và hoàn thiện Agent tự động gọi Tool.
- **Đã làm:**
  - Hoàn thiện `tools.py`: 3 tools lấy dữ liệu thật (`get_stock_price`, `get_company_info`, `get_financial_ratios`) kèm `TOOLS_SCHEMA` cho Function Calling.
  - Xử lý bài toán thiếu dữ liệu BCTC: Thiết kế cơ chế **Smart Fallback** cho chỉ số tài chính (tự tìm quý gần nhất có dữ liệu kèm cờ `is_latest` để LLM tự quyết định ngữ cảnh so sánh).
  - Hoàn thiện `agent_with_tools.py`: Xây dựng vòng lặp Two-turn Function Calling hoàn chỉnh.
  - Xử lý lỗi gõ sai mã (Typo): Dùng Prompt Engineering để Agent tự động map tên doanh nghiệp / mã sai phổ biến ("thế giới di động" -> `MWG`, "FBT" -> `FPT`).
- **Thử nghiệm thực tế:**
  - Test hỏi giá MWG: Gemini dính lỗi 503 và Timeout -> Hệ thống tự động kích hoạt Fallback 2 lần sang Groq GPT-OSS 120B thành công, trả về đúng giá 72.8k.
  - Test hỏi ngoài phạm vi (trái phiếu): Agent nhận biết phạm vi, không gọi bừa tool và từ chối lịch sự.
- **Quyết định kiến trúc:**
  - MVP (Hiện tại): Dùng Prompt Engineering xử lý mã cổ phiếu và hướng dẫn đọc quý BCTC.
  - Giai đoạn sau (Multi-Agent): Nâng cấp Tool trả về cả `latest_quarter_data` và `complete_quarter_data` khi cần phân tích chéo đa agent; mở rộng thêm các danh mục đầu tư khác (Trái phiếu, Vĩ mô).
- **Kết quả:** Đạt mục tiêu **Milestone 1 (Giai đoạn 1)** của Master Roadmap.
- **Bước tiếp theo:** Bắt đầu **Milestone 2 (Giai đoạn 2)**: RAG nâng cao cho Báo cáo tài chính (PDF parsing, trích xuất dữ liệu BCTC chi tiết).


## 14/10/2026 Hoàn thiện LLM Client
### Làm được
- Xong `llm_client.py`: multi-model fallback Gemini → Groq → OpenRouter, Retry + Exponential Backoff, hỗ trợ Function Calling. Test chạy ổn.

### 13/10/2026: Buổi 8 - Test Fallback thực tế
- **Mục tiêu:** Ép lỗi có chủ đích để kiểm tra hệ thống chuyển model tự động.
- **Thử nghiệm:** Cố tình sửa sai API key và tên model của Gemini và Groq trong `.env`.
- **Kết quả:**
  - Gemini dính lỗi hỏng model -> Bỏ qua.
  - Groq dính `BadRequestError` (sai key) -> Bỏ qua ngay lập tức, không retry vô ích.
  - OpenRouter ở chốt chặn cuối cùng gánh thành công, trả lời chính xác câu hỏi ("Messi là ai").
- **Đánh giá:** Logic fallback và retry đã chạy chuẩn xác 100%.
- **Bước tiếp theo:** Bắt tay vào làm **Project M1** (Ghép Function Calling lấy dữ liệu chứng khoán thật vào hệ thống fallback).

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
- **Bước tiếp theo:** Function Calling với vnstock.

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
- **Bước tiếp theo:** Nghiên cứu Multi-Model Fallback.