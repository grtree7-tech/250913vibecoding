import streamlit as st
import pandas as pd
import altair as alt
import os

st.title("🌍 MBTI 유형별 TOP 10 국가")

# 파일 경로 설정
file_path = "countriesMBTI_16types.csv"

# 데이터 불러오기 (기본: 로컬, 예외: 업로드)
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
else:
    uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        st.stop()  # 데이터가 없으면 실행 중단

# MBTI 유형 선택
mbti_types = df.columns[1:].tolist()
selected_type = st.selectbox("MBTI 유형을 선택하세요:", mbti_types)

# 선택된 유형의 TOP 10 추출
top10 = df[["Country", selected_type]].sort_values(by=selected_type, ascending=False).head(10)

# Altair 그래프 생성
chart = (
    alt.Chart(top10)
    .mark_bar()
    .encode(
        x=alt.X(selected_type, title=f"{selected_type} 비율", axis=alt.Axis(format="%")),
        y=alt.Y("Country", sort="-x"),
        tooltip=["Country", alt.Tooltip(selected_type, format=".2%")]
    )
    .properties(width=600, height=400, title=f"{selected_type} TOP 10 국가")
)

st.altair_chart(chart, use_container_width=True)

# 데이터 테이블 표시
st.dataframe(top10.reset_index(drop=True))
