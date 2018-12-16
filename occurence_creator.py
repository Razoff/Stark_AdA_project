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
import re

from bokeh.palettes import YlOrBr3 as palette

import cartopy
from cartopy import crs as ccrs

from bokeh.tile_providers import STAMEN_TONER
from bokeh.models import WMTSTileSource

hv.notebook_extension('bokeh')

#from geolite2 import geolite2
import time

DATA_PATH = "data/"
MAP_PATH = DATA_PATH + "world.geo.json/countries/"
COUNTRY_CODE_DATA = DATA_PATH + "country-codes/data/country-codes.csv"
CATEGORY_PATH = DATA_PATH + "GDELT-Global_Knowledge_Graph_CategoryList.xlsx"
SOURCE_PATH = DATA_PATH + "data_SourceName.csv"

def get_gkg_names():
    file = open(DATA_PATH + "gkg_table_name", "r")
    names = file.readlines()[0].split(" ")
    names[-1] = names[-1][:-1]
    return names

def read_gkg(month):
    col_gkg = ['GKGRECORDID', 'DATE', 'Counts', 'SourceCommonName', 'Locations', 'DocumentIdentifier', 'V2Themes', 'Themes', 'V2Tone']
    col_gkg_list = ['GKGRECORDID', 'DATE', 'Counts', 'SourceCommonName', 'Locations', 'Themes', 'V2Tone']
    gkg_df = pd.read_csv(DATA_PATH+'gkg_'+str(month)+'.csv.gz', compression='gzip', low_memory=False,
                         index_col=0, header=0, names=col_gkg) #, usecols = col_gkg_list)
    return gkg_df

def read_gkg_csv(url):
    col_gkg = get_gkg_names()
    col_gkg_list = ['GKGRECORDID', 'DATE', 'Counts', 'SourceCommonName', 'Locations', 'Themes', 'V2Tone']
    gkg_df = pd.read_csv(url, sep='\t', names=col_gkg, usecols = col_gkg_list)

    return gkg_df

def read_category():
    category_df = pd.read_excel(CATEGORY_PATH)
    category_df=category_df.astype({'Type': str, 'Name': str, 'Description': str})
    return category_df

def read_source():
    source_df = pd.read_excel(SOURCE_PATH)
    return source_df

def aggregate_theme_per_media(gkg_df):
    gkg_df_droped = gkg_df.dropna(subset=['Themes','Locations'])
    gkg_df = gkg_df.astype({'SourceCommonName': str, 'Themes': str})

    themes_per_media = pd.DataFrame( {'Source': gkg_df_droped['SourceCommonName'],
                                      'Themes': gkg_df_droped['Themes']})

    themes_per_media = themes_per_media.groupby('Source') \
                                   .apply(lambda x: x['Themes'].sum().split(";")) \
                                   .reset_index(name='Themes')
    return themes_per_media

def check_exists(x, theme_list):
    if(x in theme_list):
        return x
    return np.nan

def theme_distribution(theme, theme_list):
    M = list(map(lambda x: (x,1), theme))
    D = pd.DataFrame(M, columns = ['Themes', 'Count']).groupby('Themes').size() \
                                                      .reset_index(name='Counts') \
                                                      .sort_values(by='Counts', ascending=False)
    D['Themes']=D['Themes'].apply(lambda x: check_exists(x, theme_list))
    D = D.dropna()
    return D['Themes'].values, D['Counts'].values

def distribution_table(themes_per_media, theme_list):

    distribution = pd.DataFrame(columns = ['Source', 'Themes', 'Counts'])

    for idx in range(themes_per_media.shape[0]):
        th, ct = theme_distribution(themes_per_media['Themes'][idx].copy(), theme_list)
        distribution = distribution.append(pd.DataFrame({"Source": themes_per_media['Source'][idx],
                                                         "Themes" : [th],
                                                         "Counts":  [ct]}))

    distribution = distribution.reset_index()
    distribution = distribution.drop('index', axis=1)

    return Distribution

def create_occurence_matrix(distribution, theme_list):

    cols = theme_list
    cols.insert(0,'Source')

    occurence_matrix = pd.DataFrame(columns = cols, index = distribution['Source'])
    occurence_matrix['Source'] = distribution['Source']
    occurence_matrix = occurence_matrix.reindex(distribution['Source'])
    occurence_matrix = occurence_matrix.fillna(0)
    occurence_matrix = occurence_matrix.drop('Source', axis=1)
    occurence_matrix = occurence_matrix.transpose()

    for idx in range(distribution.shape[0]):
        occurence_matrix[distribution['Source'][idx]][distribution['Themes'][idx]] = distribution['Counts'][idx]

    return occurence_matrix.transpose()

def extract_info_gkg(url): # or extract_info_gkg(month)
    gkg_df = read_gkg_csv(url) # or read_gkg(month)
    category_df = read_category()
    themes_per_media = aggregate_theme_per_media(gkg_df)
    theme_list = list(re.sub(r"[]\[]|\n|'", '', str(np.asarray(category_df['Name']))).split(' '))
    distribution = distribution_table(themes_per_media, theme_list)
    occurence_matrix = create_occurence_matrix(distribution, theme_list)

    return occurence_matrix

def update_occurence_matrix(old_matrix, new_matrix):

    added_sources = set(new_matrix.index) - set(old_matrix.index)
    same_sources = set(new_matrix.index) - added_sources

    new_matrix = new_matrix.transpose()
    old_matrix = old_matrix.transpose()

    old_matrix[list(same_sources)] = old_matrix[list(same_sources)] + 1*new_matrix[list(same_sources)]
    new_matrix = new_matrix.transpose()
    old_matrix = old_matrix.transpose()

    for source in list(added_sources):
        old_matrix = old_matrix.append(new_matrix[new_matrix.index == source],sort=True)
    return old_matrix

def save_matrix(matrix,i):
    file = DATA_PATH + "occurence_matrix_" + str(i) +".csv"
    #file = DATA_PATH + "occurence_matrix.csv"
    if os.path.isfile(file):
        os.remove(file)
    matrix.to_csv(file)


def read_matrix(i):
    file = DATA_PATH + "occurence_matrix_" + str(i) +".csv"
    occurence_matrix = pd.read_csv(file,index_col=0, header=0) #pd.read_csv(DATA_PATH + "occurence_matrix.csv")
    return occurence_matrix

def compute_occurence_matrix(months):
    for i in months:
        print(i)
        if(i==0):
            # or extract_info_gkg(i)
            old_matrix = extract_info_gkg('http://data.gdeltproject.org/gdeltv2/20150218234500.gkg.csv.zip')
            save_matrix(old_matrix,i) #instead of i we can also use 0 all the time for instance
        else:
            old_matrix = read_matrix(i-1)
            # or extract_info_gkg(i)
            new_matrix = extract_info_gkg('http://data.gdeltproject.org/gdeltv2/20160218234500.gkg.csv.zip')
            old_matrix = update_occurence_matrix(old_matrix, new_matrix)
            print(old_matrix.shape)
            save_matrix(old_matrix,i)

list_gkg = ['results/0to30gkg.csv.gz', 'results/210to240gkg.csv.gz', 'results/60to90gkg.csv.gz' , 'results/120to150gkg.csv.gz',  'results/30to60gkg.csv.gz','results/90to120gkg.csv.gz', 'results/150to180gkg.csv.gz',  'results/330to360gkg.csv.gz', 'results/180to210gkg.csv.gz',  'results/420to450gkg.csv.gz']

single_gkg = ['results/0to30.gkg.csv.gz']

compute_occurence_matrix(single_gkg)
