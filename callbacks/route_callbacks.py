from app import app
from dash import dcc, html, Output, Input, State
from layouts import import_layout, dashboard_layout

@app.callback(
    Output("root-container", "children"),
    Input("url", "pathname"),
)
def display_page(pathname):
    if pathname == "/dashboard":
        return dashboard_layout.layout
    elif pathname == "/import":
       return import_layout.layout
    else:
        return "Page Not Found"