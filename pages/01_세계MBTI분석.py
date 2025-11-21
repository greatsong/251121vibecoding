import streamlit as st
import pandas as pd
import altair as alt

# 페이지 설정
st.set_page_config(
    page_title="MBTI 국가별 비율 탐색기",
    page_icon="🌍",
    layout="centered"
)

@st.cache_data
def load_data():
    # Streamlit Cloud에서는 같은 폴더에 CSV 파일을 두세요.
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

st.title("🌍 국가별 MBTI 비율 탐색기")
st.write("MBTI 유형을 선택하면, 해당 유형 비율이 **가장 높은 10개 나라**와 **가장 낮은 10개 나라**를 Altair 막대그래프로 보여주는 웹앱입니다.")

# MBTI 유형 선택
mbti_types = [col for col in df.columns if col != "Country"]
selected_mbti = st.selectbox("MBTI 유형을 선택하세요", mbti_types, index=0)

# 선택한 MBTI 기준으로 정렬
sorted_df = df.sort_values(by=selected_mbti, ascending=False)

top10 = sorted_df.head(10).copy()
bottom10 = sorted_df.tail(10).copy()

# 상위/하위 데이터에 공통 컬럼명으로 맞추기 (Altair용)
top10 = top10[["Country", selected_mbti]].rename(columns={selected_mbti: "value"})
bottom10 = bottom10[["Country", selected_mbti]].rename(columns={selected_mbti: "value"})

# -------- 상위 10개 나라 차트 --------
st.subheader(f"🔼 {selected_mbti} 비율이 가장 높은 10개 나라")

top_chart = (
    alt.Chart(top10)
    .mark_bar()
    .encode(
        x=alt.X("value:Q", title=f"{selected_mbti} 비율"),
        y=alt.Y("Country:N", sort="-x", title="나라"),
        tooltip=[
            alt.Tooltip("Country:N", title="나라"),
            alt.Tooltip("value:Q", title=f"{selected_mbti} 비율", format=".3f"),
        ]
    )
    .properties(
        width=600,
        height=400
    )
    .interactive()
)

st.altair_chart(top_chart, use_container_width=True)

# -------- 하위 10개 나라 차트 --------
st.subheader(f"🔽 {selected_mbti} 비율이 가장 낮은 10개 나라")

# 하위 10개는 값이 작은 순으로 정렬 (보기 좋게)
bottom10_sorted = bottom10.sort_values(by="value", ascending=True)

bottom_chart = (
    alt.Chart(bottom10_sorted)
    .mark_bar()
    .encode(
        x=alt.X("value:Q", title=f"{selected_mbti} 비율"),
        y=alt.Y("Country:N", sort="x", title="나라"),
        tooltip=[
            alt.Tooltip("Country:N", title="나라"),
            alt.Tooltip("value:Q", title=f"{selected_mbti} 비율", format=".3f"),
        ]
    )
    .properties(
        width=600,
        height=400
    )
    .interactive()
)

st.altair_chart(bottom_chart, use_container_width=True)
