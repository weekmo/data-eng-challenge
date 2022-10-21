# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 08:29:04 2022

@author: HassaM3
"""
# TODO: convert hectare to km2
import pandas as pd
import requests

import models
from database import engine, SessionLocal


record_num = 500
db = SessionLocal()
meta = models.Base.metadata
meta.create_all(bind=engine)

for tb in reversed(meta.sorted_tables):
    db.execute(f"delete from {tb.name}")
db.commit()

df_countries = None
df_regions = None
with requests.get(f"http://api.worldbank.org/v2/country?format=json&per_page={record_num}") as req:
    df_countries = pd.json_normalize(req.json()[1])

if df_countries is not None:
    df_countries = df_countries[["id", "name", "capitalCity", "region.id","region.value"]]
    df_countries = df_countries[df_countries["region.value"]!="Aggregates"]
    df_regions = df_countries.drop_duplicates(subset="region.value")[["region.id","region.value"]]
    df_regions.columns = ["isocode","name"]

df_regions.to_sql("tb_regions", con=engine,if_exists='append', index=False)
del df_regions

region_from_db_df = pd.read_sql("select id, isocode from tb_regions", con=engine)

df_countries = df_countries.merge(region_from_db_df, how="left", left_on="region.id", right_on="isocode", suffixes=('_country', '_region'))
df_countries = df_countries[["name","id_country","id_region"]]
df_countries.columns = ["name","isocode","region_id"]
df_countries.to_sql("tb_countries", con=engine,if_exists='append', index=False)


agro_df = pd.DataFrame()
indicators = {
    "agro_srfc":"AG.LND.TOTL.K2",
    "cereal_land":"AG.LND.CREL.HA",
    "cereal_yield":"AG.YLD.CREL.KG"}

api_link = "http://api.worldbank.org/v2/country/{countryiso2code}/indicator/{indicator}?per_page={record_num}"

for country in db.query(models.Country).all():
    agro_df = pd.DataFrame()
    for key, val in indicators.items():
        url = api_link.format(countryiso2code=country.isocode,indicator=val, record_num=record_num)
        try:
            temp_df = pd.read_xml(url)
            temp_df = temp_df[["date","value"]]
            if key == "cereal_land":
                temp_df["value"] = temp_df["value"] / 100
            elif key == "cereal_yield":
                temp_df["value"] = temp_df["value"] * 100
            temp_df.columns = ["date_year",key]
            if "date_year" in agro_df:
                agro_df = agro_df.merge(temp_df, on="date_year")
            else:
                agro_df = temp_df
        except:
            print(url)
            continue
    #agro_df[["cereal_land","cereal_yield"]] = agro_df[["cereal_land","cereal_yield"]] * 100
    agro_df["country_id"] = country.id
    agro_df.to_sql("tb_agro", con=engine,if_exists='append', index=False)

""" 
    for country in db.query(models.Country).all():
        temp_df = pd.read_xml(api_link.format(countryiso2code=country.isocode,indicator=ind, record_num=record_num))
"""      
#for country in db.query(models.Country).