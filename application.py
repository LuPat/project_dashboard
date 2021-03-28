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
df = cars.groupby(['region', 'country', 'customer', 'plant', 'date']).sum().reset_index()

# define variables with unique names for customer, plant, country and region
customer = [{'label':i, 'value': i} for i in df['customer'].unique()]
plant = [{'label':i, 'value': i} for i in df['plant'].unique()]
country = [{'label':i, 'value': i} for i in df['country'].unique()]
region = [{'label':i, 'value': i} for i in df['region'].unique()]
#df = px.data.gapminder()

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
                html.H6(
                    "Please choose region and customer",
                    className="card-text",
                ),
                dcc.Dropdown(id='region_choice', options=region,
                             value=None, placeholder='select Region', clearable=True, style={"color": "#000000"}),
                dcc.Dropdown(id='customer_choice', options= [],
                             value='', placeholder='select Customer', clearable=True, style={"color": "#000000"}),
                dcc.Dropdown(id='plant_choice', options=[],
                              value='', placeholder='select Customer Plant', clearable=True, style={"color": "#000000"}),
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
            ],),
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
    ]), ),
    ]),
    ], className='divFrame')
], className='divBorder')

# region selection
@app.callback(
    Output(component_id ='customer_choice', component_property='options'),
    #Output(component_id='customer_choice', component_property='value'),
    Input(component_id='region_choice', component_property='value')
)

def update_customer(selected_region):
    filter_region = df[df['region'] == selected_region]
    customer_options = [{'label': i, 'value': i} for i in sorted(filter_region['customer'].unique())]
    #print(customer_options)
    return customer_options#, customer_options[0]['value']

@app.callback(
    Output('plant_choice', 'options'),
    #Output('plant_choice', 'values'),
    #Input('customer_choice', 'options'),
    Input('customer_choice', 'value')
)
def update_plant(selected_customer):
    print(selected_customer)
    if type(selected_customer) !=str:
        val = selected_customer
        print(val)
        filter_customer = df[df['customer'] == val]
        
        #plant_options = [{'label': x, 'value': x} for x in sorted(filter_customer['plant'].unique())]
    return filter_customer, #plant_options[0]['value'], 


# select customer plant
# @app.callback(
#     Output('carbuilds_graph', 'figure'),
#     Input('plant_choice', 'value')
# )
# def select_plant(selected_plant):
#     select_plant = df[df.plant == selected_plant]
#     return select_plant




# def update_graph(selected_plant):
#     df_graph = df[df.plant == selected_plant]
#     line_fig = line_fig = px.bar(df_graph, x='date', y='carbuilds', title=f'Carbuilds in {selected_plant}')
#     line_fig.update_xaxes(rangeslider_visible=True)
#     line_fig.update_xaxes(
#         rangeslider_visible=True,
#         rangeselector=dict(
#             buttons=list([
#                 dict(count=1, label="1m", step="month", stepmode="backward"),
#                 dict(count=6, label="6m", step="month", stepmode="backward"),
#                 dict(count=1, label="YTD", step="year", stepmode="todate"),
#                 dict(count=1, label="1y", step="year", stepmode="backward"),
#                 dict(step="all")
#         ])
#     ))
#     line_fig.update_layout(
#         font_family='Courier New',
#         font_color='Black',
#         title_font_family='Times New Roman',
#         legend_title_font_color="grey"
#     )   
#     return line_fig

if __name__ == '__main__':
    app.run_server(debug=True)
