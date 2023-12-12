import time
import streamlit as st

import pandas as pd
import plotly.express as px

import numpy as np
import seaborn as sn

import matplotlib.pyplot as plt

plt.style.use('ggplot')

#Importing the datafram from cleaning file
from cleaning import *
#from calculation import *

st.set_page_config(
    page_title="Renewable Dashboard",
    page_icon=":infinity:",
    layout="wide",
    initial_sidebar_state="expanded"
)

#Sidebar config
st.sidebar.title('Dashboard')

#Calling the merged_df
df = renw_clean()
gdp = gdp_clean()
oil = oil_clean()

#Merging
merged_df = df.merge(gdp, how='inner')\
    .sort_values('year')

#Creating the correlation
merged_df['corr'] = merged_df['value'] / (merged_df['gdp']/1000000)

#Selecting the continent
cntry_reg = st.sidebar.selectbox("Continent",df['cntry_region'].unique())
df_c = merged_df[merged_df['cntry_region'] == cntry_reg] #Selecting the continent from Merge dataframe

#Selecting the country
cntry = st.sidebar.selectbox("Country",df_c['cntry_name'].unique())
df_mt = df_c[df_c['cntry_name'] == cntry] #Selecting the country from Renewable dataframe

################# FIRST SECTION
sec_1 = st.container()

#Section 1 - Header
sec_1.subheader('Resumo Mensal - %s' %cntry, divider='grey')

#Page layout
col1, col2 = sec_1.columns(2, gap='large')

#Ploting the total production Year
fig_total = px.bar(df_mt, x='year', y='value')
col1.plotly_chart(fig_total, use_container_width=True)

#Ploting the total GDP Year
gdp_total = px.line(df_mt, x='year', y='gdp')
col2.plotly_chart(gdp_total, use_container_width=True)

################# SECOUND SECTION
sec_2 = st.container()

#Section 1 - Header
sec_2.subheader('Correlação Renewable x GDP', divider='grey')

oil_total = px.line(oil, x='year', y='oil_price')
sec_2.plotly_chart(oil_total, use_container_width=True)

#Merging the ren and the oil prices with label columns

#Page Layout
#col3, col4 = sec_2.columns(2, gap='large')

'''
#Correlation Renewable and GPD
fig_corr = px.scatter(df_c, x='year', y='gdp', size='value', color='cntry_name',
           hover_name='cntry_name', log_x=True, size_max=30)
sec_2.plotly_chart(fig_corr, use_container_width=True)
'''

