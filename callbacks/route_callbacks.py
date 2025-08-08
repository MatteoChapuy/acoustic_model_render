from app import app
from dash import dcc, html, Output, Input, State
from layouts import dashboard_layout

@app.callback(
    Output("root-container", "children"),
    Input("url", "pathname"),
)
def display_page(pathname):
    if pathname == "/dashboard" or pathname == "/":
        return dashboard_layout.layout
    else:
        return "Page Not Found"