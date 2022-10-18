import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd

df_countries = pd.read_json("http://127.0.0.1:8000/countrieswithcode")
df_countries.sort_values(by=['name'], inplace=True)

countries_hash = {country['iso2Code']: country['name'] for _,country in df_countries.iterrows()}
countryisocode = list(countries_hash.keys())[0]

data_frame = pd.read_json(f"http://127.0.0.1:8000/agro-surface/{countryisocode}")
max_year = data_frame['date'].max()
min_year = data_frame['date'].min()


del df_countries
page_name = "Country's Agricultural Land Curface"

dash.register_page(__name__, name=page_name)



layout = html.Div(children=[
    #html.H5(children=page_name),
    
    html.Div(children=[
        dcc.Dropdown(
            [{'label':val,'value':key} for key,val in countries_hash.items()],
            id="countries-drop",
            clearable=False,
            value=countryisocode
        )
    ]),
    html.Div(children=[
        dcc.Graph(id='agro-land-line-graph')#,
            #figure=px.line(data_frame, x="date", y="value", markers=True,title=f"{countries_hash[countryisocode]}'s Agricultural Land Curface"))
    ]),
    dcc.RangeSlider(min_year,max_year,1, id='year-range-slider', marks={i:{'label':f'{i}'} for i in range(min_year,max_year)}),
    html.Br()
])

@callback(
    Output("agro-land-line-graph", "figure"),
    Input("countries-drop", "value")
)
def update_line_graph(selected_country):
    data_frame_update = pd.read_json(f"http://127.0.0.1:8000/agro-surface/{selected_country}")
    fig = px.line(data_frame_update, x="date", y="value", 
        title=f"{countries_hash[selected_country]}'s Agricultural Land Curface", 
        markers=True,
        #log_y=True
    )
    #fig.update_traces(textposition="bottom right")
    fig.update_layout(transition_duration=500,
        xaxis_title='Years',
        yaxis_title='Agricultural Land Curface (in sq. km)')
    """
    max_year = data_frame["date"].max()
    min_year = data_frame["date"].min()
    range_slider = dcc.RangeSlider(
        id="year-range-slider1",
        min=min_year,
        max=max_year,
        step=1,
        value=[min_year,max_year]
        )
        """
    return fig

def get_data_df(url):
    data_frame = pd.read_json(url)
