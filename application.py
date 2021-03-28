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

pio.templates.default = 'plotly'

# Import Data, set 'date' column to datetime and as index
cars = pd.read_csv('./data/car_builds_long_format.csv', index_col=0, parse_dates=True)
cars['date'] = pd.to_datetime(cars['date'])

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
                html.H6(
                    "Please choose region and customer",
                    className="card-text",
                ),
                dbc.FormGroup([
                    
                    dbc.Checklist(
                        options=region, value=[], id="checklist_region", inline=True
                    ),
                ]),
                #     'Europe', id='eu_button', value=region, color='primary'),
                # dbc.Button('Middle East / Africa', id='mea', color='primary'),
                # ], size='sm'),
                # dbc.Button("Europe", id="eu_button", color="primary"),
                # dbc.Button("Midlle East / Africa", id="mea_button", color="primary"),
                dcc.Dropdown(id='customer_choice', options=customer,
                             value='BMW', placeholder='select Customer', clearable=True, style={"color": "#000000"}),
                dcc.Dropdown(id='plant_choice', options=plant,
                              value=' ', clearable=True, style={"color": "#000000"}),
                 #dbc.CardLink("GirlsWhoCode", href="https://girlswhocode.com/", target="_blank"),
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
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("That's your KPI"),
                dbc.CardBody([
                    ("DIsplay the KPI NUmber"),
                ]),
            ]),
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("That's your KPI 2"),
                dbc.CardBody([
                    ("DIsplay the KPI NUmber"),
                ]),
            ]),
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("That's your KPI3"),
                dbc.CardBody([
                    ("DIsplay the KPI NUmber"),
                ]),
            ]),
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("That's your KPI4"),
                dbc.CardBody([
                    ("DIsplay the KPI NUmber"),
                ]),
            ],
        )),
    ]),               
    
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
    Output('customer_choice', 'options'),
    Output('customer_choice', 'value'),
    [Input('checklist_region', 'value')]
)
def update_dropdown(selected_region):
    df = cars
    filter_region = df[df['region'] == selected_region]
    return country_options

@app.callback(
    Output('carbuilds_graph', 'figure'),
    [Input('customer_choice', 'value')],
    [Input('customer_choice', 'value')]
    )

def update_graph(selected_customer, selected_data):
    df = cars
    df = df.groupby(['region', 'country', 'customer', 'date']).sum().reset_index()
    customer_filter = df[df['customer'] == selected_customer]
    line_fig = line_fig = px.bar(customer_filter, x='date', y='carbuilds', title=f'Carbuilds in {selected_customer}')
    line_fig.update_xaxes(rangeslider_visible=True)
    line_fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
        ])
    ))
    line_fig.update_layout(
        font_family='Courier New',
        font_color='Black',
        title_font_family='Times New Roman',
        legend_title_font_color="grey"
    )   
    return line_fig

if __name__ == '__main__':
    app.run_server(debug=True)
