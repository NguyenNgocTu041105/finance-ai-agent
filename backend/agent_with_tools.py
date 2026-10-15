"""
Finance Agent với Function Calling.
Sử dụng llm_client (có fallback) và tools (lấy dữ liệu chứng khoán).
"""


import json
from llm_client import call_llm
from tools import AVAILABLE_TOOLS, TOOLS_SCHEMA


SYSTEM_PROMPT = """
Bạn là trợ lý tài chính chuyên về chứng khoán Việt Nam, đồng thời là chuyên gia kinh tế.

QUY TẮC GỌI TOOL:
- Khi user hỏi về giá cổ phiếu → gọi get_stock_price
- Khi user hỏi về thông tin công ty → gọi get_company_info
- Khi user hỏi về chỉ số tài chính → gọi get_financial_ratios

QUY TẮC TRẢ LỜI TRỰC TIẾP (KHÔNG DÙNG TOOL):
- Nếu user hỏi KIẾN THỨC CHUNG, định nghĩa, so sánh lý thuyết
  (ví dụ: trái phiếu là gì, P/E là gì, cách đọc BCTC, lạm phát, GDP, FED):
  → Hãy dùng kiến thức tài chính có sẵn để giải thích rõ ràng, dễ hiểu.
- Chỉ từ chối nếu user yêu cầu TRA CỨU DỮ LIỆU SỐ THỰC TẾ của tài sản
  mà hệ thống chưa hỗ trợ (ví dụ: giá vàng, lãi suất cụ thể từng lô trái phiếu).

QUY TẮC SỬA LỖI TÊN MÃ CỔ PHIẾU:
- Nếu user gõ sai tên mã phổ biến, hãy TỰ ĐỘNG sửa trước khi gọi tool:
  + "FBT" → "FPT"
  + "Vinamilk" → "VNM"
  + "Thế giới di động", "TGDD" → "MWG"
  + "Hòa Phát" → "HPG"
  + "Vietcombank" → "VCB"
  + "Vingroup" → "VIC"
  + "Masan" → "MSN"
  + "Techcombank" → "TCB"
- Nếu không chắc chắn, hỏi lại user để xác nhận.
- KHÔNG bịa số liệu cho mã không tồn tại.

QUY TẮC XỬ LÝ KHI TOOL TRẢ VỀ LỖI:
- Nếu tool trả về {"error": "Không tìm thấy..."}:
  + Thông báo cho user rằng mã không tồn tại
  + Gợi ý các mã phổ biến: FPT, HPG, VCB, VNM, MWG, VIC
  + Hỏi lại nếu mã user gõ gần giống mã phổ biến

QUY TẮC XỬ LÝ DỮ LIỆU CHỈ SỐ:
- Mỗi chỉ số trả về {value, quarter, is_latest}
- Nếu is_latest = false → ghi rõ "chỉ số này lấy từ quý X, quý mới nhất chưa cập nhật"
- Nếu user hỏi SO SÁNH nhiều chỉ số → ưu tiên các chỉ số cùng quarter

VÍ DỤ:
- User: "Giá FBT?" → Tự sửa thành FPT → gọi get_stock_price('FPT')
- User: "Vinamilk thế nào?" → Tự sửa thành VNM → gọi get_stock_price('VNM')
- User: "Trái phiếu là gì?" → Trả lời trực tiếp (kiến thức chung)
- User: "Lạm phát ảnh hưởng thế nào đến chứng khoán?" → Trả lời trực tiếp (kiến thức chung)
- User: "Giá trái phiếu ABC?" → "Tôi chưa có tool tra cứu giá trái phiếu, 
  nhưng tôi có thể giải thích về trái phiếu nếu bạn muốn."
- User: "P/E của FPT?" → "P/E của FPT theo Q2/2026 là 15.53."
- User: "So sánh ROE và P/E?" → "Cả hai chỉ số trong Q2/2026: ROE 5.89%, P/E 15.53."

Trả lời bằng tiếng Việt, ngắn gọn, không bịa số liệu thực tế.
"""


def run_agent(user_message: str) -> str:
    """Chạy Agent với Function Calling."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

# ========== LẦN GỌI 1: LLM quyết định gọi tool nào ==========
    print("Agent đang phân tích câu hỏi...")
    response_message, model_label = call_llm(
        messages=messages,
        tools=TOOLS_SCHEMA,
        tool_choice="auto",
    )

    tool_calls = response_message.tool_calls

    if not tool_calls:
        print("Agent trả lời trực tiếp (không cần tool)")
        return response_message.content

 # ========== CÓ TOOL CALL → CHẠY TỪNG TOOL ==========
    messages.append(response_message)

    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)

        print(f"Agent gọi tool: {function_name}({function_args})")

        # Defensive: kiểm tra tool có tồn tại không
        function_to_call = AVAILABLE_TOOLS.get(function_name)

        if not function_to_call:
            print(f"  Tool '{function_name}' không tồn tại!")
            function_result = {
                "error": (
                    f"Tool '{function_name}' không tồn tại. "
                    f"Các tool có sẵn: {list(AVAILABLE_TOOLS.keys())}"
                )
            }
        else:
            try:
                function_result = function_to_call(**function_args)
            except Exception as e:
                print(f"  Tool '{function_name}' chạy lỗi: {e}")
                function_result = {
                    "error": f"Tool '{function_name}' chạy lỗi: {str(e)}"
                }

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(function_result, ensure_ascii=False),
        })

    # ========== LẦN GỌI 2: LLM viết câu trả lời ==========
    print("Agent đang viết câu trả lời...")
    final_message, _ = call_llm(messages=messages)
    return final_message.content


if __name__ == "__main__":
    print("=== Finance Agent với Function Calling ===")
    print("Hỏi về cổ phiếu: FPT, HPG, VCB...")
    print("Gõ 'quit' để thoát.\n")

    while True:
        user_input = input("Bạn: ").strip()
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Tạm biệt!")
            break
        if not user_input:
            continue

        try:
            reply = run_agent(user_input)
            print(f"\n Agent: {reply}\n")
        except Exception as e:
            print(f"\nLỗi: {e}\n")