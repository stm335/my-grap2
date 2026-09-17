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
        df['genre'] = df['genre'].fillna('').astype(str).str.split('|').str[0]
        df['genre'] = df['genre'].replace('', '기타')
        
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
fig1 = px.pie(
    genre_counts, 
    names='genre', 
    values='count', 
    hole=0.4,
    title='장르별 영화 비율 및 편수'
)

# 마우스 호버 시 편수(value)와 비율(percent) 표시 설정
fig1.update_traces(
    textinfo='percent+label',
    hovertemplate='<b>장르:</b> %{label}<br><b>편수:</b> %{value}편<br><b>비율:</b> %{percent}'
)

st.plotly_chart(fig1, use_container_width=True)

# 구분 구역 및 첫 번째 그래프 설명 영역
st.divider()
st.info("💡 **이 그래프로 알 수 있는 것:** 주요 개봉작 중 특정 장르(예: 드라마, 애니메이션 등)가 차지하는 비중과 다양성을 한눈에 비교할 수 있습니다.")

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 두 번째 그래프: 장르별 영화 관객수 트리맵
# ---------------------------------------------------------
st.subheader("2. 장르 및 영화별 총 관객수 분포 (트리맵)")

# Plotly 트리맵 생성 (계층 구조: genre -> movieNm, 칸 크기: total_audi)
fig2 = px.treemap(
    df,
    path=['genre', 'movieNm'],
    values='total_audi',
    title='장르 및 영화별 총 관객수 비율'
)

# 마우스 호버 시 영화명과 총 관객수 표시 설정
fig2.update_traces(
    hovertemplate='<b>영역/영화명:</b> %{label}<br><b>총 관객수:</b> %{value:,}명'
)

st.plotly_chart(fig2, use_container_width=True)

# 구분 구역 및 두 번째 그래프 설명 영역
st.divider()
st.info("💡 **이 그래프로 알 수 있는 것:** 전체 박스오피스 관객수를 이끈 주요 장르와 그 안에서 실질적인 흥행을 견인한 특정 영화의 기여도를 직관적으로 파악할 수 있습니다.")
