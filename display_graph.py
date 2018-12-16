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
import matplotlib.pyplot as plt

from bokeh.palettes import YlOrBr3 as palette

import cartopy
from cartopy import crs as ccrs

from bokeh.tile_providers import STAMEN_TONER
from bokeh.models import WMTSTileSource

hv.notebook_extension('bokeh')

def isNaN(num):
    return num != num

def get_export_names():
    file = open(DATA_PATH + "event_table_name", "r")
    names = file.readlines()[0].rstrip('\n').split(" ")
    return names

def get_mentions_names():
    file = open(DATA_PATH + "mentions_table_name", "r")
    names = file.readlines()[0].rstrip('\n').split(" ")
    return names

def get_gkg_names(): # GKG
    file = open(DATA_PATH + "gkg_table_name", "r")
    names = file.readlines()[0].rstrip('\n').split(" ")
    names[-1] = names[-1][:-1]
    return names

def get_map_site():
    file = pd.read_csv(COUNTRY_CODE_DATA)
    return dict(zip(file['TLD'], file['ISO3166-1-Alpha-3'])), dict(zip(file['ISO3166-1-Alpha-3'], file['TLD']))


data = pd.read_csv("~/Downloads/occurence_matrix.csv").T

def do_bags(data):
    indexes = data.index
    bags = {}

    for i in range(len(indexes)):
        bags[indexes[i]] = data.iloc[i].values
    return bags

def get_mat(data):
    ret = []
    for i in range(len(data.index)):
        ret.append(data.iloc[i].values)

    return np.array(ret).astype('int'), data.index.values.tolist()

def sort_themes(data, keep_n = 500, display_top_fifteen = True):
    themes = data.iloc[0].values
    data = data.iloc[1:]
    data["tot"] = data.apply(lambda row: np.sum(row), axis=1)

    if display_top_fifteen:
        ret = data.sort_values(by=['tot'], ascending=False)
        display(ret['tot'].head(15))

        return ret.drop(columns=['tot']).head(keep_n), themes
    else:
        return data.sort_values(by=['tot'], ascending=False).drop(columns=['tot']).head(keep_n), themes

#mat = get_mat(data)
# print(mat.shape)
#data["tot"] = data.apply(lambda row: np.sum(row), axis=1)

data_s , thems = sort_themes(data)
mat, indexes = get_mat(data_s)
print(mat.shape)
print(type(mat[0][0]))
#print(sources)

