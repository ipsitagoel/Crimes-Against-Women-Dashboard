from includes.about import about
from includes.navbar import navbar
from includes.home import home
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import dash_table
import io
import base64
import datetime
import plotly.express as px
import xlrd
import seaborn as sns
import matplotlib.pyplot as plt


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.BOOTSTRAP, external_stylesheets])
app.config['suppress_callback_exceptions'] = True
app.title = 'Crimes Against Women'
server=app.server
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

colors = {
    'background': '#131419',
    'text': '#7FDBFF'
}

# ========================== Data Processing ===============================================
df = pd.read_excel('Data/crime2014.xlsx')
tf = df
# print(df.head())
cols = df.columns

display_data = df.drop(columns='Total Crimes Against Women')
year_data = display_data.groupby("Year").sum().reset_index()
classy = year_data.melt(id_vars="Year", var_name="Cases")
nf = classy.pivot('Year', 'Cases', 'value')
sf = classy.pivot('Cases', 'Year', 'value')

# Year list:
year_options = []
for year in df['Year'].unique():
    year_options.append({'label': str(year), 'value': year})
state_options = []
for state in df['State/UT'].unique():
    state_options.append({'label': str(state), 'value': state})

minYear = df['Year'].min()
maxYear = df['Year'].max()
# Crime head dictionary-LIST:
# With Sum aggr:
crimeDictS = {'Rape': sum, 'Kidnapping & Abduction': sum, 'Dowry Deaths': sum, 'Assault on women with intent to outrage her modesty ': sum, 'Insult to modesty of women': sum, 'Cruelty by Husband or his Relatives': sum,
              'Importation of Girls from foreign country': sum, 'Immoral Traffic (P) Act': sum, 'Dowry Prohibition Act': sum, 'Indecent Representation of Women(P) Act': sum, 'Commission of Sati Prevention Act': sum}
# Without aggr list:
crimeDict = ['Rape', 'Kidnapping & Abduction', 'Dowry Deaths', 'Assault on women with intent to outrage her modesty ', 'Insult to modesty of women', 'Cruelty by Husband or his Relatives',
             'Importation of Girls from foreign country', 'Immoral Traffic (P) Act', 'Dowry Prohibition Act', 'Indecent Representation of Women(P) Act', 'Commission of Sati Prevention Act']
# crime list:
crimes = ['Rape', 'Kidnapping & Abduction', 'Dowry Deaths', 'Assault on women with intent to outrage her modesty ', 'Insult to modesty of women', 'Cruelty by Husband or his Relatives',
          'Importation of Girls from foreign country', 'Immoral Traffic (P) Act', 'Dowry Prohibition Act', 'Indecent Representation of Women(P) Act', 'Commission of Sati Prevention Act']

states = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya',
          'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'A & N Islands', 'Chandigarh', 'D&N Haveli', 'Daman & Diu', 'Delhi UT', 'Lakshadweep', 'Puducherry']

total_crimes = [16477, 180, 4243, 5356, 3989, 83, 5805, 3393, 890, 1656, 2229, 6002, 5450, 14549, 12524,
                112, 66, 126, 30, 5357, 2361, 12175, 24, 10111, 438, 20227, 749, 6570, 34, 150, 19, 10, 2291, 0, 119]

# New df: removing year:
totalc = df.groupby(["State/UT"], as_index=False).agg(crimeDictS)
totalc['Total'] = totalc[crimeDict].sum(axis=1)
print(totalc.columns)
# ==========================  plots =============================================
plottab1 = html.Div(children=[



    # Plot 1:
    html.Div(children=[
        html.H1(style={'textAlign': 'center', 'color': '#c7c7c7', 'font-weight': '900', 'font-size': '18px', 'letter-spacing': '2px'}, children=[
            "State-Wise Total Crimes Against Women In India",
        ]),
        html.P(style={'textAlign': 'center', 'color': '#03a9f4'}, children=[
               "("+str(minYear)+" - "+str(maxYear)+")"]),
        dcc.Graph(id='totalYear',
                  figure={
                      'data': [go.Bar(
                          x=totalc['State/UT'],
                          y=totalc['Total'],
                      )],
                      'layout':go.Layout(margin=dict(l=30, r=10, t=10, b=120), xaxis={'title': 'States/UT'}, paper_bgcolor=colors['background'], plot_bgcolor=colors['background'], height=250, width=650)
                  })
    ]),




])


plottab4 = html.Div(children=[

    # Plot 2:
    html.Div(style={'margin-left': 'auto', 'margin-right': 'auto'}, children=[
        html.H1(style={'textAlign': 'center', 'color': '#c7c7c7', 'font-weight': '900', 'font-size': '18px', 'letter-spacing': '2px'}, children=[
            "Year-Wise Sub-Crimes Against Women In India",
        ]),
        dcc.Graph(id='treemap',
                  figure=px.treemap(classy,
                                    path=["Year", "Cases"], values="value",
                                    height=500, width=800).update_layout(margin=dict(t=10, r=0, l=5, b=20), paper_bgcolor=colors['background'], plot_bgcolor=colors['background'])
                  )
    ]),


])

plottab7 = html.Div(children=[

    # Plot 7:
    html.Div(style={'margin-left': 'auto', 'margin-right': 'auto'}, children=[
        html.H1(style={'textAlign': 'center', 'color': '#c7c7c7', 'font-weight': '900', 'font-size': '18px', 'letter-spacing': '2px'}, children=[
            "Year-Wise Sub-Crimes Against Women In India",
        ]),
        dcc.Graph(id='the_heat', figure=px.imshow(nf,
                                                  color_continuous_scale=px.colors.sequential.Plasma, width=520, height=500
                                                  ).update_layout(margin=dict(t=5, r=0, l=5, b=5), paper_bgcolor=colors['background'], plot_bgcolor=colors['background'])
                  )
    ]),


])


plottab8 = html.Div(children=[

    # Plot 8:
    html.Div(style={'margin-left': 'auto', 'margin-right': 'auto'}, children=[
        html.H1(style={'textAlign': 'center', 'color': '#c7c7c7', 'font-weight': '900', 'font-size': '18px', 'letter-spacing': '2px'}, children=[
            "State-Wise Total Crimes Against Women In India",
        ]),

        # html.Div([
        #          html.Label("Select State: "),
        #          dcc.Dropdown(id='statez', options=state_options, style={'width': '500px', 'background': '#131419', 'box-shadow': 'inset -2px -2px 6px rgba(255, 255, 255, 0.1), inset 2px 2px 6px rgba(0, 0, 0, 0.8)', 'border': '0', 'color': '#03a9f4', 'font-weight': '500', 'border-radius': '40px', 'margin-bottom': '15px'},
        #                       value='Andhra Pradesh'),
        #          ]),

        dcc.Graph(id='the_pie', figure=px.pie(df,
                                              names=states, values=total_crimes,
                                              ).update_layout(margin=dict(t=10, r=0, l=5, b=20), paper_bgcolor=colors['background'], plot_bgcolor=colors['background'], height=290, width=650)
                  )
    ]),


])

plottab6 = html.Div(children=[

    # Plot 6:
    html.Div(children=[
        html.H1('Crimes Against Women In States Per Year',
                style={'textAlign': 'center', 'color': '#c7c7c7', 'font-weight': '900', 'font-size': '18px', 'letter-spacing': '2px'}),
        html.Div(className='row', children=[
            html.Div(className='col', children=[html.Label('Select Year:', style={
                'margin-left': 'auto', 'margin-right': 'auto', 'color': '#03a9f4', 'font-weight': '500'}), ]),
            html.Div(className='col', children=[dcc.Dropdown(id='year-picker', options=year_options,
                                                             value=df['Year'].min(), style={'margin-left': 'auto', 'margin-right': 'auto', 'width': '220px', 'background': '#131419', 'box-shadow': 'inset -2px -2px 6px rgba(255, 255, 255, 0.1), inset 2px 2px 6px rgba(0, 0, 0, 0.8)', 'border': '0', 'color': '#03a9f4', 'font-weight': '500', 'border-radius': '40px', 'margin-bottom': '15px'}),
                                                ]), ]),
        html.Div(children=[
            dcc.Graph(id='the_graph',
                      ),
        ]),
    ]),



])


plottab10 = html.Div(children=[

    # Plot 10:
    html.Div(children=[
        html.H1('Crimes Against Women In A Year Per State',
                style={'textAlign': 'center', 'color': '#c7c7c7', 'font-weight': '900', 'font-size': '18px', 'letter-spacing': '2px'}),
        html.Div(className='row', children=[
            html.Div(className='col', children=[html.Label('Select Year:', style={
                'margin-left': 'auto', 'margin-right': 'auto', 'color': '#03a9f4', 'font-weight': '500'}), ]),
            html.Div(className='col', children=[dcc.Dropdown(id='the_statez', options=state_options, style={'width': '500px', 'background': '#131419', 'box-shadow': 'inset -2px -2px 6px rgba(255, 255, 255, 0.1), inset 2px 2px 6px rgba(0, 0, 0, 0.8)', 'border': '0', 'color': '#03a9f4', 'font-weight': '500', 'border-radius': '40px', 'margin-bottom': '15px'},
                                                             value='Andhra Pradesh'),
                                                ]), ]),
        html.Div(children=[
            dcc.Graph(id='the_line',
                      ),
        ]),
    ]),



])


# plottab11 = html.Div(children=[


#     # Plot 11:
#     html.Div(children=[
#         html.H1(style={'textAlign': 'center', 'color': '#c7c7c7', 'font-weight': '900', 'font-size': '18px', 'letter-spacing': '2px'}, children=[
#             "State-Wise Total Crimes Against Women In India",
#         ]),
#         html.P(style={'textAlign': 'center', 'color': '#03a9f4'}, children=[
#                "("+str(minYear)+" - "+str(maxYear)+")"]),
#         dcc.Graph(id='the_box',
#                   figure={
#                       'data': [go.Box(
#                           x=df['State/UT'],
#                           y=df['Total Crimes Against Women'],
#                       )],
#                       'layout':go.Layout(margin=dict(l=30, r=10, t=10, b=120), xaxis={'title': 'States/UT'}, paper_bgcolor=colors['background'], plot_bgcolor=colors['background'], height=250, width=650)
#                   })
#     ]),


# ])

plottab11 = html.Div(children=[

    # Plot 11:
    html.Div(children=[
        html.H1('Crimes Against Women In States Per Year',
                style={'textAlign': 'center', 'color': '#c7c7c7', 'font-weight': '900', 'font-size': '18px', 'letter-spacing': '2px'}),
#        html.Div(className='row', children=[
#            html.Div(className='col', children=[html.Label('Select Year:', style={
#                'margin-left': 'auto', 'margin-right': 'auto', 'color': '#03a9f4', 'font-weight': '500'}), ]),
#            html.Div(className='col', children=[dcc.Dropdown(id='the_year-picker', options=year_options,
#                                                             value=df['Year'].min(), style={'margin-left': 'auto', 'margin-right': 'auto', 'width': '220px', 'background': '#131419', 'box-shadow': 'inset -2px -2px 6px rgba(255, 255, 255, 0.1), inset 2px 2px 6px rgba(0, 0, 0, 0.8)', 'border': '0', 'color': '#03a9f4', 'font-weight': '500', 'border-radius': '40px', 'margin-bottom': '15px'}),
#                                                ]), ]),
        html.Div(children=[
            dcc.Graph(id='the_box',
                      figure={
                          'data': [go.Box(
                           x=df['State/UT'],
                           y=df['Total Crimes Against Women'],
                       )],
                       'layout':go.Layout(margin=dict(l=30, r=10, t=10, b=120), xaxis={'title': 'States/UT'}, paper_bgcolor=colors['background'], plot_bgcolor=colors['background'], height=290, width=650)
                      }),
        ]),
    ]),



])


# plottab9 = html.Div(children=[

#     # Plot 9:
#     html.Div(children=[
#         html.H1('Crimes Against Women In States Per Year',
#                 style={'textAlign': 'center', 'color': '#c7c7c7', 'font-weight': '900', 'font-size': '18px', 'letter-spacing': '2px'}),
#         html.Div(className='row', children=[
#             html.Div(className='col', children=[html.Label('Select Year:', style={
#                 'margin-left': 'auto', 'margin-right': 'auto', 'color': '#03a9f4', 'font-weight': '500'}), ]),
#             html.Div(className='col', children=[dcc.Dropdown(id='year-picker', options=year_options,
#                                                              value=df['Year'].min(), style={'margin-left': 'auto', 'margin-right': 'auto', 'width': '220px', 'background': '#131419', 'box-shadow': 'inset -2px -2px 6px rgba(255, 255, 255, 0.1), inset 2px 2px 6px rgba(0, 0, 0, 0.8)', 'border': '0', 'color': '#03a9f4', 'font-weight': '500', 'border-radius': '40px', 'margin-bottom': '15px'}),
#                                                 ]), ]),
#         html.Div(children=[
#             dcc.Graph(id='the_scatter',
#                       ),
#         ]),
#     ]),


# ])


plottab5 = html.Div(children=[

    # Plot 3:
    html.Div(children=[
        html.H1('Crimes Against Women In A Year Per State',
                style={'textAlign': 'center', 'color': '#c7c7c7', 'font-weight': '900', 'font-size': '18px', 'letter-spacing': '2px'}),
        html.Div(className='row', children=[
            html.Div(className='col', children=[html.Label('Select Year:', style={
                'margin-left': 'auto', 'margin-right': 'auto', 'color': '#03a9f4', 'font-weight': '500'}), ]),
            html.Div(className='col', children=[dcc.Dropdown(id='statez1', options=state_options, style={'width': '500px', 'background': '#131419', 'box-shadow': 'inset -2px -2px 6px rgba(255, 255, 255, 0.1), inset 2px 2px 6px rgba(0, 0, 0, 0.8)', 'border': '0', 'color': '#03a9f4', 'font-weight': '500', 'border-radius': '40px', 'margin-bottom': '15px'},
                                                             value='Andhra Pradesh'),
                                                ]), ]),
        html.Div(children=[
            dcc.Graph(id='perYear',
                      figure={
                          'layout': {'paper_bgcolor': '#131419', 'plot_bgcolor': '#131419'}
                      }),
        ]),
    ]),



])


plottab2 = html.Div([
    html.Div(className='row', children=[

        # Figure 2.1
        html.H1(style={'text-align': 'center', 'margin-left': 'auto', 'margin-right': 'auto', 'color': '#c7c7c7', 'font-weight': '900', 'font-size': '18px', 'letter-spacing': '2px'}, children=[
                "States & Sub-Crimes Interactive",
                ]),
        html.Div([
            html.Label('Select State/UT:'),
            dcc.Dropdown(id='selectState', style={'width': '500px', 'background': '#131419', 'box-shadow': 'inset -2px -2px 6px rgba(255, 255, 255, 0.1), inset 2px 2px 6px rgba(0, 0, 0, 0.8)', 'border': '0', 'color': '#03a9f4', 'font-weight': '500', 'border-radius': '40px', 'margin-bottom': '15px'}, options=state_options,
                         value=df['State/UT'][0])
        ]),
        html.Div([
            html.Label('Select Sub-Crime:'),
            dcc.Dropdown(id='selectCrime', style={'width': '500px', 'background': '#131419', 'box-shadow': 'inset -2px -2px 6px rgba(255, 255, 255, 0.1), inset 2px 2px 6px rgba(0, 0, 0, 0.8)', 'border': '0', 'color': '#03a9f4', 'font-weight': '500', 'border-radius': '40px', 'margin-bottom': '15px'}, options=[
                {'label': i, 'value': i} for i in crimes], value='Rape')
        ]),
        # Figure 2.2
    ]),
    html.Div(className="row", children=[
        html.H2(style={'color': '#03a9f4', 'font-weight': '900', 'font-size': '1rem',
                       'font-style': 'italic', 'font-family': 'sans-serif'}, children=["FORECAST:"]),
        dcc.Markdown(id='forecast'),

    ]),
    html.Div(className="row", children=[
        dcc.Graph(id="stateCrime",
                  figure={
                      'layout': {'paper_bgcolor': '#131419', 'plot_bgcolor': '#131419', 'height': 420, 'width': 580}
                  }),

    ]),
], style={'padding-left': 15})


plottab12 = html.Div([
    html.Div(className='row', children=[

        # Figure 12.1
        html.H1(style={'text-align': 'center', 'margin-left': 'auto', 'margin-right': 'auto', 'color': '#c7c7c7', 'font-weight': '900', 'font-size': '18px', 'letter-spacing': '2px'}, children=[
                "States & Sub-Crimes Interactive",
                ]),
        html.Div([
            html.Label('Select State/UT:'),
            dcc.Dropdown(id='selectState1', style={'width': '500px', 'background': '#131419', 'box-shadow': 'inset -2px -2px 6px rgba(255, 255, 255, 0.1), inset 2px 2px 6px rgba(0, 0, 0, 0.8)', 'border': '0', 'color': '#03a9f4', 'font-weight': '500', 'border-radius': '40px', 'margin-bottom': '15px'}, options=state_options,
                         value=df['State/UT'][0])
        ]),
        html.Div([
            html.Label('Select Sub-Crime:'),
            dcc.Dropdown(id='selectCrime1', style={'width': '500px', 'background': '#131419', 'box-shadow': 'inset -2px -2px 6px rgba(255, 255, 255, 0.1), inset 2px 2px 6px rgba(0, 0, 0, 0.8)', 'border': '0', 'color': '#03a9f4', 'font-weight': '500', 'border-radius': '40px', 'margin-bottom': '15px'}, options=[
                {'label': i, 'value': i} for i in crimes], value='Rape')
        ]),
        # Figure 2.2
    ]),
    html.Div(className="row", children=[
        html.H2(style={'color': '#03a9f4', 'font-weight': '900', 'font-size': '1rem',
                       'font-style': 'italic', 'font-family': 'sans-serif'}, children=["FORECAST:"]),
        dcc.Markdown(id='the_forecast'),

    ]),
    html.Div(className="row", children=[
        dcc.Graph(id="the_stateCrime",
                  figure={
                      'layout': {'paper_bgcolor': '#131419', 'plot_bgcolor': '#131419', 'height': 420, 'width': 580}
                  }),

    ]),
], style={'padding-left': 15})

plottab3 = html.Div([
    html.Div(className="row", children=[
             html.H1(style={'text-align': 'center', 'margin-left': 'auto', 'margin-right': 'auto', 'color': '#c7c7c7', 'font-weight': '900', 'font-size': '18px', 'letter-spacing': '2px'}, children=[
                 "Crimes Correlation Interactive",
             ]),
             html.Div([
                 html.Label("Select State: "),
                 dcc.Dropdown(id='statez', options=state_options, style={'width': '500px', 'background': '#131419', 'box-shadow': 'inset -2px -2px 6px rgba(255, 255, 255, 0.1), inset 2px 2px 6px rgba(0, 0, 0, 0.8)', 'border': '0', 'color': '#03a9f4', 'font-weight': '500', 'border-radius': '40px', 'margin-bottom': '15px'},
                              value='Andhra Pradesh'),
             ]),
             ]),

    html.Div(className='row', children=[
        html.Div(className='col', children=[html.Label("Select Crime 1: "),
                                            dcc.Dropdown(id='crimex', options=[
                                                {'label': i, 'value': i} for i in crimeDict], value='Rape', style={'width': '220px', 'background': '#131419', 'box-shadow': 'inset -2px -2px 6px rgba(255, 255, 255, 0.1), inset 2px 2px 6px rgba(0, 0, 0, 0.8)', 'border': '0', 'color': '#03a9f4', 'font-weight': '500', 'border-radius': '40px', 'margin-bottom': '15px'}), ]),
        html.Div(className='col', children=[html.Label("Select Crime 2: "),
                                            dcc.Dropdown(id='crimey', options=[
                                                {'label': i, 'value': i} for i in crimeDict], value='Dowry Deaths', style={'width': '220px', 'background': '#131419', 'box-shadow': 'inset -2px -2px 6px rgba(255, 255, 255, 0.1), inset 2px 2px 6px rgba(0, 0, 0, 0.8)', 'border': '0', 'color': '#03a9f4', 'font-weight': '500', 'border-radius': '40px', 'margin-bottom': '15px'}), ]),
    ]),

    html.Div(className="row", children=[
        html.P(id='corrRes1', children=[
            "Correlation value: ",
            html.B(id='corrRes'),
            html.Br(),
            "Correlation degree: ",
            html.B(id='corrType'),
        ], style={'width': '100%', 'display': 'inline-block'}),

        html.Div(
            dcc.Graph(id='corr-graphic',
                      figure={
                          'layout': {'paper_bgcolor': '#131419', 'plot_bgcolor': '#131419', 'height': 420, 'width': 600}
                      })
        ),
    ]),





], style={'padding-left': 10})


plottab13 = html.Div([
    html.Div(className="row", children=[
             html.H1(style={'text-align': 'center', 'margin-left': 'auto', 'margin-right': 'auto', 'color': '#c7c7c7', 'font-weight': '900', 'font-size': '18px', 'letter-spacing': '2px'}, children=[
                 "Crimes Correlation Interactive",
             ]),
             html.Div([
                 html.Label("Select State: "),
                 dcc.Dropdown(id='stateza', options=state_options, style={'width': '500px', 'background': '#131419', 'box-shadow': 'inset -2px -2px 6px rgba(255, 255, 255, 0.1), inset 2px 2px 6px rgba(0, 0, 0, 0.8)', 'border': '0', 'color': '#03a9f4', 'font-weight': '500', 'border-radius': '40px', 'margin-bottom': '15px'},
                              value='Andhra Pradesh'),
             ]),
             ]),

    html.Div(className='row', children=[
        html.Div(className='col', children=[html.Label("Select Crime 1: "),
                                            dcc.Dropdown(id='crimexa', options=[
                                                {'label': i, 'value': i} for i in crimeDict], value='Rape', style={'width': '220px', 'background': '#131419', 'box-shadow': 'inset -2px -2px 6px rgba(255, 255, 255, 0.1), inset 2px 2px 6px rgba(0, 0, 0, 0.8)', 'border': '0', 'color': '#03a9f4', 'font-weight': '500', 'border-radius': '40px', 'margin-bottom': '15px'}), ]),
        html.Div(className='col', children=[html.Label("Select Crime 2: "),
                                            dcc.Dropdown(id='crimeya', options=[
                                                {'label': i, 'value': i} for i in crimeDict], value='Dowry Deaths', style={'width': '220px', 'background': '#131419', 'box-shadow': 'inset -2px -2px 6px rgba(255, 255, 255, 0.1), inset 2px 2px 6px rgba(0, 0, 0, 0.8)', 'border': '0', 'color': '#03a9f4', 'font-weight': '500', 'border-radius': '40px', 'margin-bottom': '15px'}), ]),
    ]),

    html.Div(className="row", children=[
        html.P(id='the_corrRes', children=[
            "Correlation value: ",
            html.B(id='the_corrRes1'),
            html.Br(),
            "Correlation degree: ",
            html.B(id='the_corrType'),
        ], style={'width': '100%', 'display': 'inline-block'}),

        html.Div(
            dcc.Graph(id='the_corr-graphic',
                      figure={
                          'layout': {'paper_bgcolor': '#131419', 'plot_bgcolor': '#131419', 'height': 420, 'width': 600}
                      })
        ),
    ]),





], style={'padding-left': 10})

plottab14 = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'color': '#03a9f4',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
])


# ========================== Routes: ============================================
# Nav bar:
navbar = navbar
# home:
home = home
# about
about = about

# ========================== TABS ===============================================


caw1 = dbc.Row(
    [dbc.Col(dbc.Card(
        [
            plottab1,
        ],
        body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '100%'}
    ), width="auto"), dbc.Col(dbc.Card(
        [
            plottab8,
        ],
        body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '100%'}
    ), width="auto")]
)

# caw1 = dbc.Card(
#     [
#         plottab1,
#     ],
#     body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '42%'}
# )

# caw5 = dbc.Card(
#     [
#         plottab5,
#     ],
#     body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '42%'}
# )

caw4 = dbc.Row(
    [dbc.Col(dbc.Card(
        [
            plottab4,
        ],
        body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '100%'}
    ), ), dbc.Col(dbc.Card(
        [
            plottab7,
        ],
        body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '100%'}
    ), )]
)

# caw4 = dbc.Card(
#     [
#         plottab4, plottab7
#     ],
#     body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '100%'}
# )

# caw4 = dbc.Card(
#     [
#         plottab4,
#     ],
#     body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '65%'}
# )

# caw7 = dbc.Card(
#     [
#         plottab7,
#     ],
#     body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '35%'}
# )

# caw8 = dbc.Card(
#     [
#         plottab8,
#     ],
#     body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '65%'}
# )

caw6 = dbc.Row(
    [dbc.Col(dbc.Card(
        [
            plottab6,
        ],
        body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '100%'}
    ), width="auto"), dbc.Col(dbc.Card(
        [
            plottab11,
        ],
        body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '100%'}
    ), width="auto")]
)

# caw6 = dbc.Card(
#     [
#         plottab6,
#     ],
#     body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '65%'}
# )
caw10 = dbc.Row(
    [dbc.Col(dbc.Card(
        [
            plottab10,
        ],
        body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '100%'}
    ), width="auto"), dbc.Col(dbc.Card(
        [
            plottab5,
        ],
        body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '100%'}
    ), width="auto")]
)

# caw10 = dbc.Card(
#     [
#         plottab10,
#     ],
#     body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '65%'}
# )

# caw11 = dbc.Card(
#     [
#         plottab5,
#     ],
#     body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '65%'}
# )
# caw9 = dbc.Card(
#     [
#         plottab9,
#     ],
#     body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '65%'}
# )

caw2 = dbc.Row(
    [dbc.Col(dbc.Card(
        [
            plottab2,
        ],
        body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '50%'}
    ), width="auto"), dbc.Col(dbc.Card(
        [
            plottab12,
        ],
        body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '50%'}
    ), width="auto")]
)

# caw2 = dbc.Card(
#     [
#         plottab2,
#     ],
#     body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '45%'}
# )

# caw12 = dbc.Card(
#     [
#         plottab12,
#     ],
#     body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '45%'}
# )

caw3 = dbc.Row(
    [dbc.Col(dbc.Card(
        [
            plottab3,
        ],
        body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '90%'}
    ), width="auto"), dbc.Col(dbc.Card(
        [
            plottab13,
        ],
        body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '90%'}
    ), width="auto")]
)

# caw3 = dbc.Card(
#     [
#         plottab3,
#     ],
#     body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '45%'}
# )

# caw13 = dbc.Card(
#     [
#         plottab13,
#     ],
#     body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '45%'}
# )

caw14 = dbc.Card(
    [
        plottab14,
    ],
    body=True,  style={"box-shadow": "-5px -5px 10px rgba(255, 255, 255, 0.05), 5px 5px 15px rgba(0, 0, 0, 0.8)", "background-color": "#131419", 'margin-bottom': '20px', 'border-radius': '10px', 'width': '45%'}
)

# ========================= page layout =========================================
app.layout = html.Div(
    [
        dcc.Location(id="url", pathname="/home"),
        navbar,
        html.Div(className="container-fluid",
                 id="content", style={"padding": "40px"}
                 ),


    ], style={'backgroundColor': colors['background']},
)

# ====================== Plotngs ============================================

# TAB 1 : STARTS


@ app.callback(Output(component_id='perYear', component_property='figure'),
               [Input(component_id='statez1', component_property='value')])
def update_figure(state_options):
    filtered_mf = df[df['State/UT'] == state_options]
    tracesm = [go.Bar(
        x=filtered_mf['Year'],
        y=filtered_mf['Total Crimes Against Women']
    )]
    return {
        'data': tracesm,
        'layout': go.Layout(margin=dict(l=40, r=10, t=0, b=35), title='Total crime in  '+str(state_options), xaxis={'title': 'States/UT'}, paper_bgcolor=colors['background'], plot_bgcolor=colors['background'], height=240, width=620)
    }
# TAB 1 ENDS


# @ app.callback(Output(component_id='the_pie', component_property='figure'),
#                [Input(component_id='statez', component_property='value')])
# def update_graph(statez):
#     filtered_df = classy[classy['State/UT'] == statez]
#     piechart = px.pie(data_frame=filtered_df,
#                       names=crimes, hole=.3,

#                       )
#     return {
#         'data': piechart,
#         'layout': px.Layout(margin=dict(l=30, r=10, t=25, b=100), paper_bgcolor=colors['background'], plot_bgcolor=colors['background'], height=240, width=240)
#     }


@ app.callback(Output(component_id='the_graph', component_property='figure'),
               [Input(component_id='year-picker', component_property='value')])
def update_figure(selected_year):
    filtered_xf = df[df['Year'] == selected_year]

    trace = [go.Scatter(
        x=filtered_xf['State/UT'],
        y=filtered_xf['Total Crimes Against Women']
    )]
    return {
        'data': trace,
        'layout': go.Layout(margin=dict(l=30, r=10, t=0, b=100), title='Total crime in the year '+str(selected_year), xaxis={'title': 'States/UT'}, paper_bgcolor=colors['background'], plot_bgcolor=colors['background'], height=240, width=650)
    }


@ app.callback(Output(component_id='the_line', component_property='figure'),
               [Input(component_id='the_statez', component_property='value')])
def update_figure(state_options):
    filtered_lf = df[df['State/UT'] == state_options]

    line = [go.Scatter(
        x=filtered_lf['Year'],
        y=filtered_lf['Total Crimes Against Women']
    )]
    return {
        'data': line,
        'layout': go.Layout(margin=dict(l=30, r=10, t=0, b=35), xaxis={'title': 'States/UT'}, paper_bgcolor=colors['background'], plot_bgcolor=colors['background'], height=240, width=650)
    }


#@ app.callback(Output(component_id='the_box', component_property='figure'),
#               [Input(component_id='the_year-picker', component_property='value')])
#def update_figure(selected_year):
#    filtered_sf = df[df['Year'] == selected_year]

#    box = [go.Box(
#        x=df['State/UT'],
#        y=df['Total Crimes Against Women'],
#    )]
#    # return box
#    return {
#        'data': box,
#        'layout': go.Layout(margin=dict(l=30, r=10, t=0, b=100), xaxis={'title': 'States/UT'}, paper_bgcolor=colors['background'], plot_bgcolor=colors['background'], height=240, width=650)
#    }


# @ app.callback(Output(component_id='the_scatter', component_property='figure'),
#                [Input(component_id='year-picker', component_property='value')])
# def update_figure(selected_year):
#     filter_df = df[df['Year'] == selected_year]

#     trace_scatter = [px.scatter(
#         x=filter_df['State/UT'],
#         y=filter_df['Total Crimes Against Women'],
#         color=filter_df['Year'],
#     )]
#     return {
#         'data': trace_scatter,
#     }


# TAB 2 : STARTS


@ app.callback(Output('stateCrime', 'figure'),
               [Input('selectState', 'value'),
                Input('selectCrime', 'value')])
def state_crime_graph(sstate, scrime):
    filter_state = df[df['State/UT'] == sstate]
    traces = [go.Scatter(
        x=filter_state['Year'],
        y=filter_state[scrime],
        name=scrime,
        fill='tonexty',
        mode='lines'
    )]
    return {
        'data': traces,
        'layout': go.Layout(title='{} cases in {}'.format(scrime, sstate),
                            xaxis={'title': 'Year'},
                            yaxis={'title': 'cases of '+scrime},
                            hovermode='closest', paper_bgcolor=colors['background'], plot_bgcolor=colors['background'])
    }

# Forecast:


def pattern(a, b, c):
    if(a == 1):
        if(b == 1):
            if(c == 1):
                return "Higher chances of an increase"
            else:
                return "Medium chances of an decrease"
        elif(b == 0):
            if(c == 1):
                return "Medium chances of an increase"
            else:
                return "High chances of an decrease"
    elif(a == 0):
        if(b == 0):
            if(c == 0):
                return "Higher chances of decrease"
            else:
                return "Lower chances of increase"
        elif(b == 1):
            if(c == 0):
                return "Lower chances of decrease"
            else:
                return "Higher chances of increase"


@ app.callback(Output('forecast', 'children'),
               [Input('selectState', 'value'),
                Input('selectCrime', 'value')])
def forecast_update(sstate, scrime):
    y1 = df['Year'].max()
    y2 = y1-1
    y3 = y2-1
    y4 = y3-1
    x1 = list(df[(df['State/UT'] == sstate) & (df['Year'] == y1)][scrime])
    x2 = list(df[(df['State/UT'] == sstate) & (df['Year'] == y2)][scrime])
    x3 = list(df[(df['State/UT'] == sstate) & (df['Year'] == y3)][scrime])
    x4 = list(df[(df['State/UT'] == sstate) & (df['Year'] == y4)][scrime])
    if((sstate == 'Telangana') & (y1 == 2015)):
        s1 = 0
        s2 = 0
        if((x1[0] - x2[0]) > 0):
            s3 = 1
        else:
            s3 = 0
    else:
        if((x3[0] - x4[0]) > 0):
            s1 = 1
        else:
            s1 = 0
        if((x2[0] - x3[0]) > 0):
            s2 = 1
        else:
            s2 = 0
        if((x1[0] - x2[0]) > 0):
            s3 = 1
        else:
            s3 = 0
    res = pattern(s1, s2, s3)
    cast = "> {} has {} in {} in the year {} ,considering constant current policies.".format(
        sstate, res, scrime, str(y1+1))
    return cast


################
@ app.callback(Output('the_stateCrime', 'figure'),
               [Input('selectState1', 'value'),
                Input('selectCrime1', 'value')])
def state_crime_graph(sstate1, scrime1):
    filter_sstate1 = df[df['State/UT'] == sstate1]
    traces11 = [go.Scatter(
        x=filter_sstate1['Year'],
        y=filter_sstate1[scrime1],
        name=scrime1,
        mode='markers',
        marker=dict(symbol='square')
    )]
    return {
        'data': traces11,
        'layout': go.Layout(title='{} cases in {}'.format(scrime1, sstate1),
                            xaxis={'title': 'Year'},
                            yaxis={'title': 'cases of '+scrime1},
                            hovermode='closest', paper_bgcolor=colors['background'], plot_bgcolor=colors['background'])
    }

# Forecast:


def pattern(a1, b1, c1):
    if(a1 == 1):
        if(b1 == 1):
            if(c1 == 1):
                return "Higher chances of an increase"
            else:
                return "Medium chances of an decrease"
        elif(b1 == 0):
            if(c1 == 1):
                return "Medium chances of an increase"
            else:
                return "High chances of an decrease"
    elif(a1 == 0):
        if(b1 == 0):
            if(c1 == 0):
                return "Higher chances of decrease"
            else:
                return "Lower chances of increase"
        elif(b1 == 1):
            if(c1 == 0):
                return "Lower chances of decrease"
            else:
                return "Higher chances of increase"


@ app.callback(Output('the_forecast', 'children'),
               [Input('selectState1', 'value'),
                Input('selectCrime1', 'value')])
def forecast_update(sstate1, scrime1):
    y1a = df['Year'].max()
    y2a = y1a-1
    y3a = y2a-1
    y4a = y3a-1
    x1a = list(df[(df['State/UT'] == sstate1) & (df['Year'] == y1a)][scrime1])
    x2a = list(df[(df['State/UT'] == sstate1) & (df['Year'] == y2a)][scrime1])
    x3a = list(df[(df['State/UT'] == sstate1) & (df['Year'] == y3a)][scrime1])
    x4a = list(df[(df['State/UT'] == sstate1) & (df['Year'] == y4a)][scrime1])
    if((sstate1 == 'Telangana') & (y1a == 2015)):
        s1a = 0
        s2a = 0
        if((x1a[0] - x2a[0]) > 0):
            s3a = 1
        else:
            s3a = 0
    else:
        if((x3a[0] - x4a[0]) > 0):
            s1a = 1
        else:
            s1a = 0
        if((x2a[0] - x3a[0]) > 0):
            s2a = 1
        else:
            s2a = 0
        if((x1a[0] - x2a[0]) > 0):
            s3a = 1
        else:
            s3a = 0
    res1 = pattern(s1a, s2a, s3a)
    cast1 = "> {} has {} in {} in the year {} ,considering constant current policies.".format(
        sstate1, res1, scrime1, str(y1a+1))
    return cast1

# TAB 2 ENDS
# TAB 3 STARTS


@ app.callback(Output('corr-graphic', 'figure'),
               [Input('crimex', 'value'),
                Input('crimey', 'value'),
                Input('statez', 'value')])
def update_graph(xaxis_name, yaxis_name, state_name):
    filter_tf = tf[tf['State/UT'] == state_name]
    total = filter_tf['Total Crimes Against Women'].sum()
    return {'data': [go.Scatter(x=filter_tf[xaxis_name],
                                y=filter_tf[yaxis_name],
                                text=filter_tf['Year'],
                                mode='markers',
                                marker=dict(size=(filter_tf['Total Crimes Against Women']/total)*1000,
                                            color=filter_tf['Total Crimes Against Women'], showscale=True)
                                )],
            'layout': go.Layout(title='Crime correlation in '+state_name,
                                xaxis={'title': xaxis_name},
                                yaxis={'title': yaxis_name},
                                hovermode='closest', paper_bgcolor=colors['background'], plot_bgcolor=colors['background'])
            }


@ app.callback(Output('corrRes', 'children'),
               [Input('crimex', 'value'),
                Input('crimey', 'value'),
                Input('statez', 'value')])
def corr_result(xvalue, yvalue, zvalue):
    filter_tf = tf[tf['State/UT'] == zvalue]
    Correlation = filter_tf[xvalue].corr(filter_tf[yvalue])
    strcorr = str(round(Correlation, 1))
    if(strcorr != 'nan'):
        r = strcorr
    else:
        r = '0'
    return r


def corr_check(corr):
    if(corr > 0.0):
        if(corr >= 0.5 and corr < 2.0):
            return 'Highly Positive'
        elif(corr >= 0.3 and corr < 0.5):
            return 'Moderately Positive'
        elif(corr < 0.3):
            return'Low positive'
    elif(corr == 0):
        return 'No correlation'
    else:
        return 'Negative'


@ app.callback(Output('corrType', 'children'),
               [Input('crimex', 'value'),
                Input('crimey', 'value'),
                Input('statez', 'value')])
def corr_type(xvalue, yvalue, zvalue):
    filter_tf = tf[tf['State/UT'] == zvalue]
    Correlation = filter_tf[xvalue].corr(filter_tf[yvalue])
    corri = round(Correlation, 1)
    strcorr = str(corri)
    if(strcorr == 'nan'):
        rtype = 'No correlation'
    else:
        rtype = corr_check(corri)
    return rtype


##############################################################
@ app.callback(Output('the_corr-graphic', 'figure'),
               [Input('crimexa', 'value'),
                Input('crimeya', 'value'),
                Input('stateza', 'value')])
def update_graph(xaxis_name1, yaxis_name1, state_name):
    filters_tf = tf[tf['State/UT'] == state_name]
    totals = filters_tf['Total Crimes Against Women'].sum()
    return {'data': [go.Scatter(x=filters_tf[xaxis_name1],
                                y=filters_tf[yaxis_name1],
                                text=filters_tf['Year'],
                                mode='markers',
                                marker=dict(symbol='cross',
                                            color=filters_tf['Total Crimes Against Women'], showscale=True)
                                )],
            'layout': go.Layout(title='Crime correlation in '+state_name,
                                xaxis={'title': xaxis_name1},
                                yaxis={'title': yaxis_name1},
                                hovermode='closest', paper_bgcolor=colors['background'], plot_bgcolor=colors['background'])
            }


@ app.callback(Output('the_corrRes1', 'children'),
               [Input('crimexa', 'value'),
                Input('crimeya', 'value'),
                Input('stateza', 'value')])
def corr_result(xvalue1, yvalue1, zvalue1):
    filters_tf = tf[tf['State/UT'] == zvalue1]
    Correlations = filters_tf[xvalue1].corr(filters_tf[yvalue1])
    strcorrs = str(round(Correlations, 1))
    if(strcorrs != 'nan'):
        ra = strcorrs
    else:
        ra = '0'
    return ra


def corr_check(corr1):
    if(corr1 > 0.0):
        if(corr1 >= 0.5 and corr1 < 2.0):
            return 'Highly Positive'
        elif(corr1 >= 0.3 and corr1 < 0.5):
            return 'Moderately Positive'
        elif(corr1 < 0.3):
            return'Low positive'
    elif(corr1 == 0):
        return 'No correlation'
    else:
        return 'Negative'


@ app.callback(Output('the_corrType', 'children'),
               [Input('crimexa', 'value'),
                Input('crimeya', 'value'),
                Input('stateza', 'value')])
def corr_type(xvalue1, yvalue1, zvalue1):
    filters_tf = tf[tf['State/UT'] == zvalue1]
    Correlations = filters_tf[xvalue1].corr(filters_tf[yvalue1])
    corris = round(Correlations, 1)
    strcorrs = str(corris)
    if(strcorrs == 'nan'):
        rtypea = 'No correlation'
    else:
        rtypea = corr_check(corris)
    return rtypea

# TAB 3 ENDS
# TAB 4 STARTS:


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            newdf = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            updatedf = df.append(newdf)
            updatedf.to_excel('Data/crime2014.xlsx', index=False)

        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            newdf = pd.read_excel(io.BytesIO(decoded))
            updatedf = df.append(newdf)
            updatedf.to_excel('Data/crime2014.xlsx', index=False)

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        html.H4("Dataframe added!"),
        # dash_table.DataTable(
        #     data=updatedf.to_dict('rows'),
        #     columns=[{'name': i, 'id': i} for i in updatedf.columns]
        # ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


@ app.callback(Output('output-data-upload', 'children'),
               [Input('upload-data', 'contents')],
               [State('upload-data', 'filename'),
                State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


# TAB 4 ENDS:
# ========================== Route Controller ==================================
@ app.callback(Output("content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/home":
        return home
    if pathname == "/about":
        return about
    if pathname == "/caw":
        return caw1, caw4, caw6, caw10, caw2, caw3
    # if not recognised, return 404 message
    return html.P("Adding Soon")
# ========================== Server =============================================


if __name__ == "__main__":
    app.run_server(debug=True)
