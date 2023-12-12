import pandas as pd
from pandas.api.types import CategoricalDtype

import warnings
warnings.filterwarnings('ignore')

import numpy as np


######## Cleaning the Renewable Energy database
def renw_clean():
    
    #Inputing the data
    df = pd.read_csv('./data/renewable_energy.csv')

    #First Formating and Cleanup
    df = df.rename(str.lower, axis='columns')
    df = df.rename(columns={'flag codes' : 'flag_codes'})
    df = df.fillna(0)

    df['time'] = pd.to_datetime(df['time'], format="%Y")
    df['year'] = df['time'].dt.year
    
    #Deleting the other type of measure
    df = df[df['measure']=='KTOE']

    #Deleting the L values rows
    dfl = df[df['flag_codes']!='L'] 
    dfl = dfl.drop(columns=['flag_codes'])

    #Loading the countries file
    df_countries = pd.read_csv('./data/cntry_database.csv', sep=';')
    df_countries = df_countries.rename(columns={'continent' : 'cntry_region','name':'cntry_name','code':'cntry_code'})

    #Cleaning the countries dataframe, exclusing the antarctic regions
    df_countries = df_countries[df_countries['cntry_region']!='Antarctica North']

    #Merging the DF to have the countries names on my DF
    merged_df = pd.merge(dfl, df_countries, left_on='location', right_on='cntry_code', how='left')

    #Cleaning the general values such as World; G20 and European Union
    codes_drop = ['WLD','EU28','OECD','G20','OEU']
    merged_df = merged_df[~merged_df['location'].isin(codes_drop)]

    #Reorganizing the dataframe
    merged_df = merged_df[['time','year','cntry_code','cntry_name','cntry_region','measure','subject','value']]

    #Categorizing the location by continent
    reg_cont = ['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']
    reg_type = CategoricalDtype(categories=reg_cont, ordered=False)
    merged_df['cntry_region'] = merged_df['cntry_region'].astype(reg_type)
    return merged_df


######## Cleaning the GDP database
def gdp_clean():
    
    #Inputing the data
    df = pd.read_csv('.\data\gdp_data.csv')
    
    df = df.sort_values('year')
    df = df[df['year'] <= 2015]
    df = df[['country_code','year','value']]

    df_countries = pd.read_csv('./data/cntry_database.csv', sep=';')
    df_countries = df_countries.rename(columns={'continent' : 'cntry_region','name':'cntry_name','code':'cntry_code'})

    df = df.rename(columns={'country_code':'cntry_code','year':'year','value':'gdp'})
    df['gdp'] = df['gdp'] #GDP in dollars (USD)
    gpd_df = df[df['cntry_code'].isin(df_countries['cntry_code'].unique())]

    gpd_df = gpd_df.merge(df_countries, how='inner')
    gpd_df = gpd_df[['cntry_code','cntry_name','cntry_region','year','gdp']]
    
    return gpd_df

def oil_clean():
    
    #Inputing the data
    df = pd.read_csv('.\data\oilprice_data.csv')

    #Rename the columns
    df = df.rename(columns={'Date' : 'date','Price':'oil_price'})
    
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df = df[df['year']<=2015]
    
    df_oil = df[['year','oil_price']]
    df_oil = df_oil.groupby('year').mean()
    df_oil = df_oil.reset_index()
    
    return df_oil