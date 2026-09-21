# ---------------------------------------------------------
# 여덟 번째 그래프: 연도/월별 주요 장르 관객수 변화 추이 (선 그래프)
# ---------------------------------------------------------
st.subheader("8. 시간에 따른 장르별 관객수 변화 추이")

# 연도별/장르별 총 관객수 집계 (결측치 제외)
df_valid_year = df.dropna(subset=['year']).copy()
df_valid_year['year'] = df_valid_year['year'].astype(int)

# 영화 편수가 많은 상위 주요 장르만 추출 (데이터 시각성 확보)
top_genres = df_valid_year['genre'].value_counts().head(7).index
df_top_genre = df_valid_year[df_valid_year['genre'].isin(top_genres)]

# 연도 & 장르별 관객수 합계 계산
genre_yearly_audi = df_top_genre.groupby(['year', 'genre'])['total_audi'].sum().reset_index()

# Plotly 선 그래프(Line Chart) 생성
fig8 = px.line(
    genre_yearly_audi,
    x='year',
    y='total_audi',
    color='genre',
    markers=True,
    title='연도별 주요 장르 관객수 변화 추이',
    labels={
        'year': '개봉 연도',
        'total_audi': '총 관객수 (명)',
        'genre': '장르'
    }
)

# 호버 서식 및 레이아웃 설정
fig8.update_traces(
    hovertemplate='<b>연도:</b> %{x}년<br><b>장르:</b> %{fullData.name}<br><b>관객수 합계:</b> %{y:,}명'
)

fig8.update_layout(
    xaxis_title='개봉 연도',
    yaxis_title='총 관객수 (명)',
    xaxis=dict(dtick=1),  # 연도 눈금 단위 설정
    hovermode='x unified', # 동일 연도의 모든 장르 관객수 한번에 보기
    height=550
)

st.plotly_chart(fig8, use_container_width=True)

# 구분 구역 및 여덟 번째 그래프 설명 영역
st.divider()
st.info("💡 **이 그래프로 알 수 있는 것:** 시간에 따라 특정 장르의 인기와 관객 수 총합이 어떻게 변화하는지 한눈에 확인할 수 있습니다. 연도별로 특정 장르가 흥행을 주도했는지 아니면 장르 전반의 관객수가 감소/증가했는지 유기적인 변화 흐름을 파악할 수 있습니다.")
