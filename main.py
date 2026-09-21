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
    
    # openDt에서 연도 추출 (전처리)
    if 'openDt' in df.columns:
        open_str = df['openDt'].astype(str).str.replace('.0', '', regex=False).str.strip()
        df['year'] = pd.to_numeric(open_str.str[:4], errors='coerce')
        df.loc[(df['year'] < 1950) | (df['year'] > 2030), 'year'] = None
    
    # genre 열 전처리 (첫 번째 장르만 추출 및 결측치 처리)
    if 'genre' in df.columns:
        df['genre'] = df['genre'].fillna('기타').astype(str).str.split('|').str[0]
        df['genre'] = df['genre'].replace('', '기타')
        
    # nation 열 결측치 처리
    if 'nation' in df.columns:
        df['nation'] = df['nation'].fillna('기타').astype(str)
        df['nation'] = df['nation'].replace('', '기타')
        
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
st.info("💡 **이 그래프로 알 수 있는 것:** 영화의 종류가 많은 영화일 수록 관객의 수도 증가하는 추세이지만 영화의 종류가 적은 장르라고 적다고는 말 할수 없다는 것을 알 수 있다.")

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

# 구분 구역 및 세 번째 그래프 설명 영역
st.divider()
st.info("💡 **이 그래프로 알 수 있는 것:** 대부분의 영화가 크게 흥행에 성공하지 못하고 극소수의 영화들만이 대흥행을 한다는 것을 알 수 있습니다.")

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
st.info("💡 **이 그래프로 알 수 있는 것:** 스크린의 수가 증가할 수록 곽객의 수도 증가하는 추세이지만 왕과사는 남자처럼 엄청나게 많은 수의 스크린이 아니여도 대흥행을 할 수 있고 호프처럼 많은 스크린 수에도 불구하고 큰 흥행에 성공하지 못한 경우도 있다.")

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 다섯 번째 그래프: 주요 장르별 총 관객수 박스플롯
# ---------------------------------------------------------
st.subheader("5. 주요 장르별 총 관객수 분포 (상자 그림)")

# 영화 수 10편 이상인 장르만 추출
genre_counts = df['genre'].value_counts()
top_genres = genre_counts[genre_counts >= 10].index
df_filtered = df[df['genre'].isin(top_genres)]

# Plotly 상자 그림 생성
fig5 = px.box(
    df_filtered,
    x='genre',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    points='outliers',
    title='주요 장르(10편 이상)별 총 관객수 분포 및 이상치',
    labels={
        'genre': '장르',
        'total_audi': '총 관객수 (명)'
    }
)

fig5.update_traces(
    hovertemplate='<b>%{hovertext}</b><br>장르: %{x}<br>관객수: %{y:,}명'
)

fig5.update_layout(
    xaxis_title='장르 (10편 이상)',
    yaxis_title='총 관객수 (명)',
    showlegend=False
)

st.plotly_chart(fig5, use_container_width=True)

# 구분 구역 및 다섯 번째 그래프 설명 영역
st.divider()
st.info("💡 **이 그래프로 알 수 있는 것:** 애니메이션의 경우는 각각의 영화마다 본 사람의 수가 차이가 확연히 나지만 드라마의 경우 대부분 비슷한 관객수를 가졌다는 것을 알 수 있습니다")

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 여섯 번째 그래프: 스크린수, 총 관객수, 첫 주 관객수 (버블 차트)
# ---------------------------------------------------------
st.subheader("6. 스크린수, 총 관객수, 첫 주 관객수의 관계 (버블 차트)")

# Plotly 버블 차트 생성 (size = first_week_audi)
fig6 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    size='first_week_audi',
    color='genre',
    hover_name='movieNm',
    size_max=40,
    title='개봉일 스크린수 vs 총 관객수 (점 크기: 개봉 첫 주 관객수)',
    labels={
        'first_scrn': '개봉일 스크린수 (개)',
        'total_audi': '총 관객수 (명)',
        'first_week_audi': '첫 주 관객수 (명)',
        'genre': '장르'
    }
)

fig6.update_traces(
    hovertemplate='<b>%{hovertext}</b><br>장르: %{fullData.name}<br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명<br>첫 주 관객수: %{marker.size:,}명'
)

fig6.update_layout(
    xaxis_title='개봉일 스크린수 (개)',
    yaxis_title='총 관객수 (명)'
)

st.plotly_chart(fig6, use_container_width=True)

# 구분 구역 및 여섯 번째 그래프 설명 영역
st.divider()
st.info("💡 **이 그래프로 알 수 있는 것:** 대체로 스크린 수가 많을 수록,초기 관객수가 많을 수록 총 관객수가 증가하는 추세이지만 왕과 사는 남자처럼 초기 관객수가 많지 않음에도 총관객수는 많은 경우가 존재할 수도 있습니다")

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 일곱 번째 그래프: 국가 -> 장르 선버스트 그래프
# ---------------------------------------------------------
st.subheader("7. 제작 국가 및 장르별 영화 편수 분포 (선버스트)")

# Plotly 선버스트 생성 (계층 구조: nation -> genre, 칸 크기: 영화 편수)
fig7 = px.sunburst(
    df,
    path=['nation', 'genre'],
    title='제작 국가 및 장르별 영화 편수 비율'
)

# 마우스 호버 시 구분/장르명 및 영화 편수 표시 설정
fig7.update_traces(
    hovertemplate='<b>국가/장르:</b> %{label}<br><b>영화 편수:</b> %{value}편'
)

st.plotly_chart(fig7, use_container_width=True)

# 구분 구역 및 일곱 번째 그래프 설명 영역
st.divider()
st.info("💡 **이 그래프로 알 수 있는 것:** 한국은 드라마, 일본은 애니메이션, 미국은 다양한 장르의 관객수가 분포되어있는 것을 보았을 때 그 나라에서 어떠한 영화의 종류를 좋아하는지 알 수 있습니다")

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 여덟 번째 그래프: 주요 제작 국가별 1위 흥행 영화 비교 (막대그래프)
# ---------------------------------------------------------
st.subheader("8. 주요 제작 국가별 1위 흥행 영화 비교")

# 주요 국가(한국, 미국, 일본 등)의 관객수 1위 영화만 추출
target_nations = ['한국', '미국', '일본']
top1_list = []

for nation in target_nations:
    df_nat = df[df['nation'] == nation].sort_values(by='total_audi', ascending=False)
    if not df_nat.empty:
        top1_list.append(df_nat.iloc[0])

df_top1 = pd.DataFrame(top1_list)

# 막대 상단에 표시할 텍스트 생성 (영화명 + 관객수)
df_top1['display_text'] = df_top1.apply(
    lambda row: f"<b>{row['movieNm']}</b><br>({row['total_audi']:,}명)", axis=1
)

# Plotly 막대그래프 생성
fig8 = px.bar(
    df_top1,
    x='nation',
    y='total_audi',
    color='genre',
    text='display_text',
    hover_name='movieNm',
    title='주요 제작 국가별 최다 관객수 1위 영화',
    labels={
        'nation': '제작 국가',
        'total_audi': '총 관객수 (명)',
        'genre': '장르'
    }
)

# 막대 바깥쪽 상단에 텍스트 표기 및 호버 설정
fig8.update_traces(
    textposition='outside',
    hovertemplate='<b>국가:</b> %{x}<br><b>1위 영화:</b> %{hovertext}<br><b>장르:</b> %{fullData.name}<br><b>총 관객수:</b> %{y:,}명'
)

# Y축 범위에 여유를 두어 텍스트 잘림 방지
max_audi = df_top1['total_audi'].max() if not df_top1.empty else 1000000
fig8.update_layout(
    xaxis_title='제작 국가',
    yaxis_title='총 관객수 (명)',
    yaxis=dict(range=[0, max_audi * 1.25]),
    bargap=0.4
)

st.plotly_chart(fig8, use_container_width=True)

# 구분 구역 및 여덟 번째 그래프 설명 영역
st.divider()
st.info("💡 **이 그래프로 알 수 있는 것:** 각 국가별 역대 가장 많은 관객을 동원한 1위 영화를 직접적으로 비교할 수 있습니다. 한국, 미국, 일본 각 나라의 최다 흥행작과 관객수 규모를 한눈에 파악할 수 있습니다.")
