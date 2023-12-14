import time
import streamlit as st

import pandas as pd
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')

#Importing the cleaning file
from cleaning import *

################# STREAMLIT PAGE SETUP

st.set_page_config(
    page_title="Renewable Dashboard",
    page_icon=":infinity:",
    layout="wide",
    initial_sidebar_state="expanded"
)

#Sidebar config
st.sidebar.title('Select Country')

#Calling the merged_df
renw = renw('./data/renewable_energy.csv')
gdp = gdp('./data/gdp_data.csv')
oil = oil('./data/oilprice_data.csv')

#Merging Renewable and GDP
merged_df = pd.merge(renw,gdp, how='inner')\
    .sort_values('year')

################# SIDEBAR

#Selecting the continent
merged_df = merged_df.sort_values('cntry_region')

cntry_reg = st.sidebar.selectbox("Continent:",merged_df['cntry_region'].unique())

df_c = merged_df[merged_df['cntry_region'] == cntry_reg] 
df_c = df_c.sort_values('cntry_name')

#Selecting the country
cntry = st.sidebar.selectbox("Country:",df_c['cntry_name'].unique())

df_selection = df_c[df_c['cntry_name'] == cntry]
df_selection = df_selection.sort_values('year')

#Time Range
time_range = st.sidebar.slider(
    'Time range:',
    1990, 2015, (1990, 2015)
)

df_selection = df_selection[(df_selection['year'] >= time_range[0])&(df_selection['year'] <= time_range[1])]
renw = renw[(renw['year'] >= time_range[0])&(renw['year'] <= time_range[1])]

st.title(":bar_chart: Renewable Integration Dashboard")
st.markdown("###")

################# Section 1 - Metrics

sec_1 = st.container()
sec_1.subheader(cntry, divider='grey')

#Page layout
col1, col2, col3 = sec_1.columns(3, gap='large')

#KPIs

total_production = round(df_selection['value'].sum()/1000,3)
average_renw = round(df_selection['value'].mean(),2)
std_renw = round(df_selection['value'].std(),2)
delta_renw = round(std_renw / average_renw,2)

#Ranking
renw['value'] = round(renw['value'],2)
df_ranking = renw[['cntry_name','value']]
df_ranking = df_ranking.groupby(by=['cntry_name']).sum()\
    .sort_values('value', ascending=False)
df_ranking['ranking'] = range(1, len(df_ranking['value']) + 1)

world_ranking = df_ranking.query(
    'cntry_name == @cntry'
)

#Printing KPI

col1.metric(
    label="Average Production:",
    value='%s Ktoe'%average_renw,
    delta=delta_renw,
    help='Ktoe - kilo ton of oil equivalent'
)

col2.metric(
    label="Total Production:",
    value='%s Mtoe'%total_production,
    help='Mtoe - Mega ton of oil equivalent'
)

col3.metric(
    label=":star2: World Ranking:",
    value='%iº' %world_ranking['ranking'].values[0]
)

################# Section 2 - Charts

sec_2 = st.container()
#Page layout
col3, col4 = sec_2.columns(2, gap='large')

#Ploting the total production Year
fig_total = px.bar(
    df_selection, 
    x='year', 
    y='value',
    title=f'Renewable Production ({time_range[0]} - {time_range[1]})',
    labels={
        'year':'Year',
        'value':'Kton Oil Equivalent (Ktoe)' 
    }
)
col3.plotly_chart(
    fig_total,
    use_container_width=True
)

#Ploting the total GDP Year
gdp_total = px.line(
    df_selection,
    x='year',
    y='gdp',
    title=f'GDP USD ({time_range[0]} - {time_range[1]}) ',
    labels={
        'year':'Year',
        'gdp':'GDP (USD)' 
    }
)
col4.plotly_chart(
    gdp_total,
    use_container_width=True
)


#################  RESET STREAMLIT
hide_st_style="""
            <style>
            #MainMenu {visibility:hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)

