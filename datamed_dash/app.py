import dash
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        __file__.replace("index.py", "./assets/style.css"),
    ],
    suppress_callback_exceptions=True,
    title="Dashboard - DataMed",
)
server = app.server
