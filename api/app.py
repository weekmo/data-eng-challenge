# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 23:34:20 2022

@author: weekm
"""

import pandas as pd
import requests
from fastapi import FastAPI

app = FastAPI()

async def get_all_countries_df(record_num:int = 500):
    df_countries = None
    with requests.get(f"http://api.worldbank.org/v2/country?format=json&per_page={record_num}") as req:
        df_countries = pd.json_normalize(req.json()[1])

    df_countries = df_countries[["iso2Code", "name", "capitalCity", "region.iso2code","region.value"]]
    return df_countries[df_countries["region.value"]!="Aggregates"]

async def get_agro_land_srfc_df(countryiso2code):
    try:
        agro_data = pd.read_xml(f"http://api.worldbank.org/v2/country/{countryiso2code}/indicator/AG.LND.AGRI.ZS")
        agro_data = agro_data[["date","value"]]
        
        agro_data.fillna(0,inplace=True)
        #agro_data.set_index('date', inplace=True)
        return agro_data
    except KeyError:
        return []

@app.get("/")
async def index():
    return "It works, it is none"


@app.get("/countries")
async def get_all_countries():
    """Returns all the countries in a given region, as a list"""
    countries = await get_all_countries_df()
    return countries["name"].tolist()

@app.get("/countries/{region}")
async def get_countries(region):
    """Returns all the countries in a given region, as a list"""
    countries = await get_all_countries_df()
    return countries["name"][countries["region.iso2code"]==region].tolist()




@app.get("/agro-surface/{country}")
async def get_agro_land_srfc_all_years(country):
    """Returns a country’s agricultural land surface (in sq. km)..."""
    agricultural_land_surface = await get_agro_land_srfc_df(country)
    return agricultural_land_surface['date'].tolist()

@app.get("/agro-surface/{country}/{year}")
async def get_agro_land_srfc(country, year:int):
    """Returns a country’s agricultural land surface (in sq. km) for a given
    year, as a float."""
    agricultural_land_surface = await get_agro_land_srfc_df(country)
    agricultural_land_surface = agricultural_land_surface[agricultural_land_surface['date']==year]
    try:
        return agricultural_land_surface['value'].iloc[0]
    except IndexError:
        return 0.0
    except KeyError:
        return "Currect the input parameters"
    return agricultural_land_surface['value'].iloc[0]






@app.get("/cereal-yield/{country}}/{year}")
async def get_cereal_yield(country, year:int):
    """Returns the cereal yield of a country for a given year (in kg/hectare, as
    an integer. If no year is provided, returns list of all available years..."""
    # . . . your code here . . .
    cereal_yield = None
    return cereal_yield


@app.get("/cereal-land/{country}}/{year}")
async def get_cereal_land(country, year:int):
    """Returns the land of a country dedicated to cereal production, for a given
    year (in hectares) ..."""
    # . . . your code here . . .