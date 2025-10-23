import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
import os
from dotenv import load_dotenv
import pandas as pd

# 컬럼 설명 및 시각화 함수
from column_descriptions import COLUMN_DESCRIPTIONS
from visualization import display_store_insights

# MCP 서버 기능 호출
from mcp_server import load_store_data, analyze_case, find_store_name, has_visualization

# .env에서 GOOGLE_API_KEY 로드
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Gemini 모델 초기화
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.5,
)

def clear_chat_history():
    st.session_state.chat_history = []
    st.rerun()

# 첫화면 멘트
INITIAL_INTRO = """
🗣️ **가게명**이나 지금 겪고 계신 **문제 상황**을 말씀해 주세요. 구체적인 전략을 드리기 위해 사건 제보가 필요합니다.  

예시:  
- "OO 매장인데, 단골이 줄었어요."
- "△△ 카페인데, 젊은 손님들이 잘 안 와요."
- "□□ 식당인데, 홍보가 잘 안 되는 것 같아요."
"""

# 페이지 설정
st.set_page_config(page_title="🕵️ 탐정 D의 마케팅 수사노트", layout="wide")

# 세션 상태 초기화
if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.chat_history.append({"role": "assistant", "content": INITIAL_INTRO})

if "case_counter" not in st.session_state:
    st.session_state.case_counter = 1

# 사이드바 구성
if st.session_state.sidebar_open:
    with st.sidebar:
        st.image("assets/shc_ci_basic_00.png", use_container_width=True)

        st.markdown("<p style='text-align: center; font-size: 18px; font-weight: bold;'>🕵️ 탐정 D 마케팅 수사본부</p>", unsafe_allow_html=True)
        st.markdown("""
        <p style='text-align: center; font-size: 16px;'>
          데이터와 추리가 만나는 곳<br><strong>Data × Detective</strong>
        </p>
        """, unsafe_allow_html=True)

        st.write("")

        button_html = """
        <style>
        div.stButton > button {
            width: 180px;
            margin: auto;
            display: block;
        }
        </style>
        """
        st.markdown(button_html, unsafe_allow_html=True)

        if st.button("🧹 Clear Case Log"):
            st.session_state.chat_history = [{
                "role": "assistant",
                "content": INITIAL_INTRO
            }]
            st.rerun()

st.title("🕵️ 탐정 D : 데이터 기반 마케팅 수사 AI")
st.markdown("""
이곳은 단골 실종 사건과 매출 하락 미스터리가 끊이지 않는 현장.  
저는 데이터를 단서 삼아 문제를 추적하는 마케팅 전문 탐정, **데이텍티브 Datetective**입니다. 사람들은 저를 **탐정 D**라고 부르죠.

📂 단골 손님의 실종, 📉 매출의 급락, 🧩 의문의 광고 성과 하락…  
무엇이든 **사건**이 있다면, 단서를 분석해 **전략이라는 이름의 해결책**을 찾아드립니다.

🕵️ **탐정 D, 수사 개시 준비 완료.**
""")

# 채팅 메시지 출력
case_index = 1
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):

        # 사건 번호 표시
        if msg["role"] == "assistant" and msg.get("store_row"):
            st.markdown(f"📎 **사건 파일 #{case_index:03}**")
            case_index += 1

        # 시각화 포함 메시지 처리
        if "[[VISUALIZATION_PLACEHOLDER]]" in msg["content"]:
            before_vis, after_vis = msg["content"].split("[[VISUALIZATION_PLACEHOLDER]]", 1)
            st.markdown(before_vis)

            if msg.get("store_row"):
                df_row = pd.Series(msg["store_row"])
                display_store_insights(df_row)

            st.markdown(after_vis)
        else:
            st.markdown(msg["content"])

# 입력 처리
user_input = st.chat_input("💬 사건을 제보해 주세요 (예: 다다** 단골이 줄었어요)")
if user_input:
    matched_store_name = find_store_name(user_input)
    store_row, _ = load_store_data(matched_store_name) if matched_store_name else (None, None)

    if matched_store_name:
        st.session_state.case_counter += 1

    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.spinner("🔍 단서를 분석 중입니다..."):
        try:
            response = analyze_case(
                messages=st.session_state.chat_history,
                store_row=store_row.to_dict() if store_row is not None else {},
                column_descriptions=COLUMN_DESCRIPTIONS
            )
        except Exception as e:
            response = f"❌ 오류가 발생했습니다: {str(e)}"

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response,
        "store_row": store_row.to_dict() if store_row is not None else None
    })

    st.rerun()
