# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 23:34:20 2022

@author: weekm
"""

import pandas as pd
import requests
from fastapi import FastAPI

app = FastAPI()

agro_land_srfc_ind = "AG.LND.TOTL.K2"
cereal_yield_ind = "AG.YLD.CREL.KG"
cereal_land_ind = "AG.LND.CREL.HA"
api_link = "http://api.worldbank.org/v2/country/{countryiso2code}/indicator/{indicator}?per_page={record_num}"

async def get_all_countries_df(record_num:int = 500):
    df_countries = None
    with requests.get(f"http://api.worldbank.org/v2/country?format=json&per_page={record_num}") as req:
        df_countries = pd.json_normalize(req.json()[1])

    df_countries = df_countries[["iso2Code", "name", "capitalCity", "region.iso2code","region.value"]]
    return df_countries[df_countries["region.value"]!="Aggregates"]

async def get_data_df(indicator,countryiso2code, record_num=500,date_year=""):
    url_str = api_link.format(indicator=indicator, countryiso2code=countryiso2code,record_num=record_num)
    if date_year != "":
        url_str+="&date="+str(date_year)
    print(url_str)
    try:
        agro_data = pd.read_xml(url_str)
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

@app.get("/countrieswithcode")
async def get_all_countries_with_code():
    """Returns all the countries in a given region, as a list"""
    countries = await get_all_countries_df()
    return countries[["name","iso2Code"]].to_dict()


@app.get("/agro-surface/{country}")
async def get_agro_land_srfc_all_years(country):
    """Returns a country’s agricultural land surface (in sq. km)..."""
    agricultural_land_surface = await get_data_df(agro_land_srfc_ind,country)
    #return agricultural_land_surface['date'].tolist()
    return agricultural_land_surface.to_dict()

@app.get("/agro-surface/{country}/{year}")
async def get_agro_land_srfc(country, year:int):
    """Returns a country’s agricultural land surface (in sq. km) for a given
    year, as a float."""
    agricultural_land_surface = await get_data_df(agro_land_srfc_ind,country)
    agricultural_land_surface = agricultural_land_surface[agricultural_land_surface['date']==year]
    try:
        return agricultural_land_surface['value'].iloc[0]
        
    except IndexError:
        return None
    except KeyError:
        return "Currect the input parameters"
    #return agricultural_land_surface['value'].iloc[0]



@app.get("/cereal-yield/{country}")
async def get_cereal_yield_all_years(country):
    """Returns list of all available years..."""
   
    cereal_yield = await get_data_df(cereal_yield_ind,country)
    return cereal_yield.to_dict()

@app.get("/cereal-yield/{country}/{year}")
async def get_cereal_yield(country, year:int):
    """Returns the cereal yield of a country for a given year (in kg/hectare, as
    an integer."""
   
    cereal_yield = await get_data_df(cereal_yield_ind,country,date_year=year)
    return cereal_yield['value'].iloc[0]




@app.get("/cereal-land/{country}")
async def get_cereal_land_all_years(country):
    """Returns the land of a country dedicated to cereal production, for a given
    year (in hectares) ..."""
    cereal_land = await get_data_df(cereal_land_ind,country)
    return cereal_land.T.to_dict()
    
@app.get("/cereal-land/{country}/{year}")
async def get_cereal_land(country, year:int):
    """Returns the land of a country dedicated to cereal production, for a given
    year (in hectares) ..."""
    cereal_land = await get_data_df(cereal_land_ind,country,date_year=year)
    return int(cereal_land['value'].iloc[0])
    #return cereal_land.to_dict()