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
import geopandas as gpd
import matplotlib.pyplot as plt

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config['suppress_callback_exceptions'] = True
app.title = 'Crimes Against Women'
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"


# ========================== Data Processing ===============================================
df = pd.read_excel('Data/crime2014.xlsx')
tf = df
# print(df.head())
cols = df.columns

display_data = df.drop(columns='Total Crimes Against Women')
year_data = display_data.groupby("Year").sum().reset_index()
classy = year_data.melt(id_vars="Year", var_name="Cases")

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


# New df: removing year:
totalc = df.groupby(["State/UT"], as_index=False).agg(crimeDictS)
totalc['Total'] = totalc[crimeDict].sum(axis=1)
print(totalc.columns)



card_question = dbc.Card(
    [
        dbc.CardBody([
            html.H4("Question 1", className="card-title"),
            html.P("What was India's life expectancy in 1952?",
                   className="card-text"),
            dbc.ListGroup(
                [
                    dbc.ListGroupItem("A. 55 years"),
                    dbc.ListGroupItem("B. 37 years"),
                    dbc.ListGroupItem("C. 49 years"),
                ], flush=True)
        ]),
    ], color="warning",
)

card_graph = dbc.Card(
    dcc.Graph(id='treemap',
              figure=px.treemap(classy,
                                path=["Year", "Cases"], values="value",
                                height=600, width=1450).update_layout(margin=dict(t=25, r=0, l=5, b=20))), body=True, color="secondary",
)


app.layout = html.Div([
    dbc.Row([dbc.Col(card_question, width=1),
             dbc.Col(card_graph, width=10)], justify="around"),  # justify="start", "center", "end", "between", "around"

    # dbc.CardGroup([card_main, card_question, card_graph])   # attaches cards with equal width and height columns
    # dbc.CardDeck([card_main, card_question, card_graph])    # same as CardGroup but with gutter in between cards

    # dbc.CardColumns([                        # Cards organised into Masonry-like columns
    #         card_main,
    #         card_question,
    #         card_graph,
    #         card_question,
    #         card_question,
    # ])

])


@app.callback(Output(component_id='perYear', component_property='figure'),
              [Input(component_id='year-picker', component_property='value')])
def update_figure(selected_year):
    filtered_df = df[df['Year'] == selected_year]
    traces = [go.Bar(
        x=filtered_df['State/UT'],
        y=filtered_df['Total Crimes Against Women']
    )]
    return {
        'data': traces,
        'layout': go.Layout(title='Total crime in the year '+str(selected_year), xaxis={'title': 'States/UT'})
    }
# TAB 1 ENDS
# TAB 2 : STARTS


@app.callback(Output('stateCrime', 'figure'),
              [Input('selectState', 'value'),
               Input('selectCrime', 'value')])
def state_crime_graph(sstate, scrime):
    filter_state = df[df['State/UT'] == sstate]
    traces = [go.Scatter(
        x=filter_state['Year'],
        y=filter_state[scrime],
        name=scrime,
        fill='tonexty',
        mode='lines+markers'
    )]
    return {
        'data': traces,
        'layout': go.Layout(title='{} cases in {}'.format(scrime, sstate),
                            xaxis={'title': 'Year'},
                            yaxis={'title': 'cases of '+scrime},
                            hovermode='closest')
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


@app.callback(Output('forecast', 'children'),
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
# TAB 2 ENDS
# TAB 3 STARTS


@app.callback(Output('corr-graphic', 'figure'),
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
                                hovermode='closest')
            }


@app.callback(Output('corrRes', 'children'),
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


@app.callback(Output('corrType', 'children'),
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


@app.callback(Output('output-data-upload', 'children'),
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
@app.callback(Output("content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/home":
        return home
    if pathname == "/about":
        return about
    if pathname == "/caw":
        return caw

    # if not recognised, return 404 message
    return html.P("Adding Soon")
# ========================== Server =============================================


if __name__ == "__main__":
    app.run_server(debug=True)
