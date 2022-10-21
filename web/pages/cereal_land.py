import dash
from dash import  dcc, callback, Input, Output
import pandas as pd
import plotly.express as px
from modules.utils import get_reg_country_dict, get_layout, get_data_from_api

page_name = "Cereal Land"

dash.register_page(__name__,path='/cereal-land', name=page_name, suppress_callback_exceptions=True)

reg_country_dict = get_reg_country_dict()
suffix = "land"
layout = get_layout(suffix)

@callback(
    Output("countries-drop-land","options"),
    Output("countries-drop-land","value"),
    Input("region-drop-land","value")
)
def get_countries_by_region(region):
    countries = reg_country_dict[0][region]
    first_country_in_reg = list(countries.keys())[0]
    return countries,first_country_in_reg

@callback(
    Output("container-div-land","children"),
    Output("store-dataframe-land","data"),
    Input("countries-drop-land", "value")
)
def update_line_graph_by_country(selected_country):
    data_frame_update_land = get_data_from_api(suffix,selected_country)
    max_year = data_frame_update_land["date_year"].max()
    min_year = data_frame_update_land["date_year"].min()
    range_slider = dcc.RangeSlider(
        id="year-range-slider-land",
        min=min_year,
        max=max_year,
        step=1,
        value=[min_year,max_year],
        marks={i:{'label':f"{i}"} for i in range(min_year,max_year,5)}
        )
    return range_slider, data_frame_update_land.to_json()


@callback(
    Output("line-graph-land", "figure"),
    Input("store-dataframe-land","data"),
    Input("year-range-slider-land","value"),
    Input("log-options-land","value")
)

def get_data(stored_dataframe, years,graph_log):
    data_frame_from_store_land = pd.read_json(stored_dataframe)
    data_frame_from_store_land = data_frame_from_store_land[data_frame_from_store_land["date_year"].between(years[0],years[1])]
    log_x = False
    log_y = False
    if graph_log:
        log_x = "x" in graph_log
        log_y = "y" in graph_log
    fig = px.line(data_frame_from_store_land, x="date_year", y="cereal_land", 
        title=page_name, 
        markers=True,
        log_y=log_y,
        log_x=log_x,
        #text="date"
    )
    fig.update_layout(transition_duration=500,
        xaxis_title='Years',
        yaxis_title=page_name),
    return fig