import dash
from dash import html, dcc

page_name = "Country’s Agricultural Land Surface"

dash.register_page(__name__,path='/', name=page_name)

layout = html.Div(children=[
    html.H1(children=page_name),
    html.Div(children='''
        This is our Home page content.
    ''')
])