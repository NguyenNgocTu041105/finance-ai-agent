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
        "name": os.getenv("OPENROUTER_MODEL", "openrouter/google/gemma-4-31b-it:free"),
        "env_key": "OPENROUTER_API_KEY",
        "label": "OpenRouter Free",
    },
]

# Cấu hình Retry & Backoff
MAX_RETRIES = 2
RETRY_DELAY = 2  # giây cơ sở

# Chỉ retry các lỗi tạm thời (nghẽn server, timeout, quá tải)
RETRYABLE_ERRORS = ["503", "502", "504", "Timeout", "timeout", "Service Unavailable", "overloaded"]

def chat_with_fallback(user_message:str)->tuple[str,str]:
    """
    Gửi message tới các LLM với fallback tự động,
    trả về tuple (response_text,model_used)
    """
    last_error=None

    for model_config in MODEL_FALLBACKS:
        model_name=model_config["name"]
        api_key=os.getenv(model_config["env_key"])
        label=model_config["label"]

        if not api_key:
            print(f"Bỏ qua {label}:chưa có API key trong .env")
            continue
        for attempt in range(1,MAX_RETRIES+1):
            try:
                if attempt==1:    
                    print(f"Đang thử : {label} ...")
                else:
                    delay = RETRY_DELAY * (2 ** (attempt - 2))
                    print(f"Thử lại {label} lần {attempt}/{MAX_RETRIES} sau {delay}s ...")
                    time.sleep(delay)

                response=completion(
                    model=model_name,
                    messages=[{"role":"user","content":user_message}],
                    api_key=api_key,
                    timeout=30,
                )
                print(f"Thành công với : {label}")
                return response.choices[0].message.content,label
        
            except Exception as e:
                last_error = e
                error_str = str(e)
                # Kiểm tra xem lỗi này có đáng để retry không
                is_retryable = any(code in error_str for code in RETRYABLE_ERRORS)

                if is_retryable and attempt < MAX_RETRIES:
                    print(f"{label} tạm thời bận. Sẽ thử lại...")
                    continue
                else:
                    print(f"{label} thất bại: {error_str[:80]}...")
                    break  
    
    # nếu tất cả model lỗi
    raise Exception(f"Tất cả model đều lỗi . Lỗi cuối :{last_error}")

if __name__ == "__main__":
    print("=== Multi-Model Chat Bot ===")
    print("Tự động fallback khi model lỗi.")
    print("Gõ 'quit' để thoát.\n")

    while True:
        user_input=input("Bạn:").strip()
        if user_input.lower() in ["quit","exit","q"]:
            print("Tạm biệt. Hẹn gặp lại !")
            break
        if not user_input:
            continue
        
        try:
            reply,model_used=chat_with_fallback(user_input)
            print(f"\n[{model_used}]: {reply}\n")
        except Exception as e:
            print(f"\n Lỗi: {e}\n")