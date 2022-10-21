from time import sleep
from tqdm import tqdm
for i in tqdm(range(10)):
    sleep(3)
    
import pandas as pd


countries = pd.read_xml("http://api.worldbank.org/v2/country/USA/indicator/AG.LND.CREL.HA?per_page=500")

countries[["date","value"]] = countries[["date","value"]]/100
"""
countries = await get_all_countries_df()
if not countries:
    raise HTTPException(status_code=500, detail=errore_message)
return countries["name"].tolist()
"""

"""
countries = await get_all_countries_df()
if not countries:
    raise HTTPException(status_code=500, detail=errore_message)
return countries["name"][countries["region.iso2code"]==region].tolist()
"""

"""Returns all the countries in a given region, as a list"""
"""
countries = await get_all_countries_df()
if not countries:
    raise HTTPException(status_code=500, detail=errore_message)
return countries[["name","iso2Code","region.value","region.iso2code"]].to_dict()
"""

"""
agricultural_land_surface = await get_data_df(agro_land_srfc_ind,country)
if not agricultural_land_surface:
    raise HTTPException(status_code=500, detail=errore_message)
#return agricultural_land_surface['date'].tolist()
return agricultural_land_surface.to_dict()
"""

"""
try:
    return agricultural_land_surface['value'].iloc[0]
except IndexError:
    raise HTTPException(status_code=404, detail="Data not found")
except:
    raise HTTPException(status_code=500, detail=errore_message) 
#return agricultural_land_surface['value'].iloc[0]
"""

"""
cereal_yield = await get_data_df(cereal_yield_ind,country)
if not cereal_yield:
    raise HTTPException(status_code=500, detail=errore_message)
"""

"""
cereal_yield = await get_data_df(cereal_yield_ind,country,year=year)
if not cereal_yield:
    raise HTTPException(status_code=500, detail=errore_message)
try:
    return cereal_yield['value'].iloc[0]
except IndexError:
    raise HTTPException(status_code=404, detail="Data not found")
except:
    raise HTTPException(status_code=500, detail=errore_message)
"""

"""
cereal_land = await get_data_df(cereal_land_ind,country)
if not cereal_land:
    raise HTTPException(status_code=500, detail=errore_message)
return cereal_land.to_dict()
"""

"""
cereal_land = await get_data_df(cereal_land_ind,country,year=year)
if not cereal_land:
    raise HTTPException(status_code=500, detail=errore_message)
try:
    return int(cereal_land['value'].iloc[0])
except IndexError:
    raise HTTPException(status_code=404, detail="Data not found")
except:
    raise HTTPException(status_code=500, detail=errore_message)
#return cereal_land.to_dict()


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

async def get_data_df(indicator,countryiso2code,year=None,record_num=500):
    url_str = api_link.format(indicator=indicator, countryiso2code=countryiso2code,record_num=record_num)
    if year:
        url_str+=f"&date={year}"
    print(url_str)
    try:
        agro_data = pd.read_xml(url_str)
        agro_data = agro_data[["date","value"]]
        agro_data.fillna(0,inplace=True)
        agro_data["value"] = agro_data["value"].astype(float)
        #agro_data.set_index('date', inplace=True)
        return agro_data
    except KeyError:
        return []
"""