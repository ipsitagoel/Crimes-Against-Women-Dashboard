import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
navbar = dbc.NavbarSimple(
    children=[
        # dbc.NavItem(dbc.NavLink("About", href="/about")),
        dbc.NavItem(dbc.NavLink("Crime Insights", href="caw")),
    ],
    brand="Crimes Against Women",
    brand_href="home",
    color="#131419",
    dark=True,
    sticky="top",
)
