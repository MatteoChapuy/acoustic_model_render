import dash_mantine_components as dmc
from callbacks import appshell_callbacks
from dash_iconify import DashIconify

logo = "assets/logo.png"

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Title("Delhom - Acoustic Model Dashboard", order=2),
                ],
                h="100%",
                px="md",
            )
        ),
        dmc.AppShellMain(children=dmc.Container(id="root-container", fluid=True)),
    ],
    header={"height": 50},
    padding="md",
    id="appshell",
)
