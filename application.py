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
from functions import clean_datetime

#pio.templates.default = 'plotly_dark'

# Import Data, set 'date' column to datetime and as index
cars = pd.read_csv('./data/car_builds_long_format.csv', index_col=0, parse_dates=True)
cars['date'] = pd.to_datetime(cars['date'])
cars = clean_datetime(cars)

# define variables with unique names for customer, plant, country and region
customer = [{'label':i, 'value': i} for i in cars['customer'].unique()]
plant = [{'label':i, 'value': i} for i in cars['plant'].unique()]
country = [{'label':i, 'value': i} for i in cars['country'].unique()]
region = [{'label':i, 'value': i} for i in cars['region'].unique()]

table_header = [
    html.Thead(html.Tr([html.Th("First Name"), html.Th("Last Name")]))
]

row1 = html.Tr([html.Td("Arthur"), html.Td("Dent")])
row2 = html.Tr([html.Td("Ford"), html.Td("Prefect")])
row3 = html.Tr([html.Td("Zaphod"), html.Td("Beeblebrox")])
row4 = html.Tr([html.Td("Trillian"), html.Td("Astra")])

table_body = [html.Tbody([row1, row2, row3, row4])]

table = dbc.Table(table_header + table_body, bordered=True)

table = dbc.Table(
    # using the same table as in the above example
    table_header + table_body,
    bordered=True,
    dark=True,
    hover=True,
    responsive=True,
    striped=True,
)

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
        dbc.Col(dcc.Dropdown(id='region-drop', placeholder='select region',
                             options=region, value='Europe'),
                             width={'size': 3}
                             ),
        dbc.Col(dcc.Dropdown(id='country-drop', placeholder='select country',
                             options=[], value=''),
                             width={'size': 3}
                             ),
        dbc.Col(dcc.Dropdown(id='customer', placeholder='select customer',
                            options=customer, value=''),
                            ),
        dbc.Col(dcc.Dropdown(id='plant-drop', placeholder='select plant',
                             options=plant, value=' '),
                             width={'size': 3}
                             ), 
    ], no_gutters=False
    ),
    dbc.Row([],style={'height': '1vh'}),
    dbc.Row([
        dbc.Col(dcc.Graph(
            id='carbuilds_graph'),
            width=8, lg={'size': 8,  "offset": 0, 'order': 'first'}
            ),
        dbc.Col(dbc.Table(table)),
    ], justify='around')
])

@app.callback(
    Output('country-drop', 'options'),
    Output('country-drop', 'value'),
    Input('region-drop', 'value'))

def update_dropdown(selected_region):
    region_filter = cars[cars['region'] == selected_region]
    country_options = [{'label': i, 'value': i} for i in
                        cars['country'].unique()]
    return country_options, country_options[0]['value']


@app.callback(
    Output('carbuilds_graph', 'figure'),
    Input('country-drop', 'value'),
    Input('region-drop', 'value'))

def update_graph(selected_region, selected_data):
    region_filter = cars[cars['region'] == selected_region]
    line_fig = px.bar(region_filter,
                       x= "year", y = 'carbuilds',
                       title=f'Region :{selected_region}')
    return line_fig

if __name__ == '__main__':
    app.run_server(debug=True)
