# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 14:42:12 2022

@author: HassaM3
"""

import datetime
import dash
from dash import Dash, html, dcc
#import dash_bootstrap_components as dbc

external_scripts = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js",
]

external_stylesheets = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css"
]

app = Dash(__name__, 
    use_pages=True,
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets)
app.title = "World Bank Data analysis"

app.layout = html.Div([
    html.Nav([html.A(f"{page['name']}", href=page["relative_path"], className="nav-link", style={"color": "#FFFFFF"} ) for page in dash.page_registry.values()],className="navbar navbar-dark bg-primary h4"),
    #html.H1('World Bank Data analysis'), navbar-dark bg-primary, style={"color": "#FFFFFF"}
    dash.page_container,
    html.Br(),
    html.Footer(f"Copyright © BASF {datetime.date.today().year}")
])

#print(dash.page_registry.values())

if __name__ == '__main__':
    app.run_server(debug=True)