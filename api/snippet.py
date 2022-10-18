import pandas as pd
df_countries = pd.read_xml("http://api.worldbank.org/v2/country?per_page=1000")
df_countries = df_countries[["iso2Code", "name", "region", "capitalCity"]]
df_countries = df_countries[df_countries["region"]!="Aggregates"]
df_countries.set_index("iso2Code", inplace=True)

sr_regions = df_countries["region"].unique()
try:
    agro_data = pd.read_xml(f"http://api.worldbank.org/v2/country/SD/indicator/AG.LND.CREL.HA?per_page=500&date=2020")
    agro_data = agro_data[["date","value"]]
    agro_data.fillna(0,inplace=True)
    val = agro_data['value'].iloc[0]
except KeyError:
    print(KeyError)

agro_dict = agro_data.to_dict('series')
print(agro_data['date'])


# http://api.worldbank.org/v2/country/all/indicator/AG.YLD.CREL.KG
# https://api.worldbank.org/v2/en/indicator/AG.LND.CREL.HA