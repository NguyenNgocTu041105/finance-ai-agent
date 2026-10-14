import time
from pathlib import Path
import os
from dotenv import load_dotenv
from litellm import completion

# load API keys từ .env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# Danh sách các model theo mức độ ưu tiên
MODEL_FALLBACKS = [
    {
        "name": os.getenv("GEMINI_MODEL", "gemini/gemini-3.8-flash"),
        "env_key": "GEMINI_API_KEY",
        "label": "Gemini 3.8 Flash",
    },
    {
        "name": os.getenv("GROQ_MODEL", "groq/openai/gpt-oss-120b"),
        "env_key": "GROQ_API_KEY",
        "label": "Groq GPT-OSS 120B",
    },
       {
        "name": os.getenv("OPENROUTER_MODEL", "openrouter/nvidia/nemotron-3-super-120b-a12b:free"),
        "env_key": "OPENROUTER_API_KEY",
        "label": "OpenRouter Free",
    },
]


# Cấu hình Retry & Backoff
MAX_RETRIES = 2
RETRY_DELAY = 2  # giây cơ sở

RETRYABLE_ERRORS = ["503", "502", "504", "Timeout", "timeout", "Service Unavailable", "overloaded"]


def call_llm(messages: list, tools: list = None, tool_choice: str = None) -> tuple:
    """
    Gọi LLM với fallback tự động.
    
    Args:
        messages: List các message (role, content)
        tools: (Optional) Danh sách tools cho function calling
        tool_choice: (Optional) "auto", "required", hoặc "none"
    
    Returns:
        Tuple (response_message, model_label)
    """
    last_error = None

    for model_config in MODEL_FALLBACKS:
        model_name = model_config["name"]
        api_key = os.getenv(model_config["env_key"])
        label = model_config["label"]

        if not api_key:
            print(f" Bỏ qua {label}: chưa có API key")
            continue
        
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                if attempt == 1:
                    print(f" Đang thử: {label}...")
                else:
                    delay = RETRY_DELAY * (2 ** (attempt - 2))
                    print(f" Thử lại {label} lần {attempt}/{MAX_RETRIES} sau {delay}s...")
                    time.sleep(delay)

                # Chuẩn bị kwargs
                kwargs = {
                    "model": model_name,
                    "messages": messages,
                    "api_key": api_key,
                    "timeout": 60,
                }

                # Thêm tools nếu có
                if tools:
                    kwargs["tools"] = tools
                    kwargs["tool_choice"] = tool_choice or "auto"

                response = completion(**kwargs)
                print(f" Thành công với: {label}")
                return response.choices[0].message, label

            except Exception as e:
                last_error = e
                error_str = str(e)
                is_retryable = any(code in error_str for code in RETRYABLE_ERRORS)

                if is_retryable and attempt < MAX_RETRIES:
                    print(f"{label} tạm thời bận. Sẽ thử lại...")
                    continue
                else:
                    print(f"{label} thất bại: {error_str[:80]}...")
                    break

    raise Exception(f"Tất cả model đều lỗi. Lỗi cuối: {last_error}")


def simple_chat(user_message: str) -> str:
    """Chat đơn giản không dùng tools."""
    messages = [{"role": "user", "content": user_message}]
    response_message, label = call_llm(messages)
    return response_message.content


if __name__ == "__main__":
    print("=== Test LLM Client ===")
    print("Gõ 'quit' để thoát.\n")

    while True:
        user_input = input("Bạn: ").strip()
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Tạm biệt!")
            break
        if not user_input:
            continue

        try:
            reply = simple_chat(user_input)
            print(f"\n[{reply}]\n")
        except Exception as e:
            print(f"\n Lỗi: {e}\n")