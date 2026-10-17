import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

# 1. Load API keys
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 2. Tạo dữ liệu mẫu
sample_text = """
Báo cáo tài chính FPT Quý 2 năm 2026:
- Doanh thu thuần: 15,000 tỷ VND (tăng 20% so với cùng kỳ).
- Lợi nhuận sau thuế: 2,500 tỷ VND.
- Tổng tài sản: 60,000 tỷ VND.
- Nợ phải trả: 25,000 tỷ VND.
- Vốn chủ sở hữu: 35,000 tỷ VND.
FPT đang có kế hoạch mở rộng mảng AI và bán dẫn trong quý 3.
"""

file_path = "sample_finance.txt"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(sample_text)

print("1. Đang đọc tài liệu...")
loader = TextLoader(file_path, encoding="utf-8")
docs = loader.load()

print("2. Đang cắt nhỏ tài liệu (Chunking)...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
chunks = text_splitter.split_documents(docs)
print(f"   -> Đã cắt thành {len(chunks)} chunks.")

print("3. Đang tạo Vector Database (ChromaDB)...")
# Dùng model embedding thế hệ mới
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# Xóa DB cũ nếu tồn tại (bọc try-except cho Windows)
db_path = "./storage/chroma_db"
if os.path.exists(db_path):
    try:
        shutil.rmtree(db_path)
        print("   -> Đã làm mới DB.")
    except Exception as e:
        print(f"   -> Cảnh báo: Không thể xóa DB cũ ({e}). Sẽ ghi đè lên DB hiện có.")

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=db_path
)

print("4. Đang khởi tạo LLM và Retriever...")
llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash", temperature=0)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

prompt_template = """
Bạn là chuyên gia tài chính. Dựa VÀO ĐOẠN VĂN BẢN SAU ĐÂY để trả lời câu hỏi.
Không được bịa ra thông tin ngoài văn bản.

Văn bản:
{context}

Câu hỏi: {question}

Trả lời:
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

# Dùng LCEL (LangChain Expression Language)
chain = prompt | llm | StrOutputParser()


def ask_rag(question: str):
    """Hàm hỏi RAG với LCEL."""
    retrieved_docs = retriever.invoke(question)
    context_text = "\n\n".join([doc.page_content for doc in retrieved_docs])
    response = chain.invoke({"context": context_text, "question": question})
    return response


if __name__ == "__main__":
    print("\n--- RAG Agent đã sẵn sàng ---")
    
    question1 = "Doanh thu?"
    print(f"\nHỏi: {question1}")
    print(f"Đáp: {ask_rag(question1)}")
    
    question2 = "Tổng tài sản?"
    print(f"\nHỏi: {question2}")
    print(f"Đáp: {ask_rag(question2)}")