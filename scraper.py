#!/usr/bin/env python3

import sys
import os
import pandas as pd
import numpy as np
import pandas as pd
import folium
import urllib
import json
import socket
from ipwhois import IPWhois
import pycountry
import io
import requests
import xarray as xr
import numpy as np
import pandas as pd
import holoviews as hv
import geoviews as gv
import geoviews.feature as gf
import geoviews.tile_sources as gts
import geopandas

from bokeh.palettes import YlOrBr3 as palette

import cartopy
from cartopy import crs as ccrs

from bokeh.tile_providers import STAMEN_TONER
from bokeh.models import WMTSTileSource

hv.notebook_extension('bokeh')

DATA_PATH = "data/"
DATA_PATH = "data/"
MAP_PATH = DATA_PATH + "world.geo.json/countries/"
COUNTRY_CODE_DATA = DATA_PATH + "country-codes/data/country-codes.csv"

try:
    day = sys.argv[1]
    mounth = sys.argv[2]
    year = sys.argv[3]
except:
    print("Arguemnts should be like :")
    print("python scraper.py 'day' 'mounth' 'year'")

TOTAL_DAYS = int(day) + 30 * int(mounth) + 365 * int(year)
print("Total days : " + str(TOTAL_DAYS))

def isNaN(num):
    return num != num

def get_export_names():
    file = open(DATA_PATH + "event_table_name", "r")
    names = file.readlines()[0].split(" ")
    return names

def get_mentions_names():
    file = open(DATA_PATH + "mentions_table_name", "r")
    names = file.readlines()[0].split(" ")
    return names

def get_map_site():
    file = pd.read_csv(COUNTRY_CODE_DATA)
    return dict(zip(file['TLD'], file['ISO3166-1-Alpha-3'])), dict(zip(file['ISO3166-1-Alpha-3'], file['TLD']))

def scrape_list(url_ex, url_men, export_df, mentions_df):
    '''
    This function will use the list of export.csv and mentions.csv files to cash their contents and only keep relavant
    columns
    '''
    for i in range(url_ex.shape[0]):
        # Appending is slightly faster than Concat when ignore_index=True, so we used append to add  new scraped dataFrame
        ## But appending gets inefficient for large dataFrame, so instead of appending the new scraped dataframe to a ...
        ## ... large dataFrame, we recursively call our function to use a new empty dataFrame for appending to achieve...
        ## ... much faster speed in scraping large number of dataframes
        if i>= 100:
            level_f += 1
            export_df_2 = pd.DataFrame(columns=col_ex_list)
            mentions_df_2 = pd.DataFrame(columns=col_men_list)
            export_df_2, mentions_df_2 = scrape_list(url_ex.iloc[100:], url_men.loc[100:], export_df_2, mentions_df_2)
            export_df = export_df.append(export_df_2,ignore_index=True)
            mentions_df = mentions_df.append(mentions_df_2,ignore_index=True) 
            break
        else:
            s_ex=requests.get(url_ex.iloc[i])
            s_men = requests.get(url_men.iloc[i])
            if s_ex.status_code==200 and s_men.status_code==200:
                df_i_m=pd.read_csv(io.BytesIO(s_ex.content), sep='\t', compression='zip', names=col_ex)
                df_i_x=pd.read_csv(io.BytesIO(s_men.content), sep='\t',compression='zip', names=col_men)
                export_df = export_df.append(df_i_m[col_ex_list],ignore_index=True)
                mentions_df = mentions_df.append(df_i_x[col_men_list],ignore_index=True)
    return export_df, mentions_df
     


url='http://data.gdeltproject.org/gdeltv2/masterfilelist.txt'
s=requests.get(url).content

df_list=pd.read_csv(io.StringIO(s.decode('utf-8')), sep='\s', header=None, names=['Size', 'Code', 'url'])

df_list = df_list.dropna(subset=['url'])

print(df_list['url'].head())

print(df_list[df_list['url'].str.contains('.export.CSV')].head())

# We get the columns names of the datasets from the text files we've created
col_ex = get_export_names()
col_men = get_mentions_names()

# We define create a list of the column names of the columns we want to keep in the datasets
col_ex_list = ['GlobalEventID', 'Day', 'MounthYear', 'Year', 'ActionGeo_CountryCode', 'ActionGeo_Lat', 'ActionGeo_Long', 'GoldsteinScale', 'NumMentions']
col_men_list = ['GlobalEventId', 'MentionSourceName', 'Confidence', 'MentionDocTone']

# We create the empty the aggregated dataframes with the column names we want to keep
export_df = pd.DataFrame(columns=col_ex_list)
mentions_df = pd.DataFrame(columns=col_men_list)

print(col_ex)

# We filter out the urls keeping only those containing an export dataset
df_ex_w01 = df_list[df_list['url'].str.contains('.export.CSV')]
df_ex_w01 = df_ex_w01.iloc[:96*TOTAL_DAYS,2:3] #This will filter events for 7 days 

# We filter the urls keeping only those containing an export dataset
df_men_w01 = df_list[df_list['url'].str.contains('.mentions.CSV')]
df_men_w01 = df_men_w01.iloc[:96*TOTAL_DAYS,2:3] #This will filter events for 7 days

print("Load data")

# Parsing the data and returning the aggregated dataFrame
export_df, mentions_df = scrape_list(df_ex_w01['url'], df_men_w01['url'], export_df, mentions_df)

print("Save data")

# Saving the resulted dataframes
export_df.to_csv(os.path.join('results','export_df.csv'))
mentions_df.to_csv(os.path.join('results','mentions_df.csv'))

print("Load data form results")

# Loading the dataFrame
export_df = pd.read_csv('results/export_df.csv', index_col=0)
mentions_df = pd.read_csv('results/mentions_df.csv', index_col=0)

