import time
import streamlit as st

import pandas as pd
import plotly.express as px

import numpy as np
import seaborn as sn

import warnings
warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt

plt.style.use('ggplot')

#Importing the datafram from cleaning file
from cleaning import *
from calculation import *

st.set_page_config(
    page_title="Renewable Dashboard",
    page_icon=":infinity:",
    layout="wide",
    initial_sidebar_state="expanded"
)

#Sidebar config
st.sidebar.title('Dashboard')

#Calling the merged_df
renw = renw('./data/renewable_energy.csv')
gdp = gdp('./data/gdp_data.csv')
oil = oil('./data/oilprice_data.csv')

#Merging Renewable and GDP
merged_df = pd.merge(renw,gdp, how='inner')\
    .sort_values('year')
    
merged_df = merged_df.merge(oil, how='inner')

#Selecting the continent
merged_df = merged_df.sort_values('cntry_region')
cntry_reg = st.sidebar.selectbox("Continent",merged_df['cntry_region'].unique())
df_c = merged_df[merged_df['cntry_region'] == cntry_reg] #Selecting the continent from Merge dataframe
df_c = df_c.sort_values('cntry_name')

#Selecting the country
cntry = st.sidebar.selectbox("Country",df_c['cntry_name'].unique())
df_mt = df_c[df_c['cntry_name'] == cntry] #Selecting the country from Renewable dataframe
df_mt = df_mt.sort_values('year')


################# FIRST SECTION
sec_1 = st.container()

#Section 1 - Header
sec_1.subheader('Resumo Total - %s' %cntry, divider='grey')

#Page layout
col1, col2 = sec_1.columns(2, gap='large')

#Printing Metrics
gdp_boe = gdp_boe(df_mt)
md_per = round(gdp_boe['per'].mean(),3)
std_per = round(gdp_boe['per'].std(),3)
col1.metric(label="Renewable Weight (%)", value=md_per, delta=std_per)
#gdp_boe
#df_mt

#Ploting the total production Year
fig_total = px.bar(df_mt, x='year', y='value')
col1.plotly_chart(fig_total, use_container_width=True)

#Ploting the total GDP Year
gdp_total = px.line(df_mt, x='year', y='gdp')
col2.plotly_chart(gdp_total, use_container_width=True)

################# SECOUND SECTION
sec_2 = st.container()

#Section 1 - Header
sec_2.subheader('Oil price', divider='grey')

oil_total = px.line(oil, x='year', y='oil_price')
sec_2.plotly_chart(oil_total, use_container_width=True)

#Merging the ren and the oil prices with label columns

#Page Layout
#col3, col4 = sec_2.columns(2, gap='large')

#Correlation Renewable and GPD
df_pt = cntry_mean(df_c)
df_pt = df_pt.groupby('cntry_name').mean()
df_pt
#fig_corr = px.scatter(gdp_boe, x='per', y='gdp', size='value_ktoe', color='cntry_name',
#           hover_name='cntry_name', log_x=True, size_max=30)
#sec_2.plotly_chart(fig_corr, use_container_width=True)


