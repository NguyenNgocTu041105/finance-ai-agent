import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def chat_with_gemini(user_message: str) -> str:
    response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=user_message,
    )
    return response.text

if __name__ == "__main__":
    print("=== Gemini Chat Bot của Tunn.exe ===")
    print("Go 'quit' de thoat.\n")
    
    while True:
        user_input = input("Ban: ").strip()
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Tam biet!")
            break
        if not user_input:
            continue
        
        try:
            reply = chat_with_gemini(user_input)
            print(f"Gemini: {reply}\n")
        except Exception as e:
            print(f"Loi: {e}\n")