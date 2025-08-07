import os
from dash import Input, Output, callback, dcc, html, no_update
import dash_mantine_components as dmc
import plotly.graph_objects as go
import pandas as pd
from dash_ag_grid import AgGrid


def get_topography_chart(df, distance):
    df = df.rename(columns={"X (m)": "x", "Z (m)": "elevation"})
    df["x"] = df["x"].round(2)
    df["elevation"] = df["elevation"].round(1)

    # Interpolate elevation at x = 1000 if needed
    receiver_elevation = (
        df[df["x"] == distance]["elevation"].values[0]
    )
    marker_2_y = round(receiver_elevation + 2, 1)

    fig = go.Figure()

    # Main topography line
    fig.add_trace(go.Scatter(
        x=df["x"],
        y=df["elevation"],
        mode="lines",
        name="Topographie",
    ))

    # Source
    fig.add_trace(go.Scatter(
        x=[0],
        y=[df["elevation"][0] + 100],
        mode="markers+text",
        name="Source",
        marker=dict(size=10, symbol="circle"),
        text=["S"],
        textposition="top center"
    )),

    # Receiver
    fig.add_trace(go.Scatter(
        x=[distance],
        y=[marker_2_y],
        mode="markers+text",
        name="Receiver",
        marker=dict(size=10, symbol="circle"),
        text=["R"],
        textposition="top center"
    ))

    fig.update_layout(
        template="ggplot2",
        height=300,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_title="Distance (m)",
        yaxis_title="Élévation (m)",
        yaxis=dict(range=[-10, 300]),
        showlegend=False
    )

    return dcc.Graph(figure=fig)


def get_attenuation_chart(df, models, flow_resistivity, distance, wind_speed, wind_direction):
    wind_direction_dict = {
        "downwind": 0,
        "upwind": 90,
        "crosswind": 180
    }
    filtered = df[
        (df["flow_resistivity"] == float(flow_resistivity)) &
        (df["distance"] == int(distance)) &
        (df["wind_speed"] == int(wind_speed)) &
        (df["wind_direction"] == wind_direction_dict[wind_direction])
        ]

    # Create figure
    fig = go.Figure()
    attenuation_cols = models
    color_map = {
        "Acventum (delhom)": "red",
        "Nord2000 (delhom)": "green",
        "Nord2000 (windPro)": "orange",
        "BE2 (Iso9613)": "blue",
        "Iso9613 (windPro)": "purple"
    }
    for col in attenuation_cols:
        fig.add_trace(go.Scatter(
            x=filtered["frequency"],
            y=filtered[col],
            mode="lines+markers",
            name=col,
            line=dict(color=color_map[col])
        ))

    fig.update_layout(
        title="Atténuation vs Fréquence",
        xaxis_title="Fréquence (Hz)",
        yaxis_title="Atténuation (dB)",
        xaxis_type="log",
        template="plotly_white",
        height=800,
        showlegend=True
    )

    return dcc.Graph(figure=fig)


@callback(Output("csv-select", "data"),
          Input("dashboard-url", "pathname"))
def update_csv_list(_):
    csv_files = [f for f in os.listdir("data/results") if f.endswith(".csv")]
    return csv_files


@callback(
    Output("topography-chart", "children"),
    Input("topography-select", "value"),
    Input("distance-select", "value")
)
def load_and_display_topography(n, distance):
    df = pd.read_csv("data/topography/mountain.csv".format(n))
    return get_topography_chart(df, int(distance))


@callback(
    Output("attenuation-chart-container", "children"),
    Input("csv-select", "value"),
    Input("models-select", "value"),
    Input("topography-select", "value"),
    Input("flow-resistivity-select", "value"),
    Input("distance-select", "value"),
    Input("wind-speed-select", "value"),
    Input("wind-direction-select", "value")
)
def update_attenuation_chart(csv_name, models, topography, flow_resistivity, distance, wind_speed, wind_direction):
    if csv_name :
        if models :
            df = pd.read_csv(f"data/results/{csv_name}")
            return get_attenuation_chart(
                df,
                models,
                flow_resistivity,
                distance,
                wind_speed,
                wind_direction
            )
        else:
            return no_update
    else:
        return no_update
