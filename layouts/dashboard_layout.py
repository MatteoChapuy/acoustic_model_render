from dash import html, dcc
import dash_mantine_components as dmc
from callbacks import dashboard_callbacks

layout = [
    dcc.Location(id="dashboard-url"),
    dmc.Grid(
        gutter="md",
        children=[
            dmc.GridCol(
                [dmc.Paper(
                    [
                        dmc.Title("Load Data", order=2),
                        dmc.Select(
                            id="csv-select",
                            placeholder="Select CSV file...",
                            data=[],
                            clearable=False,
                            searchable=True,
                            mt=10
                        ),
                    ], withBorder=True, shadow="md", p="lg", radius="md", mt=20
                ),
                    dmc.Paper(
                        [
                            dmc.Title("Parameters", order=2),
                            dmc.MultiSelect(
                                label="Model(s) section",
                                data=["Acventum (delhom)", "Nord2000 (delhom)", "Nord2000 (windPro)",
                                      "BE2 (Iso9613)",
                                      "Iso9613 (windPro)"],
                                id="models-select",
                            ),
                            dmc.Flex([
                                dmc.Select(
                                    label="Flow resistivity (Ray/m)",
                                    data=["12.5", "2000"],
                                    value="12.5",
                                    id="flow-resistivity-select",
                                ),
                                dmc.Select(
                                    label="Distance (m)",
                                    data=["500", "1000", "1500"],
                                    id="distance-select",
                                    value="500",
                                )
                            ],
                                gap="md",
                                justify="center",
                                align="center",
                                direction="row",
                            ),
                            dmc.Flex([
                                dmc.Select(
                                    label="Wind Speed at 10m (m/s)",
                                    data=["3", "5", "7", "9"],
                                    value="3",
                                    id="wind-speed-select",
                                ),
                                dmc.Select(
                                    label="Topography (m)",
                                    data=["Montain"],
                                    value="Montain",
                                    id="topography-select",
                                )
                            ],
                                gap="md",
                                justify="center",
                                align="center",
                                direction="row",
                            ),
                            dmc.Flex([
                                dmc.Select(
                                    label="Wind direction",
                                    data=["downwind", "crosswind", "upwind"],
                                    value="downwind",
                                    id="wind-direction-select",
                                ),
                            ],
                                gap="md",
                                justify="center",
                                align="center",
                                direction="row",
                            ),
                        ],
                        withBorder=True, shadow="md", p="lg", radius="md", mt=20
                    ),
                    dmc.Paper(
                        [dmc.Title("Topography", order=3),
                         dmc.Container(id="topography-chart"),
                         ],
                        withBorder=True, shadow="md", p="lg", radius="md", mt=20)],
                span=4
            ),
            dmc.GridCol(
                dmc.Paper(
                    [dmc.Title("Excess Attenuation", order=3),
                     dmc.Container(id="attenuation-chart-container")],
                    withBorder=True, shadow="md", p="lg", radius="md", mt=20),
                span=8
            )
        ]
    ),

]
