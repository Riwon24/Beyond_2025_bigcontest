# gemini_client.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

# .env에서 GOOGLE_API_KEY 로드
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("환경 변수 GOOGLE_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

# LLM 객체 초기화: Gemini 2.5 Flash 모델 사용
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",       # 모델 명시
    google_api_key=GOOGLE_API_KEY, # 키 불러오기
    temperature=0.1                # 낮은 온도 → 정제된 문장
)

# 문장 생성 함수
def generate_gemini_caption(prompt: str) -> str:
    try:
        # HumanMessage로 전달
        response = llm([HumanMessage(content=prompt)])
        return response.content.strip()
    except Exception as e:
        return f"[Gemini 오류] 마케팅 문구 생성 실패: {str(e)}"
