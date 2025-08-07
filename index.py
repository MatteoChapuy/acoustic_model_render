from app import app
import dash_mantine_components as dmc
from dash import dcc, html
from layouts import appshell_layout
from callbacks import route_callbacks

theme = {
    "primaryColor": "gray",
    "defaultRadius": "sm",
    "components": {
        "Card": {
            "defaultProps": {
                "shadow": "lg"
            }
        }
    }
}

app.layout = dmc.MantineProvider(
    children=[
        dcc.Location(id="url"),
        dmc.NotificationContainer(
            id="notification-container",
        ),
        appshell_layout.layout
        ],
    theme=theme,
    forceColorScheme="light"
)

if __name__ == "__main__":
    app.run(host="localhost", port=8050, debug=True)