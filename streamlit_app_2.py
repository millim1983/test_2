import altair as alt
import pandas as pd
import streamlit as st



# Show the page title and description.

st.set_page_config(page_title='황삭 가공 제조 데이터 분석',page_icon=':factory:'), # This is an emoji shortcode. Could be a URL too.
st.title(":factory: 제조데이터 분석 프로젝트")
st.write(
    """
    빅데이터 분석의 첫걸음!  
    제조데이터 분석을 위한 데이터 시각화 표출 대시보드입니다.   
    다양한 그래프들을 활용하여 데이터 특성을 시각적으로 나타냈습니다.  
    변수들을 조정하며 데이터의 특성을 찾아봅시다. 
    """
)


# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).
@st.cache_data
def get_data():
    # 원본데이터를 불러와 전처리하는 과정을 넣을 것 
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    location = 'https://raw.githubusercontent.com/millim1983/bigdata_project01/main/steel_ai_01_on.csv'
    raw_df = pd.read_csv(location, header = 0)

    # MIN_YEAR = 1960
    # MAX_YEAR = 2022

    # The data above has columns like:
    # FACTORY	공장코드
    # WORK_SHAPE	작업조(1근/2근/3근)
    # INPUT_ED	투입되는 소재의 외경(mm)
    # INPUT_LENGTH	투입되는 소재의 개별 길이(mm)
    # INPUT_QTY	투입 총 수량(개)
    # DIRECTION_ED	가공 후 목표 외경(mm)
    # OUTPUT_ED	생산된 소재의 외경(mm)
    # STEEL_CATEGORY	투입 강종 분류
    # WORK_START_DT	작업시작일시
    # WORK_END_DT	작업종료일시
    #
    # 종속변수
    # diff = WORK_END_DT -  WORK_START_DT
    # INPUT_QTY
    # OUTPUT_ED
    # 투입되는 소재 총길이 = 

    # 데이터 타입 변경

    raw_df = raw_df.astype({'STEEL_CATEGORY' : 'category'})  # STEEL_CATEGORY 값이 6개이므로 타입을 category로 변경
    raw_df = raw_df.astype({'WORK_SHAPE':'object'})  # WORK_SHAPE은 숫자이지만, 작업조를 나타냄 1근, 2근 3근 > object로 변경

    # 중복데이터 제거 

    raw_df = raw_df.drop_duplicates()

    # 종속변수 추가 
    raw_df['work_start_dt_ns'] = pd.to_datetime(raw_df['WORK_START_DT'])
    raw_df['work_end_dt_ns'] = pd.to_datetime(raw_df['WORK_END_DT'])

    raw_df['diff'] = (raw_df['work_end_dt_ns'] - raw_df['work_start_dt_ns']).dt.total_seconds().div(60).astype(int)


    # # 원본의 year 별 gdp 를 year vs gdp 로 변환하는 과정 
    # # So let's pivot all those year-columns into two: Year and GDP
    # gdp_df = raw_gdp_df.melt(
    #     ['Country Code'],
    #     [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
    #     'Year',
    #     'GDP',
    # )
    # # Convert years from string to integers
    # gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])


    return raw_df

df = get_data()

print(df.columns.unique())

# Show a multiselect widget with the genres using `st.multiselect`.
cols = st.multiselect(
    "변수를 살펴보세요!",
    df.columns.unique(),
    ['FACTORY', 'WORK_SHAPE', 'INPUT_ED', 'INPUT_LENGTH', 'INPUT_QTY',
    'DIRECTION_ED', 'OUTPUT_ED', 'STEEL_CATEGORY', 'WORK_START_DT',
    'WORK_END_DT', 'work_start_dt_ns', 'work_end_dt_ns', 'diff'],
)

# Show a slider widget with the years using `st.slider`.
diff = st.slider("작업시간", -60, 500, (0, 120))


# Filter the dataframe based on the widget input and reshape it.
df_filtered = df.loc[df['diff'].between(diff[0], diff[1]),cols]
df_reshaped = df_filtered.pivot_table(
    index="diff", columns="cols", values="gross", aggfunc="sum", fill_value=0
)
df_reshaped = df_reshaped.sort_values(by="year", ascending=False)

'''
# Display the data as a table using `st.dataframe`.
st.dataframe(
    df_reshaped,
    use_container_width=True,
    column_config={"year": st.column_config.TextColumn("Year")},
)

# Display the data as an Altair chart using `st.altair_chart`.
df_chart = pd.melt(
    df_reshaped.reset_index(), id_vars="year", var_name="genre", value_name="gross"
)
chart = (
    alt.Chart(df_chart)
    .mark_line()
    .encode(
        x=alt.X("year:N", title="Year"),
        y=alt.Y("gross:Q", title="Gross earnings ($)"),
        color="genre:N",
    )
    .properties(height=320)
)
st.altair_chart(chart, use_container_width=True)

'''