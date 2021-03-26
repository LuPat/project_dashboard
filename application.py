'''
Author : Lutz Kinschert
Dashboard to present carbuild numbers
'''

import numpy as np
import pandas as pd
import flask
import dash
import dash_table
import plotly.io as pio
import plotly.express as px
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output

#pio.templates.default = 'plotly_dark'

# Import Data, set 'date' column to datetime and as index
cars = pd.read_csv('./data/car_builds_long_format.csv', index_col=0, parse_dates=True)
cars['date'] = pd.to_datetime(cars['date'])
cars.index = cars['date']

# define variables with unique names for customer, plant, country and region
customer = [{'label':i, 'value': i} for i in cars['customer'].unique()]
plant = [{'label':i, 'value': i} for i in cars['plant'].unique()]
country = [{'label':i, 'value': i} for i in cars['country'].unique()]
region = [{'label':i, 'value': i} for i in cars['region'].unique()]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
server = app.server


app.layout = html.Div([
    dbc.Row(
        dbc.Col(
            html.Div(
                className="app-header",
                children=[
                    html.Div('Spiced - DashBoard - Car Builds ', className="app-header--title"),
                    ]
            ))),
    dbc.Row([],style={'height': '1vh'}),
    dbc.Row([
        dbc.Col(dcc.Dropdown(id='region_a', placeholder='first dropdown',
                             options=region, value='Europe'),
                             width={'size': 4, 'order':1}
                             ),
        dbc.Col(dcc.Dropdown(id='country_a', placeholder='second dropdown',
                             options=country, value='Germany'),
                             width={'size': 4, 'order':1}
                             ),  
        dbc.Col(width={'size':4, 'order':3}
        ),
    ], no_gutters=False
    ),
    dbc.Row([],style={'height': '1vh'}),
    dbc.Row([
        dbc.Col(dcc.Graph(
            id='carbuilds_graph'),
            width=8, lg={'size': 8,  "offset": 0, 'order': 'first'}
            )
    ])
])


    #         dbc.Col(width=4, lg={'size': 6,  "offset": 0, 'order': 'last'}
    #         )

#     html.Div(
#         children=html.Div([
#             dbc.Row(dbc.Col(html.H5('Overview'))),
#             dbc.Row(dbc.Col(html.H5('Overview'))),
#             dbc.Row(dbc.Col(html.H5('Overview'))),
#             dcc.RadioItems(
#                 id = 'radio-region',
#                 options = region, 
#                 value = 'Middle East/Africa'),
#             html.Div('''
#                 This is an example of a simple Dash app with
#                 local, customized CSS.
#             '''),


@app.callback(
    Output('carbuilds_graph', 'figure'),
    Input('dropdown-region', 'value'))

def update_graph(selected_region):
    region_filter = cars[cars['region'] == selected_region]
    line_fig = px.bar(region_filter,
                       x= "date", y = 'carbuilds',
                       title=f'{selected_region}')
    return line_fig

if __name__ == '__main__':
    app.run_server(debug=True)
