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
def load_data():
    df = pd.read_csv("data/movies_genres_summary.csv")
    return df


df = load_data()

# Show a multiselect widget with the genres using `st.multiselect`.
genres = st.multiselect(
    "Genres",
    df.genre.unique(),
    ["Action", "Adventure", "Biography", "Comedy", "Drama", "Horror"],
)

# Show a slider widget with the years using `st.slider`.
years = st.slider("Years", 1986, 2006, (2000, 2016))

# Filter the dataframe based on the widget input and reshape it.
df_filtered = df[(df["genre"].isin(genres)) & (df["year"].between(years[0], years[1]))]
df_reshaped = df_filtered.pivot_table(
    index="year", columns="genre", values="gross", aggfunc="sum", fill_value=0
)
df_reshaped = df_reshaped.sort_values(by="year", ascending=False)


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
