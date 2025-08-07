from dash import Dash, Input, Output, State, callback

@callback(
    Output("appshell", "navbar"),
    Input("mobile-burger", "opened"),
    Input("desktop-burger", "opened"),
    State("appshell", "navbar"),
)
def toggle_navbar(mobile_opened, desktop_opened, navbar):
    navbar["collapsed"] = {
        "mobile": not mobile_opened,
        "desktop": not desktop_opened,
    }
    return navbar


@callback(
    Output('url', 'pathname'),
    Input("nav-dashboard-btn", "n_clicks"),
    Input("nav-import-btn", "n_clicks"))
def navbar_routes(n_dashboard, n_import):
    if n_dashboard:
        return "/dashboard"
    elif n_import:
        return "/import"
