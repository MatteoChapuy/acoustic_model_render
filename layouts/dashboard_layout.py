from dash import html, dcc
import dash_mantine_components as dmc
from callbacks import dashboard_callbacks

layout = [
    dcc.Location(id="dashboard-url"),
    dmc.Grid(
        gutter="md",
        children=[
            dmc.GridCol(
                [
                    dmc.Paper(
                        [
                            dmc.Title("Parameters", order=4),
                            dmc.MultiSelect(
                                label="Model(s) section",
                                data=["Acventum (delhom)", "Nord2000 (delhom)", "Nord2000 (windPro)",
                                      "BE2 (Iso9613)", "Iso9613 (windPro)", "ISO9613_2024 (delhom)",
                                      "ISO9613_2024 (delhom_module_meteo_ISO)",
                                      "ISO9613_2024 (delhom_module_meteo_CONCAWE)"],
                                value=["Nord2000 (delhom)"],
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
                                    data=["Mountain", "Flat"],
                                    value="Mountain",
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
                        withBorder=True, shadow="md", p="lg", radius="md"
                    ),
                    dmc.Paper(
                        [dmc.Title("Topography", order=4),
                         dmc.Container(id="topography-chart"),
                         ],
                        withBorder=True, shadow="md", p="lg", radius="md", mt=20),
                ],
                span=4
            ),
            dmc.GridCol(
                [
                    dmc.Paper(
                        [dmc.Title("Wind Turbine", order=4),
                         dmc.Select(
                             label="Source type",
                             data=["example"],
                             value="example",
                             id="source-select",
                         ),
                         dmc.Container(id="wind-turbine-card"),

                         ],
                        withBorder=True, shadow="md", p="lg", radius="md"),
                    dmc.Paper(
                        [dmc.Title("Global SPL", order=4),
                         dmc.Container(id="global-chart-container", h="auto")],
                        withBorder=True, shadow="md", p="lg", radius="md", mt=20)
                ],
                span=4),
            dmc.GridCol(
                [dmc.Paper(
                    [dmc.Title("Excess Attenuation", order=4),
                     dmc.Container(id="attenuation-chart-container", h=700)],
                    withBorder=True, shadow="md", p="lg", radius="md"),
                ],
                span=4
            )
        ]
    ),

]
