# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 23:34:20 2022

@author: weekm
"""

import pandas as pd
import requests
from fastapi import FastAPI
import numpy as np

app = FastAPI()

df_countries = pd.read_xml("http://api.worldbank.org/v2/country?per_page=1000")
df_countries = df_countries[["iso2Code", "name", "region", "capitalCity"]]
df_countries = df_countries[df_countries["region"]!="Aggregates"]
df_countries.set_index("iso2Code", inplace=True)

sr_regions = df_countries["region"].unique()

df_countries2 = None
with requests.get("http://api.worldbank.org/v2/country?per_page=1000&format=json") as req:
    df_countries2 = pd.json_normalize(req.json()[1])

df_countries2 = df_countries2[["iso2Code", "name", "capitalCity", "region.iso2code","region.value"]]
df_countries2 = df_countries2[df_countries2["region.value"]!="Aggregates"]