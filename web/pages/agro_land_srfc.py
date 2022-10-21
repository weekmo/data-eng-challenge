import dash
from dash import  dcc, callback, Input, Output, State
import plotly.express as px
import pandas as pd
from modules.utils import get_reg_country_dict, get_layout,get_data_from_api

reg_country_dict = get_reg_country_dict()

page_name = "Agricultural Land Curface"

dash.register_page(__name__, name=page_name, suppress_callback_exceptions=True, path="/")
suffix = "agro-land"
layout = get_layout(suffix)

@callback(
    Output("countries-drop-agro-land","options"),
    Output("countries-drop-agro-land","value"),
    Input("region-drop-agro-land","value")
)
def get_countries_by_region(region):
    countries = reg_country_dict[0][region]
    first_country_in_reg = list(countries.keys())[0]
    return countries,first_country_in_reg

@callback(
    Output("container-div-agro-land","children"),
    Output("store-dataframe-agro-land","data"),
    Input("countries-drop-agro-land", "value")
)
def update_line_graph_by_country(selected_country):
    data_frame_update = get_data_from_api(suffix,selected_country)
    max_year = data_frame_update["date_year"].max()
    min_year = data_frame_update["date_year"].min()
    range_slider = dcc.RangeSlider(
        id="year-range-slider-agro-land",
        min=min_year,
        max=max_year,
        step=1,
        value=[min_year,max_year],
        marks={i:{'label':f"{i}"} for i in range(min_year,max_year,5)}
        )
    return range_slider, data_frame_update.to_json()


@callback(
    Output("line-graph-agro-land", "figure"),
    State("store-dataframe-agro-land","data"),
    Input("year-range-slider-agro-land", "value")
)

def get_data(stored_dataframe, years=None):
    data_frame_from_store = pd.read_json(stored_dataframe)
    data_frame_from_store = data_frame_from_store[data_frame_from_store["date_year"].between(years[0],years[1])]
    fig = px.line(data_frame_from_store, x="date_year", y="agro_srfc", 
        title=page_name, 
        markers=True,
    )
    fig.update_layout(transition_duration=500,
        xaxis_title='Years',
        yaxis_title='Agricultural Land Curface (in sq. km)')

    return fig
