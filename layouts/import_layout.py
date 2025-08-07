from dash import html, dcc
import dash_mantine_components as dmc
from callbacks import import_callbacks

layout = dmc.Container([
    dcc.Location(id="import-url"),
    dmc.Stack(children=[
        dcc.Upload(
            id="upload-data",
            children=dmc.Button("Importer un nouveau fichier CSV de résultats", variant="light", color="red"),
            multiple=False,
            style={"cursor": "pointer"},
        ),
        dmc.Container(id="uploaded-csv-container")
    ], align="flex-start", justify="start"),

], fluid=True)
