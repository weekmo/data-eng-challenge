from cProfile import label
from turtle import st
import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc

host = "http://127.0.0.1:8000"
consts = {
    "contries_and_region":"{host}/countrieswithcode",
    "agro-land":"{host}/agro-surface/{selected_country}",
    "land":"{host}/cereal-land/{selected_country}",
    "yield":"{host}/cereal-yield/{selected_country}",
    "cereal-land-yield-bar":"{host}/cereal-land-yield-bar"
}

drop_style = {
    "display": "inline-block",
    "minWidth": "250px",
     }

def get_reg_country_dict():
    df_countries = pd.read_json(consts["contries_and_region"].format(host=host))
    df_countries.sort_values(by=['country'], inplace=True)
    reg_country_dict = {reg:{row['countryisocode']: row['country'] for _,row in df_countries[df_countries["region"] == reg].iterrows()} for reg in df_countries["region"].unique()}
    first_reg = list(reg_country_dict.keys())[0]
    del df_countries
    return reg_country_dict, first_reg

def get_data_from_api(url_name,selected_country):
    url = consts[url_name].format(host=host, selected_country=selected_country)
    #print(url)
    return pd.read_json(url)

def get_layout(suffix):
    reg_country_dict = get_reg_country_dict()
    return html.Div(children=[
    #html.H1(children=page_name),
        html.Div(children=[
            html.Div([
            html.P("Select Region"),
            dcc.Dropdown([reg for reg in reg_country_dict[0].keys()],
                id=f"region-drop-{suffix}",
                clearable=False,
                value=reg_country_dict[1],
                style=drop_style),
            html.P("Select Country"),
            dcc.Dropdown(id=f"countries-drop-{suffix}",clearable=False,
            style=drop_style),
            ]),
            html.Br(),
            
            dbc.Checklist(
                id=f"log-options-{suffix}",
                options=[
                    {"label":"Log xaxis", "value":"x"},
                    {"label":"Log yaxis", "value":"y"},
                ],
                inline=True,
                switch=True
            )
        ]
    ),
    html.Div(children=[
        dcc.Graph(id=f'line-graph-{suffix}')#,
            #figure=px.line(data_frame, x="date", y="value", markers=True,title=f"{countries_hash[countryisocode]}'s Agricultural Land Curface"))
    ]),
    html.Div(id =f"container-div-{suffix}"),
    dcc.Store(f"store-dataframe-{suffix}")
])