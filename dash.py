import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import time

#this code constructs the dash page in tmdb.

st.set_page_config(
    page_title="Movie data",
    page_icon="🎬",
    layout="wide"
)

st.title('Data about cinema market')

st.text('Hello,')
st.text('This project aims to provide information that may be relevant to understanding the movie industry before, during, and after the COVID-19 pandemic.')
st.text('Data with the top 50 range, was collected from TMDB via API. Data from worldwide cinema market was extracted from box office mojo in the following page: https://www.boxofficemojo.com/year/?area=XWW&grossesOption=totalGrosses')
st.text('The documentation for fields extracted from TMDB and Box Office Mojo has been reviewed to try to minimize the potential impact of erroneous information, such as data at the "US Market" level for "Worldwide Market", but we are not responsible for erroneous information published on the TMDb movie pages. ')
#st.text('We have filtered some information like movies with runtime <10 or budget = 0 due to potential impact in the information')

df                  = pd.read_csv("clean_data.csv")
df_total_box_office = pd.read_csv("boxoffice.csv")
df_company          = pd.read_csv("clean_data_companies.csv")
df_country          = pd.read_csv("clean_data_countries.csv")
df_genres           = pd.read_csv("clean_data_genres.csv")


df_total_box_office['group_years'] = np.where(
    (df_total_box_office['year'] >= 2014) & (df_total_box_office['year'] <= 2019), '2014-2019',
    np.where(
        (df_total_box_office['year'] >= 2020) & (df_total_box_office['year'] <= 2021), '2020-2021',
        np.where(
            (df_total_box_office['year'] >= 2022) & (df_total_box_office['year'] <= 2024), '2022-2024',
            df_total_box_office['year'].astype(str)
        )
    )
)


#limiting box_office data to cover the range from tmdb data
df_total_box_office = df_total_box_office[(df_total_box_office['year'] >= df['year'].min()) & (df_total_box_office['year'] <= df['year'].max())]



#bar amount of movies by year

bar_movie_releases_by_year = px.bar(df_total_box_office, x="year", y="releases", title="amount of movie releases by year (worldwide data by box office mojo)")

bar_movie_releases_by_year.update_traces(marker_color='#E9963A',  
                  texttemplate='%{y:,.0f}',    
                  textposition='outside'
                  )
yearss = df_total_box_office['year'].tolist()
bar_movie_releases_by_year.update_layout(title_x=0.5,
                  xaxis_title="year",
                  yaxis_title="amount of movies",
                  xaxis=dict(showgrid=False, tickmode = "array", tickvals=yearss),
                  yaxis=dict(showgrid=False)
                  )

st.plotly_chart(bar_movie_releases_by_year)


#ok

#100% horizontal bar %of movie releases by year (countries as colors)
#color palette for countries
countries_colors = {
'US': '#000080',
'FR': '#DC143C',
'CN': '#B22222',
'GB': '#191970',
'HK': '#FF69B4',
'IN': '#FF8C00',
'AU': '#2E8B57',
'CA': '#8B0000',
'IS': '#4169E1',
'JP': '#A52A2A',
'BG': '#228B22',
'DK': '#800000',
'MX': '#006400',
'KR': '#000000',
'RU': '#0047AB',
'IT': '#FF9500',
'KW': '#FFFFFF',
'NL': '#C41E3A',
'RS': '#009E60',
'ZA': '#8B4513',
'HU': '#9400D3'
}

df_country['weight'] = 1 / df_country.groupby('id')['origin_country'].transform('count')



df_country_group_years = (
    df_country
    .groupby(['origin_country', 'year'])
    .agg({'weight': 'sum'})
    .reset_index()
)   

df_country_group_years['percentual']= (df_country_group_years['weight']/df_country_group_years.groupby('year')['weight'].transform('sum'))*100


df_country_group_years = df_country_group_years.sort_values(['year', 'weight'], ascending=[True, False])

horizontal_bar_movies_by_origin_country = px.bar(
    df_country_group_years, 
    x="percentual", 
    y="year",
    color="origin_country",
    color_discrete_map=countries_colors,
    text=[f"{country} ({percentual:.0f}%)" for country, percentual in zip(df_country_group_years['origin_country'], df_country_group_years['percentual'])],       
    orientation="h",  
    title="percent of movies by year and origin_country (top 50 movies by worldwide revenue - data from tmdb  — proportionally counting coproductions)", 
    labels={"percentual": "percent. of movies", "origin_country": "origin country"} 
)

horizontal_bar_movies_by_origin_country.update_layout(
                  yaxis=dict(showgrid=False, tickmode = "array", tickvals=yearss)
                  )


st.plotly_chart(horizontal_bar_movies_by_origin_country)



#100% horizontal bar %of movie releases by year (genres as colors)

#color pallete for genres
genres_colors = {
    'Action': '#FF6B35',
    'Adventure': '#3E7CB1', 
    'Comedy': '#F9C80E',
    'Science Fiction': '#8A4F7D',
    'Drama': '#4CB944',
    'Thriller': '#A65D2F',
    'Family': '#E377AF',
    'Fantasy': '#D7263D',
    'Romance': '#F6A7B5',
    'War': '#5C5C5C',
    'Animation': '#00A896',
    'Horror': '#721817',
    'Crime': '#0D7A8A',
    'Mystery': '#6A4C93',
    'History': '#8D5B4C',
    'Music': '#FF9F1C',
    'Western': '#C44536'
}


df_genres['weight'] = 1 / df_genres.groupby('id')['genres'].transform('count')



df_genres_group_years = (
    df_genres
    .groupby(['genres', 'year'])
    .agg({'weight': 'sum'})
    .reset_index()
)   

df_genres_group_years['percentual']= (df_genres_group_years['weight']/df_genres_group_years.groupby('year')['weight'].transform('sum'))*100


df_genres_group_years = df_genres_group_years.sort_values(['year', 'weight'], ascending=[True, False])

horizontal_bar_movies_by_genres = px.bar(
    df_genres_group_years, 
    x="percentual", 
    y="year",
    color="genres",
    color_discrete_map=genres_colors,
    text=[f"{genres} ({percentual:.0f}%)" for genres, percentual in zip(df_genres_group_years['genres'], df_genres_group_years['percentual'])],       
    orientation="h",  
    title="percent of movies by year and genres (top 50 movies by worldwide revenue - data from tmdb  — proportionally counting multigenre movies)", 
    labels={"percentual": "percent. of movies", "genres": "genres"} 
)

horizontal_bar_movies_by_genres.update_layout(
                  yaxis=dict(showgrid=False, tickmode = "array", tickvals=yearss)
                  )

st.plotly_chart(horizontal_bar_movies_by_genres)



#line graph total revenue by year

df_total_box_office['total_revenue_year_B'] = df_total_box_office['total_revenue_year']/1e9


line_total_box_office_by_year = px.line(df_total_box_office, x='year', y='total_revenue_year_B', 
                title="Total revenue by year", 
                line_shape='spline',text=df_total_box_office['total_revenue_year_B'])
            

line_total_box_office_by_year.update_traces(line=dict(color='#556B2F', width=3),
                    marker=dict(color='black', size=6),
                    texttemplate='%{y:,.1f}B',
                    textposition='top center') 
line_total_box_office_by_year.update_layout(
    title_x = 0.5,
    xaxis_title = "year",
    yaxis_title = "Total revenue (US$ billions)",
    xaxis=dict(showgrid=False, tickmode = "array", tickvals=yearss),
    
)

st.plotly_chart(line_total_box_office_by_year)

#line graph average movie revenue by year (box_office data - covering worldwide movies)

df_total_box_office['average_m'] = df_total_box_office['average']/1e6

line_average_box_office_by_year = px.line(df_total_box_office, x='year', y='average_m', 
                                          title='average movie revenue by year (worldwide data by box office mojo) ',
                                          line_shape='spline', text=df_total_box_office['average_m']
                                          )
line_average_box_office_by_year.update_traces(line=dict(color='#FF6B35', width=3),
                    marker=dict(color='black', size=6),
                    texttemplate='%{y:,.1f}M',
                    textposition='top center')

line_average_box_office_by_year.update_layout(
    title_x = 0.25,
    xaxis_title = "year",
    yaxis_title = "average revenue (US$ millions)",
    xaxis=dict(showgrid=False, tickmode = "array", tickvals=yearss),
    
)


#line graph average movie revenue by year (top 50 movies by worldwide revenue - data from tmdb )
df_avg_revenue_year= (
    df
    .groupby(['year'])
    .agg({'revenue': 'mean'})
    .reset_index()
)   


df_avg_revenue_year['average_m'] = df_avg_revenue_year['revenue']/1e6

line_average_box_office_by_year_top50 = px.line(df_avg_revenue_year, x='year', y='average_m', 
                                          title='average movie revenue by year (top 50 movies by worldwide revenue - data from tmdb )',
                                          line_shape='spline', text=df_avg_revenue_year['average_m']
                                          )
line_average_box_office_by_year_top50.update_traces(line=dict(color='#FF6B35', width=3),
                    marker=dict(color='black', size=6),
                    texttemplate='%{y:,.1f}M',
                    textposition='top center')

line_average_box_office_by_year_top50.update_layout(
    title_x = 0.25,
    xaxis_title = "year",
    yaxis_title = "average revenue (US$ millions)",
    xaxis=dict(showgrid=False, tickmode = "array", tickvals=yearss),
    
)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(line_average_box_office_by_year)

with col2:
    st.plotly_chart(line_average_box_office_by_year_top50)


#line graph revenue/budget of top 50 movies by year
df_avg_revenue_per_budget_year= (
    df
    .groupby(['year'])
    .agg({'revenue_per_budget': 'mean'})
    .reset_index()
)   

line_average_revenue_per_budget_by_year_top50 = px.line(df_avg_revenue_per_budget_year, x='year', y='revenue_per_budget', 
                                          title='average revenue/budget by movie (top 50 movies by worldwide revenue - data from tmdb )',
                                          line_shape='spline', text=df_avg_revenue_per_budget_year['revenue_per_budget']
                                          )
line_average_revenue_per_budget_by_year_top50.update_traces(line=dict(color='#8A4F7D', width=3),
                    marker=dict(color='black', size=6),
                    texttemplate='%{y:,.1f}M',
                    textposition='top center')

line_average_revenue_per_budget_by_year_top50.update_layout(
    title_x = 0.5,
    xaxis_title = "year",
    yaxis_title = "average revenue/budget (more is better)",
    xaxis=dict(showgrid=False, tickmode = "array", tickvals=yearss),
    
)

st.plotly_chart(line_average_revenue_per_budget_by_year_top50)

#linegraph avg runtime of top 50 movies by year 
df_avg_runtime_year= (
    df
    .groupby(['year'])
    .agg({'runtime': 'mean'})
    .reset_index()
)   

line_avg_runtime_year_top50 = px.line(df_avg_runtime_year, x='year', y='runtime', 
                                          title='avg movie runtime by year(top 50 movies by worldwide revenue - data from tmdb )',
                                          line_shape='spline', text=df_avg_runtime_year['runtime']
                                          )
line_avg_runtime_year_top50.update_traces(line=dict(color='#0D7A8A', width=3),
                    marker=dict(color='black', size=6),
                    texttemplate='%{y:.0f}m',
                    textposition='top center')

line_avg_runtime_year_top50.update_layout(
    title_x = 0.5,
    xaxis_title = "year",
    yaxis_title = "avg movie runtime",
    xaxis=dict(showgrid=False, tickmode = "array", tickvals=yearss),
    
)

st.plotly_chart(line_avg_runtime_year_top50)

