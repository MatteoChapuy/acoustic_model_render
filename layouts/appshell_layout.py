import dash_mantine_components as dmc
from callbacks import appshell_callbacks
from dash_iconify import DashIconify

logo = "assets/logo.png"

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Burger(
                        id="mobile-burger",
                        size="sm",
                        hiddenFrom="sm",
                        opened=False,
                    ),
                    dmc.Burger(
                        id="desktop-burger",
                        size="sm",
                        visibleFrom="sm",
                        opened=True,
                    ),
                    dmc.Title("Acoustic Model Dashboard"),
                ],
                h="100%",
                px="md",
            )
        ),
        dmc.AppShellNavbar(
            id="navbar",
            children=[
                dmc.Button('Dashboard', variant="outline", mt="sm", id="nav-dashboard-btn",
                           leftSection=DashIconify(icon="si:dashboard-horz-line")),
                dmc.Button('Importer', variant="outline", mt="sm", id="nav-import-btn",
                           leftSection=DashIconify(icon="solar:import-outline")),
            ],
            p="md",
        ),
        dmc.AppShellMain(children=dmc.Container(id="root-container", fluid=True)),
    ],
    header={"height": 60},
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"mobile": True, "desktop": False},
    },
    padding="md",
    id="appshell",
)
