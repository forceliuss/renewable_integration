import pandas as pd
from pandas.api.types import CategoricalDtype

import warnings
warnings.filterwarnings('ignore')

import numpy as np

# 1 toe = 11.63 (MWh) = 7.33 (Barrels of oil equivalent)
# 1 Ktoe = 1.163 (GWh) 
# 1 Ktoe = 7330 (Barrels of oil equivalent) 

######## Creating the country database
def cntry():
    #Import country names, codes and regions
    df = pd.read_csv('./data/cntry_database.csv', sep=';')
    df = df.rename(columns={'continent' : 'cntry_region','name':'cntry_name','code':'cntry_code'})
    
    #Cleaning the countries dataframe, exclusing the antarctic regions
    cntry_df = df[df['cntry_region']!='Antarctica North']
    cntry_df = cntry_df.sort_values('cntry_name')
    
    return cntry_df


######## Cleaning the Renewable Energy database
def renw(file):
    #Narrowing the time series to 25 year long
    start_date = 1990
    end_date = 2015
    
    #Converting to GWh
    ktoe_gwh = 0.1163
    
    #Inputing the data
    df = pd.read_csv(file)

    #First Formating and Cleanup
    df = df.rename(str.lower, axis='columns')
    df = df.rename(columns={'flag codes' : 'flag_codes', 'value':'value_ktoe'})
    df = df.fillna(0)

    df['time'] = pd.to_datetime(df['time'], format="%Y")
    df['year'] = df['time'].dt.year
    
    #Deleting the other type of measure
    df = df[df['measure']=='KTOE']

    #Deleting the L values rows
    dfl = df[df['flag_codes']!='L'] 
    dfl = dfl.drop(columns=['flag_codes'])

    #Create the countries dataframe
    cntry_df = cntry()

    #Merging the DF to have the countries names on my DF
    merged_df = pd.merge(dfl, cntry_df, left_on='location', right_on='cntry_code', how='left')

    #Cleaning the general values such as World; G20 and European Union
    codes_drop = ['WLD','EU28','OECD','G20','OEU']
    merged_df = merged_df[~merged_df['location'].isin(codes_drop)]

    #Reorganizing the dataframe
    merged_df['value_gwh'] = merged_df['value_ktoe']*ktoe_gwh
    merged_df = merged_df[['time','year','cntry_code','cntry_name','cntry_region','value_ktoe','value_gwh']]

    #Categorizing the location by continent
    reg_cont = ['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']
    reg_type = CategoricalDtype(categories=reg_cont, ordered=False)
    merged_df['cntry_region'] = merged_df['cntry_region'].astype(reg_type)
    
    #Filtering the dates
    renw_df = merged_df[(merged_df['year'] >= start_date)&(merged_df['year'] <= end_date)]
    
    return renw_df


######## Cleaning the GDP database
def gdp(file):
    
    #Narrowing the time series to 25 year long
    start_date = 1990
    end_date = 2015
    
    #Inputing the data
    df = pd.read_csv(file)
    
    df = df.sort_values('year')
    df = df[(df['year'] >= start_date)&(df['year'] <= end_date)]
    df = df[['country_code','year','value']]

    #Create the countries dataframe
    cntry_df = cntry()

    df = df.rename(columns={'country_code':'cntry_code','year':'year','value':'gdp'})
    df['gdp'] = df['gdp'] #GDP in dollars (USD)
    gpd_df = df[df['cntry_code'].isin(cntry_df['cntry_code'].unique())]

    gpd_df = gpd_df.merge(cntry_df, how='inner')
    gpd_df = gpd_df[['cntry_code','cntry_name','cntry_region','year','gdp']]
    
    return gpd_df