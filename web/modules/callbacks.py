from dash import dcc, callback, Input, Output
import pandas as pd
import plotly.express as px
from modules.utils import get_reg_country_dict


reg_country_dict = get_reg_country_dict()

@callback(
    Output("countries-drop-yield","options"),
    Output("countries-drop-yield","value"),
    Input("region-drop-yield","value")
)
def get_countries_by_region(region):
    countries = reg_country_dict[0][region]
    first_country_in_reg = list(countries.keys())[0]
    return countries,first_country_in_reg

@callback(
    Output("container-div-yield","children"),
    Output("store-dataframe-cereal-yield","data"),
    Input("countries-drop-yield", "value")
)
def update_line_graph_by_country(selected_country):
    data_frame_update_yield = pd.read_json(f"http://127.0.0.1:8000/cereal-yield/{selected_country}")
    max_year = data_frame_update_yield["date"].max()
    min_year = data_frame_update_yield["date"].min()
    range_slider = dcc.RangeSlider(
        id="year-range-slider-yield",
        min=min_year,
        max=max_year,
        step=1,
        value=[min_year,max_year],
        marks={i:{'label':f"{i}"} for i in range(min_year,max_year,5)}
        )
    return range_slider, data_frame_update_yield.to_json()


@callback(
    Output("cereal-yield-line-graph", "figure"),
    Input("store-dataframe-cereal-yield","data"),
    Input("year-range-slider-yield","value"),
    Input("log-options-yield","value")
)

def get_data(stored_dataframe, years,graph_log):
    data_frame_from_store_yield = pd.read_json(stored_dataframe)
    data_frame_from_store_yield = data_frame_from_store_yield[data_frame_from_store_yield["date"].between(years[0],years[1])]
    log_x = False
    log_y = False
    if graph_log:
        log_x = "x" in graph_log
        log_y = "y" in graph_log
    fig = px.line(data_frame_from_store_yield, x="date", y="value", 
        title="page_name", 
        markers=True,
        log_y=log_y,
        log_x=log_x,
        #text="date"
    )
    fig.update_layout(transition_duration=500,
        xaxis_title='Years',
        yaxis_title='Agricultural Land Curface (in sq. km)'),
    return fig