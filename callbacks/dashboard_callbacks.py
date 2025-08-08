from dash import Input, Output, callback, dcc, html, no_update
import dash_mantine_components as dmc
import plotly.graph_objects as go
import pandas as pd
import numpy as np

wind_direction_dict = {
    "downwind": 0,
    "upwind": 90,
    "crosswind": 180
}

color_map = {
    "Acventum (delhom)": "#E63946",  # Soft red
    "Nord2000 (delhom)": "#2A9D8F",  # Teal green
    "Nord2000 (windPro)": "#F4A261",  # Warm orange
    "BE2 (Iso9613)": "#457B9D",  # Muted blue
    "Iso9613 (windPro)": "#9D4EDD"  # Soft purple
}


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
    filtered = df[
        (df["flow_resistivity"] == float(flow_resistivity)) &
        (df["distance"] == int(distance)) &
        (df["wind_speed"] == int(wind_speed)) &
        (df["wind_direction"] == wind_direction_dict[wind_direction])
        ]

    # Create figure
    fig = go.Figure()
    attenuation_cols = models

    for col in attenuation_cols:
        fig.add_trace(go.Scatter(
            x=filtered["frequency"],
            y=filtered[col],
            mode="lines+markers",
            name=col,
            line=dict(color=color_map[col])
        ))

    fig.update_layout(
        xaxis_title="Fréquence (Hz)",
        yaxis_title="Atténuation (dB)",
        xaxis_type="log",
        yaxis=dict(range=[-30, None]),
        template="plotly_white",
        showlegend=True,
        legend=dict(
            orientation="h",  # horizontal layout
            yanchor="bottom",
            y=-0.25,  # move below plot
            xanchor="center",
            x=0.5
        )
    )
    return dcc.Graph(figure=fig)


def get_global_spl(df, models, flow_resistivity, distance, wind_speed, wind_direction, source):
    """
    Compute global SPL at receiver for each model.
    """
    source_df = pd.read_csv(f"data/sources/sources_spectrum_{source}.csv")
    source_spectrum = dict(zip(source_df["Frequency"], source_df["SPL"]))

    df_filtered = df[
        (df["flow_resistivity"] == float(flow_resistivity)) &
        (df["distance"] == int(distance)) &
        (df["wind_speed"] == int(wind_speed)) &
        (df["wind_direction"] == wind_direction_dict[wind_direction])
        ]

    spl_results = {}

    Adiv = np.round(10 * np.log10(1 / (4 * np.pi * np.square(int(distance)))), 2)
    for model in models:
        levels = []
        for _, row in df_filtered.iterrows():
            freq = int(row["frequency"])
            if freq in source_spectrum:
                Lw = source_spectrum[freq]
                att = row[model]
                Lr = Lw + Adiv + att  # SPL at receiver
                levels.append(10 ** (Lr / 10))

        if levels:
            global_spl = 10 * np.log10(sum(levels))
        else:
            global_spl = None
        spl_results[model] = round(global_spl, 1) if global_spl is not None else None

    # Create horizontal bar chart
    fig = go.Figure(go.Bar(
        x=[spl_results[m] for m in models],
        y=models,
        orientation="h",
        marker=dict(
            color=[color_map.get(m, "gray") for m in models]
        ),
        text=[f"{spl_results[m]} dB" for m in models],
        textposition="auto",
    ))

    fig.update_layout(
        xaxis_title="SPL (dB)",
        yaxis_title="Model",
        height=50 * len(models) + 100,
        bargap=0.3,
        margin=dict(l=50, r=20, t=50, b=40),
        template="plotly_white"
    )

    return dcc.Graph(figure=fig)


def get_source_spectrum_chart(source_spectrum: dict):
    # Sort frequencies to ensure ascending order
    freqs = sorted(source_spectrum.keys())
    levels = [source_spectrum[f] for f in freqs]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=freqs,
        y=levels,
        mode="lines+markers",
        name="Source Spectrum",
        line=dict(color="#264653", width=2),
        marker=dict(size=6)
    ))

    fig.update_layout(
        xaxis_title="Frequency (Hz)",
        yaxis_title="SPL (dB)",
        xaxis_type="log",  # Log scale for 1/3 octaves
        xaxis=dict(tickvals=freqs),
        template="plotly_white",
        height=250,
        margin=dict(l=40, r=20, t=50, b=40),
    )

    return dcc.Graph(figure=fig)


@callback(
    Output("topography-chart", "children"),
    Input("topography-select", "value"),
    Input("distance-select", "value")
)
def load_and_display_topography(n, distance):
    if n == "Mountain" or n == "Mountain 2":
        df = pd.read_csv("data/topography/mountain.csv".format(n))
        return get_topography_chart(df, int(distance))
    elif n == "Flat":
        df = pd.read_csv("data/topography/flat.csv".format(n))
        return get_topography_chart(df, int(distance))
    else:
        return no_update


@callback(
    Output("attenuation-chart-container", "children"),
    Output("global-chart-container", "children"),
    Input("models-select", "value"),
    Input("topography-select", "value"),
    Input("flow-resistivity-select", "value"),
    Input("distance-select", "value"),
    Input("wind-speed-select", "value"),
    Input("wind-direction-select", "value"),
    Input("source-select", "data")
)
def update_attenuation_chart(models, topography, flow_resistivity, distance, wind_speed, wind_direction, source):
    if topography == "Mountain":
        df = pd.read_csv("data/results/mountain_results.csv")
        if models:
            excess_attenuation = get_attenuation_chart(
                df,
                models,
                flow_resistivity,
                distance,
                wind_speed,
                wind_direction)
            global_spl = get_global_spl(df, models, flow_resistivity, distance, wind_speed, wind_direction, source[0])
            return excess_attenuation, global_spl
        else:
            return dmc.Alert('No model selected'), dmc.Alert('No model selected')
    elif topography == "Mountain 2":
        df = pd.read_csv("data/results/mountain_results_2.csv")
        if models:
            excess_attenuation = get_attenuation_chart(
                df,
                models,
                flow_resistivity,
                distance,
                wind_speed,
                wind_direction)
            global_spl = get_global_spl(df, models, flow_resistivity, distance, wind_speed, wind_direction, source[0])
            return excess_attenuation, global_spl
        else:
            return dmc.Alert('No model selected'), dmc.Alert('No model selected')

    elif topography == "Flat":
        df = pd.read_csv("data/results/flat_results.csv")
        if models:
            excess_attenuation = get_attenuation_chart(
                df,
                models,
                flow_resistivity,
                distance,
                wind_speed,
                wind_direction
            )
            global_spl = get_global_spl(df, models, flow_resistivity, distance, wind_speed, wind_direction, source[0])
            return excess_attenuation, global_spl
        else :
            return dmc.Alert('No model selected'), dmc.Alert('No model selected')
    else:
        return no_update, no_update


@callback(Output("wind-turbine-card", "children"),
          Input("source-select", "data"))
def update_wind_turbine(source):
    if source:
        df = pd.read_csv(f"data/sources/sources_spectrum_{source[0]}.csv")
        source_spectrum = dict(zip(df["Frequency"], df["SPL"]))
        return get_source_spectrum_chart(source_spectrum)
    else:
        return no_update
