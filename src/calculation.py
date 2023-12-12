import time
import streamlit as st

import pandas as pd
import plotly.express as px

import numpy as np
import seaborn as sn

import matplotlib.pyplot as plt

plt.style.use('ggplot')

from cleaning import *

#Correlation Renewables and GDP

ren = renw_clean()
gdp = gdp_clean()
oil_price = oil_clean()


########## Converting KTOE of reneable energy production into Dollar (Trilions)

# 1 toe = 11.63 (MWh) = 7.33 (Barrels of oil equivalent)

kto_gwh = 11.63 # 1 Ktoe = 11.63 (GWh) 
kto_bo = 7330 # 1 Ktoe = 7330 (Barrels of oil equivalent) 


ren = ren.rename(columns={'value' : 'value_ktoe'})

ren['value_boe'] = ren['value_ktoe']*kto_bo
ren['value_gwhe'] = ren['value_ktoe']*kto_gwh

#Simplifying the dataframes
ren = ren[['year','cntry_code','cntry_name','cntry_region','value_ktoe','value_gwhe','value_boe']]

#Merge the oil price with the ren production
main_df = pd.merge(ren,oil_price, on='year', how='inner')

#Calculating the total
main_df['usd_t'] = main_df['value_boe']*main_df['oil_price'] / 10**9


# NEXT STEPS
########### Compare the oil production and value with the renewable production and value

########### Using the oil price prediction, predict the renewable production for the next 5 years



