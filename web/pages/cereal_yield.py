from datetime import date, timedelta,datetime
import dash
from dash import html, dcc, Output, Input, callback

page_name = "Cereal Yield of Country"

dash.register_page(__name__, path='/arch', name=page_name)
dpVals = [
    "Mon",
    "Klark",
    "Sam",
    "James"
]
def layout():
    return  html.Div(children=[
        html.H1(children=page_name),
        html.Div(children=f'''
            This is our Archive page content.
        '''),
        html.Br(),
        dcc.Dropdown(
            id="metal-filter",
            #className="dropdown",
            options=[{"label": metal, "value": metal} for metal in dpVals],
            value="Sam",
            clearable=False
        ),
        html.Div(id="div-output"),
        dcc.DatePickerRange(
            id="date-range",
            min_date_allowed= datetime.now() - timedelta(days=-6),
            max_date_allowed=datetime.now() + timedelta(days=10),
            start_date=datetime.now(),
            end_date=datetime.now(),
            initial_visible_month=datetime.now(),
            display_format="DD.MM.YYYY"
        )
])

@callback(
    Output(component_id="div-output", component_property= "children"),
    Input("metal-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date")
)
def update_outout(drop_val, start_date, end_date):
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
    
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
    
    return f"{drop_val} is allowed to come from {start_date_string} to {end_date_string}."