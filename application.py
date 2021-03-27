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
df = px.data.gapminder()

# activate the dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
server = app.server

# styles 

card_main = dbc.Card(
    [
        dbc.CardImg(src="/assets/big_data.jpeg", top=True, bottom=False,
                    title="Image by https://unsplash.com/@ev", alt='Learn Dash Bootstrap Card Component'),
        dbc.CardBody(
            [
                # html.H4("Learn Dash with Charming Data", className="card-title"),
                # html.H6("Please choose your options"),
                html.P(
                    "Please choose region and customer",
                    className="card-text",
                ),
                dbc.Button("Europe", id="eu_button", color="primary"),
                dbc.Button("Midlle East / Africa", id="mea_button", color="primary"),
                dcc.Dropdown(id='customer_choice', options=customer,
                             value='BMW', placeholder='select Customer', clearable=True, style={"color": "#000000"}),
                dcc.Dropdown(id='plant_choice', options=plant,
                             value=2007, clearable=True, style={"color": "#000000"}),
                # dbc.CardLink("GirlsWhoCode", href="https://girlswhocode.com/", target="_blank"),
            ]
        ),
    ],
    color="Primary",   # https://bootswatch.com/default/ for more card colors
    inverse=True,   # change color of text (black or white)
    outline=False,  # True = remove the block colors from the background and header
    #body=True
)

card_graph = dbc.Card(
        dcc.Graph(id='my_bar', figure={}), body=True, color="secondary",
)

app.layout = html.Div(children=[
    dbc.Row(
        dbc.Col(
            html.Div(
                className="app-header",
                children=[
                    html.Div('Spiced - DashBoard - Car Builds ', className="app-header--title"),
                    ]
            ))),
    dbc.Row([],style={'height': '1vh'}),
    # dbc.Row([
    #     dbc.Col(dcc.Dropdown(id='region-drop', placeholder='select region',
    #                          options=region, value='Europe'),
    #                          width={'size': 3}
    #                          ),
    #     dbc.Col(dcc.Dropdown(id='country-drop', placeholder='select country',
    #                          options=[], value=''),
    #                          width={'size': 3}
    #                          ),
    #     dbc.Col(dcc.Dropdown(id='customer', placeholder='select customer',
    #                         options=customer, value=''),
    #                         ),
    #     dbc.Col(dcc.Dropdown(id='plant-drop', placeholder='select plant',
    #                          options=plant, value=' '),
    #                          width={'size': 3}
    #                          ), 
    # ], no_gutters=False
    # ),
    dbc.Row([],style={'height': '1vh'}),
    html.Div(children=[
    dbc.Row([
        dbc.Col(dcc.Graph(
            id='carbuilds_graph'),
            width=8, lg={'size': 8,  "offset": 0, 'order': 'first'}
            ), 
        dbc.Col(dbc.Card(children=[
            card_main,
    ]), width=4,),
    ]),
    ], className='divFrame')
], className='divBorder')


@app.callback(
    Output('carbuilds_graph', 'figure'),
    Input('customer_choice', 'value')
    )

def update_graph(selected_customer):
    df = cars
    customer_filter = df[df['customer'] == selected_customer]
    line_fig = px.bar(customer_filter,
                       x= "year", y = 'carbuilds',
                       title=f'Customer :{selected_customer} Plant :')
    return line_fig

if __name__ == '__main__':
    app.run_server(debug=True)
