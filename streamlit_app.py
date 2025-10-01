import streamlit as st
from mcp_server import analyze_store
from data_loader import load_store_data
import plotly.graph_objects as go

st.set_page_config(page_title="AI 마케팅 전략 코치", layout="wide")
st.title("🤖 내 가게를 살리는 AI 비밀상담사")

st.markdown("""
매장 데이터를 기반으로 경쟁 매장과의 상대적인 위치를 분석하고,  
배달/재방문/신규 유입 전략을 자동 추천해드립니다.
""")

# 입력창
store_name = st.text_input("📌 매장명 입력", placeholder="예: 커피빈 역삼점")

if store_name:
    with st.spinner("분석 중입니다..."):
        try:
            result = analyze_store(store_name)
            st.success(f"✅ '{store_name}' 마케팅 전략 분석 결과")

            # 1️⃣ 📊 퍼센타일 Plotly 그래프
            st.subheader("📊 경쟁 매장 대비 퍼센타일")
            percentile = result["percentiles"]
            labels = list(percentile.keys())
            values = [percentile[k] if percentile[k] is not None else 0 for k in labels]

            fig = go.Figure(go.Bar(
                x=labels,
                y=values,
                marker_color=['#636EFA', '#EF553B', '#00CC96'],
                text=[f"{v:.1f}%" for v in values],
                textposition='auto'
            ))
            fig.update_layout(
                yaxis=dict(title='백분위 (%)', range=[0, 100]),
                xaxis=dict(title='지표'),
                height=400,
                margin=dict(l=40, r=40, t=30, b=40)
            )
            st.plotly_chart(fig, use_container_width=True)

            # 2️⃣ 🧠 전략 카드 형식 출력
            st.subheader("🧠 맞춤형 마케팅 전략 카드")

            if result["strategies"]:
                cols = st.columns(2)
                for i, strat in enumerate(result["strategies"]):
                    with cols[i % 2]:
                        st.markdown(
                            f"""
                            <div style="background-color:#f0f2f6; padding: 1rem; border-radius: 1rem; margin-bottom: 1rem; box-shadow: 2px 2px 6px rgba(0,0,0,0.05);">
                                <h4 style="color:#1c64f2;">💡 전략 {i+1}</h4>
                                <p style="margin-top: 0.5rem;">{strat}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
            else:
                st.info("전략 조건에 해당하는 항목이 없습니다.")

            # 3️⃣ 💬 Gemini 생성 마케팅 문구
            st.subheader("💬 Gemini 생성 마케팅 문구")
            st.write(result["caption"])

        except Exception as e:
            st.error(f"❌ 분석 중 오류가 발생했습니다: {str(e)}")

else:
    # 매장명 예시 표시
    _, df = load_store_data("")
    st.markdown("🔍 예시 매장명 (상위 5개)")
    st.write(df["mct_nm"].dropna().unique().tolist()[:5])
