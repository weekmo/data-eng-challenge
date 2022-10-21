import dash
from dash import  dcc, callback, Input, Output, State, html
import plotly.express as px
import pandas as pd
from modules.utils import consts, host, get_reg_country_dict,get_data_from_api
import dash_bootstrap_components as dbc

#reg_country_dict = get_reg_country_dict()
page_name = "Data Analysis"
drop_style = {
    "display": "inline-block",
    "minWidth": "250px",
     }
dash.register_page(__name__, name=page_name, suppress_callback_exceptions=True, path="/analysis")
suffix = "analysis"
#    size="pop", size_max=45, log_x=True)
layout = html.Div(children=[
    #html.H1(children=page_name),
    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                dbc.Switch(
                    id="log-switch-graph1",
                    label="Log yaxis",
                    value=False,
                ),
                 dcc.Graph(id="graph-1")
            ],className="col-sm")
        ], className="row"),
        html.Div(children=[
            html.Div(children=[
                dbc.Switch(
                    id="log-switch-graph2",
                    label="Log yaxis",
                    value=False,
                ),
                dcc.Dropdown(
                    id="year-drop-graph2",
                    clearable=False,
                    style=drop_style),
                 dcc.Graph(id="graph-2")
            ],className="col-sm")
        ], className="row"),
        html.Div(children=[
            html.Div(children=[
                dbc.Switch(
                    id="log-switch-graph3",
                    label="Log yaxis",
                    value=False,
                ),
                dcc.Dropdown(
                    id="region-drop-graph3",
                    clearable=False,
                    style=drop_style),
                dcc.Dropdown(
                    id="year-drop-graph3",
                    clearable=False,
                    style=drop_style),
                dcc.Graph(id="graph-3"),
                html.Div(id="test-div")
            ],className="col-sm")
        ], className="row")
    ], 
    className="container"),
    dcc.Store("store-dataframe-cereal-land-yield")
])

@callback(
    Output("graph-3", "figure"),
    Input("log-switch-graph3","value"),
    Input("region-drop-graph3","value"),
    Input("year-drop-graph3","value")
)
def change_log_graph3(log_on, region_code,year):
    df3 = pd.read_json(consts["cereal-land-yield-bar"].format(host=host)+f"/{region_code}/{year}")
    fig3 = px.bar(df3, x="area", y="value", color="data_type", barmode="stack", log_y=log_on,
    title=f"Compare Agricultural Land Surface to Cereal Land Between Countries in MEA",
    labels={
            "area":"Regions",
            "value": "Area (in sq. km)",
            "data_type":"Area"
        }
    )
    fig3.update_layout(transition_duration=500
    )
    return fig3

@callback(
    Output("graph-2","figure"),
    Input("log-switch-graph2","value"),
    Input("year-drop-graph2","value")
)
def change_log_graph2(log_on, selected_year):
    print(selected_year)
    df2 = pd.read_json(consts["cereal-land-yield-bar"].format(host=host)+f"/{selected_year}")
    fig2 = px.bar(df2, x="area", y="value", color="data_type", barmode="stack", log_y=log_on,
    title=f"Compare Agricultural Land Surface to Cereal Land in Regions in {selected_year}",
    labels={
            "area":"Regions",
            "value": "Area (in sq. km)",
            "data_type":"Area"
        }
    )
    fig2.update_layout(transition_duration=500
    )
    return fig2

@callback(
    Output("graph-1", "figure"),
    Output("year-drop-graph2","options"),
    Output("year-drop-graph2","value"),
    Output("year-drop-graph3","options"),
    Output("year-drop-graph3","value"),
    Output("region-drop-graph3","options"),
    Output("region-drop-graph3","value"),
    Input("log-switch-graph1","value")
)
def change_log_graph1(log_on):
    # Land area (sq. km)
    df = pd.read_json(f"{host}/cereal-land-yield")
    fig = px.scatter(df, x="cereal_land", y="cereal_yield",
        #size="agro_srfc",
        color="region",hover_data=['country'],
        title="Correlation Between Cerial Land and Cereal Yield",
        log_y=log_on,
        labels={
            "cereal_land":"Land under cereal production (sq. km)",
            "cereal_yield": "Cereal yield (kg per sq. km)",
            "data_type":"Area"
        })
    fig.update_layout(
        transition_duration=500,
        legend=dict(
        orientation="h",
        yanchor="top",
        y=1.15,
        xanchor="left",
        x=0,
        
    ))
    options = df["date_year"].unique()
    first_year = options[1]
    regions = df[["region","region_code"]].drop_duplicates()
    regions = {row["region_code"]:row["region"] for _,row in regions.iterrows()}
    first_region = list(regions.keys())[0]
    return fig,options,first_year,options,first_year,regions,first_region