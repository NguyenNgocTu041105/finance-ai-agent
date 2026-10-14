# LEARNING LOG — Finance AI Agent
# Nguyễn Ngọc Tú | MIS Year 3 | Target: AI Engineer / SE 3.0 Internship

---

## [2026-10-14] Hoàn thiện LLM Client

### Làm được
- Xong `llm_client.py`: multi-model fallback Gemini → Groq → OpenRouter, Retry + Exponential Backoff, hỗ trợ Function Calling. Test chạy ổn.

### Để ngày mai
- Fix nốt `tools.py` (3 bug còn lại) + implement smart fallback cho financial ratios
- Tạo `agent_with_tools.py` — Two-turn Function Calling loop
