import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

home = dbc.Container(
    [
       html.Br(),
       dbc.Container(
           [
           html.H1(style={'color': '#c7c7c7', 'font-weight': '900', 'font-size': '100px', 'letter-spacing': '2px'}, className="display-3", children=[
            "Crimes Against Women Dashboard",
        ]),
           html.P(style={'color': '#03a9f4'}, className="lead", children=[
                "A dasboard for Interactive and Exploratory visualizations about Crimes Against Women in India. ",]
           ),
           html.Hr(className="my-2"),
           html.P(style={'color': '#03a9f4'}, children=[
               "Made By Ipsita Goel."
           ]),
         
        ])
],style={'height':'100%'})