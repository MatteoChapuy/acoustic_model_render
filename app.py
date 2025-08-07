import dash_mantine_components as dmc
from dash import Dash

app = Dash(external_stylesheets=[dmc.styles.ALL], suppress_callback_exceptions=True)
app.title = "Acoustic Model Dashboard"

server = app.server