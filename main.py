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
st.info("💡 **이 그래프로 알 수 있는 것:** 특정 장르가 차지하는 비중을 직관적으로 보여준다. 하지만 얼마나 많은 관객이 봤는지는 알기 힘들다.")

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
st.info("💡 **이 그래프로 알 수 있는 것:** 전체 박스오피스 관객수를 이끌어간 주요 장르와 그 안에서 실질적인 흥행을 견인한 특정 영화의 기여도를 직관적으로 파악할 수 있습니다.")

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 세 번째 그래프: 총 관객수 히스토그램
# ---------------------------------------------------------
st.subheader("3. 총 관객수 분포 (히스토그램)")

# Plotly 히스토그램 생성
fig3 = px.histogram(
    df,
    x='total_audi',
    nbins=30,
    title='영화별 총 관객수 분포',
    labels={'total_audi': '총 관객수 (명)', 'count': '영화 수'},
    color_discrete_sequence=['#636EFA']
)

fig3.update_layout(
    yaxis_title='영화 수',
    xaxis_title='총 관객수 (명)',
    bargap=0.1
)

fig3.update_traces(
    hovertemplate='<b>관객수 구간:</b> %{x}명<br><b>영화 수:</b> %{y}편'
)

st.plotly_chart(fig3, use_container_width=True)

# 동적 데이터 계산 (최고 관객수 영화 정보)
top_movie = df.loc[df['total_audi'].idxmax()]
top_movie_name = top_movie['movieNm']
top_movie_audi = top_movie['total_audi']

# 구분 구역 및 세 번째 그래프 설명 영역
st.divider()
st.info(
    f"💡 **이 그래프로 알 수 있는 것:** 대부분의 영화가 100만~200만 명 이하의 저관객 구간에 빽빽하게 쏠려 있는 '오른쪽으로 긴 꼬리를 갖는 분포(Right-skewed Distribution)'를 보입니다. "
    f"반면 가장 관객 수가 많은 영화는 **'{top_movie_name}'** (약 {top_movie_audi:,}명)로 극소수의 초대형 흥행작이 전체 관객수 상위를 독점하고 있음을 알 수 있습니다."
)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 네 번째 그래프: 개봉일 스크린수 vs 총 관객수 (산점도)
# ---------------------------------------------------------
st.subheader("4. 개봉일 스크린수와 총 관객수의 관계 (산점도)")

# Plotly 산점도 생성
fig4 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    title='개봉일 스크린수 vs 총 관객수',
    labels={
        'first_scrn': '개봉일 스크린수 (개)',
        'total_audi': '총 관객수 (명)',
        'genre': '장르'
    }
)

fig4.update_traces(
    marker=dict(size=9, opacity=0.8),
    hovertemplate='<b>%{hovertext}</b><br>장르: %{fullData.name}<br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명'
)

fig4.update_layout(
    xaxis_title='개봉일 스크린수 (개)',
    yaxis_title='총 관객수 (명)'
)

st.plotly_chart(fig4, use_container_width=True)

# 구분 구역 및 네 번째 그래프 설명 영역
st.divider()
st.info("💡 **이 그래프로 알 수 있는 것:** 대체로 개봉일 스크린수가 많을수록 최종 관객수도 증가하는 양(+)의 상관관계를 보이지만, 스크린수가 적어도 입소문으로 대흥행을 거두거나 반대로 많은 스크린수를 확보했음에도 흥행에 실패한 예외적인 사례도 함께 확인할 수 있습니다.")
