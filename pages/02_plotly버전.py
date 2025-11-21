import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="MBTI Country Explorer", layout="wide")

st.title("🌍 MBTI 국가별 비율 분석 대시보드")
st.write("MBTI 유형을 선택하면 해당 유형 비율이 **가장 높은/낮은 10개 국가**를 인터랙티브 그래프로 표시합니다.")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# MBTI 목록 (첫 컬럼이 Country라서 제외)
mbti_types = df.columns.tolist()[1:]

# MBTI 선택
selected_mbti = st.selectbox("🔎 분석할 MBTI 유형을 선택하세요:", mbti_types)

st.subheader(f"📌 선택한 MBTI: **{selected_mbti}**")

# 데이터 정렬
sorted_df = df.sort_values(by=selected_mbti, ascending=False)

top10 = sorted_df.head(10)
bottom10 = sorted_df.tail(10)

# ------------------------------
# 🔥 상위 10개 국가 그래프
# ------------------------------

st.markdown("---")
st.markdown(f"## 🏆 {selected_mbti} 비율이 가장 높은 10개 국가")

fig_top = px.bar(
    top10,
    x="Country",
    y=selected_mbti,
    color=selected_mbti,
    title=f"Top 10 Countries for {selected_mbti}",
    height=450
)
fig_top.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig_top, use_container_width=True)

# ------------------------------
# ❄️ 하위 10개 국가 그래프
# ------------------------------

st.markdown("---")
st.markdown(f"## 🧊 {selected_mbti} 비율이 가장 낮은 10개 국가")

fig_bottom = px.bar(
    bottom10,
    x="Country",
    y=selected_mbti,
    color=selected_mbti,
    title=f"Bottom 10 Countries for {selected_mbti}",
    height=450
)
fig_bottom.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig_bottom, use_container_width=True)

st.markdown("---")
st.write("📌 데이터를 기반으로 자동 생성된 대시보드입니다.")
