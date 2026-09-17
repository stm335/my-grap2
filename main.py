import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")

# 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # genre 열이 존재하는 경우, 첫 번째 장르만 추출 (세로막대 기호 '|' 기준)
    if 'genre' in df.columns:
        df['genre'] = df['genre'].astype(str).apply(lambda x: x.split('|')[0] if x != 'nan' else x)
        
    return df

df = load_data()

# ---------------------------------------------------------
# 첫 번째 그래프: 장르별 영화 편수 (플롯리 도넛 그래프)
# ---------------------------------------------------------
st.subheader("1. 장르별 영화 편수 분포")

# 장르별 영화 편수 집계
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

# Plotly 도넛 차트 생성
fig = px.pie(
    genre_counts, 
    names='genre', 
    values='count', 
    hole=0.4,
    title='장르별 영화 비율 및 편수'
)

# 마우스 호버 시 편수(value)와 비율(percent) 표시 설정
fig.update_traces(
    textinfo='percent+label',
    hovertemplate='<b>장르:</b> %{label}<br><b>편수:</b> %{value}편<br><b>비율:</b> %{percent}'
)

st.plotly_chart(fig, use_container_width=True)

# 구분 구역 및 그래프 설명 영역
st.divider()
st.info("💡 **이 그래프로 알 수 있는 것:** 주요 개봉작 중 특정 장르(예: 드라마, 애니메이션 등)가 차지하는 비중과 다양성을 한눈에 비교할 수 있습니다.")
