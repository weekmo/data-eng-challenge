import pandas as pd
df_countries = pd.read_xml("http://api.worldbank.org/v2/country?per_page=1000")
df_countries = df_countries[["iso2Code", "name", "region", "capitalCity"]]
df_countries = df_countries[df_countries["region"]!="Aggregates"]
df_countries.set_index("iso2Code", inplace=True)

sr_regions = df_countries["region"].unique()
try:
    agro_data = pd.read_xml(f"http://api.worldbank.org/v2/country/US/indicator/AG.LND.AGRI.ZS")
    agro_data = agro_data[["date","value"]]
except KeyError:
    print(KeyError)

agro_dict = agro_data.to_dict('series')
print(agro_data['date'])
