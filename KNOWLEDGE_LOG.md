# 🧠 KNOWLEDGE LOG - Finance AI Agent

## Buổi 9: Function Calling với vnstock

### Câu 1: Kiến trúc 3 file

**Trả lời:**
- `llm_client.py` — Gọi LLM + Multi-Model Fallback
- `tools.py` — Lấy dữ liệu chứng khoán (price, company, ratios)
- `agent_with_tools.py` — Orchestration (ghép 2 file trên)

**Nguyên tắc:** Separation of Concerns (SOLID - chữ S).
- Mỗi file chỉ làm 1 việc.
- Thêm tool → sửa `tools.py`.
- Thêm model → sửa `llm_client.py`.

### Câu 2: Function Calling

**Định nghĩa:** Kỹ thuật cho phép LLM quyết định gọi hàm Python (do bạn định nghĩa) khi cần dữ liệu thật.

**Luồng:**
1. Định nghĩa `TOOLS_SCHEMA`.
2. LLM đọc schema → quyết định gọi hàm.
3. LLM trả về `tool_call`.
4. Bạn chạy hàm → trả kết quả.
5. LLM viết câu trả lời.

**Tại sao cần:** Nếu không có → LLM bịa số liệu (hallucination).

### Câu 3: Luồng Agent

**Lần gọi 1:** LLM phân tích câu hỏi → quyết định gọi tool nào → trả về `tool_calls`.

**Giữa 2 lần:** Code chạy tool → lấy dữ liệu thật.

**Lần gọi 2:** LLM nhận kết quả tool → **viết câu trả lời** (không gọi tool).

### Câu 4: Multi-Model Fallback

**Chain:** Gemini → Groq → OpenRouter.

**Retry khi:** Lỗi tạm thời (503, 502, 504, timeout, overloaded).

**Chuyển model khi:** Lỗi vĩnh viễn (401, 404, 429).

**Tại sao phân biệt:** Retry lỗi 401 vô ích (sai key thì retry vẫn sai).

**Thuật ngữ:** Exponential Backoff (chờ 2s → 4s → 8s).

### Câu 5: Smart Fallback

**`is_latest = true`:** Chỉ số lấy từ quý mới nhất.
**`is_latest = false`:** Chỉ số lấy từ quý cũ (quý mới chưa cập nhật).

**LLM dùng:**
- Nếu `true` → "P/E quý mới nhất là X".
- Nếu `false` → "P/E theo Q4/2025 là X, Q2/2026 chưa có".

### Câu 6: Defensive Programming (2 lớp)

**Lớp 1:** Kiểm tra tool tồn tại — `AVAILABLE_TOOLS.get(function_name)`.
→ Nếu không tồn tại → trả error (LLM ảo giác tên tool).

**Lớp 2:** Try-except quanh tool call.
→ Nếu tool chạy lỗi → trả error.

**Nếu bỏ cả 2:** LLM ảo giác → crash. Tool lỗi → crash.

### Câu 7: Over-constraint

**Định nghĩa:** Prompt quá chặt → LLM không dám trả lời ngoài phạm vi.

**Nguyên nhân:** LLM có Safety Alignment (thà từ chối còn hơn sai).

**Cách khắc phục:** Thêm quy tắc "TRẢ LỜI TRỰC TIẾP" cho kiến thức chung.

**Ví dụ:**
- Trước: "Trái phiếu là gì?" → "Xin lỗi, tôi chỉ hỗ trợ cổ phiếu."
- Sau: "Trái phiếu là gì?" → "Trái phiếu là một loại chứng khoán nợ..."