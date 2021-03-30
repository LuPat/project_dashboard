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

'''
Author : Lutz Kinschert
Dashboard to present carbuild numbers
'''
#-----load general plotly template for graphs
pio.templates.default = 'plotly'


#---- import data, set 'date' column to datetime and as index
cars = pd.read_csv('./data/car_builds_long_format.csv', index_col=0, parse_dates=True)
cars['date'] = pd.to_datetime(cars['date'])

#---- groupby base dateset for barchart
df = cars.groupby(['region', 'country', 'customer', 'plant', 'date']).sum().reset_index()

#---- create base data for data table
# df_table = cars[cars['region'] == 'Europe']
# df_table['year'] = df_table['date'].dt.year
# df_table = df_table.groupby(['region', 'year', 'date']).sum().reset_index()

#---- define variables with unique names for customer, plant, country and region
#---- may delete partly
customer_options = [{'label':i, 'value': i} for i in df['customer'].unique()]
plant_options = [{'label':i, 'value': i} for i in df['plant'].unique()]
country_options = [{'label':i, 'value': i} for i in df['country'].unique()]
region_options = [{'label':i, 'value': i} for i in df['region'].unique()]


#---- activate the dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
server = app.server

#---- create style variables for main body 

#---- card with picture and dropdown menu for main seletcion
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
                dcc.Dropdown(id='region_choice', options=region_options,
                             value='Europe', placeholder='select Region', clearable=True, style={"color": "#000000"}),
                dcc.Dropdown(id='customer_choice', placeholder='select Customer', clearable=True, style={"color": "#000000"}),
                dcc.Dropdown(id='plant_choice', placeholder='select Customer Plant', clearable=True, style={"color": "#000000"}),
            ],
        ),
    ],
    color="Primary",   # https://bootswatch.com/default/ for more card colors
    inverse=True,   # change color of text (black or white)
    outline=False,  # True = remove the block colors from the background and header
    #body=True
)

#---- create card with graph inside 
card_graph = dbc.Card(
        dcc.Graph(id='my_bar', figure={}), body=True, color="secondary",
)

#---- create data for second bar chart 
# data_europe = cars
# fig = px.bar(data_europe, x='year', y='carbuilds',
#              hover_data=['region', 'carbuilds'],
#              labels={'pop':'Carbuilds Europe 2010 - 2021'}, height=400,
#              title='Carbuilds Europe 2010 - 2021')

#---- main dash content body
app.layout = html.Div(children=[
    #---- style header above main body
    dbc.Row(
        dbc.Col(
            html.Div(
                className="app-header",
                children=[
                    html.Div('Spiced - DashBoard - Car Builds ', className="app-header--title"),
                    ]
            ))),
    dbc.Row([],style={'height': '1vh'}),
    #---- style first row with 4 columns for kpi information
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader('Builds Total Europe 2020'),
                dbc.CardBody([
                    html.H4("21.6MM units"),
                ]),
            ]),
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Builds Middle East/Africa 2021"),
                dbc.CardBody([
                    html.H4("2.4MM units"),
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
    #---- style second row with two columns for barchart and dropdown
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
    ], className='divFrame'),

    #---- style third row with 2 columns for data table
    html.Div(children=[
        dbc.Row([
            dbc.Col(
                #dcc.Graph(
            #id='Builds per year',
            #figure = fig
            # ), width=4, lg={'size': 8,  "offset": 0, 'order': 'first'}
            ),
        ], className='divFrame')
        ])
], className='divBorder')

#---- callback to select region in dropdown
@app.callback(
    Output(component_id ='customer_choice', component_property='options'),
    Output(component_id='customer_choice', component_property='value'),
    Input(component_id='region_choice', component_property='value')
)

def update_customer(selected_region):
    #print(region)
    print(f'Selected Region : {selected_region}')
    filter_region = df[df['region'] == selected_region]
    customer_options = [{'label': i, 'value': i} for i in sorted(filter_region['customer'].unique())]
    print(f'Customer Options : {customer_options}')
    return customer_options, customer_options[0]['value']

#---- callback to select customer 
@app.callback(
    Output('plant_choice', 'options'),
    Output('plant_choice', 'values'),
    #Input('customer_choice', 'options'),
    Input('customer_choice', 'value')
)

def update_plant(selected_customer):
    #print(selected_customer)
    #print(len(selected_customer))
    print(f'Input Update Plant : {selected_customer}')
    filter_customer = df[df['customer'] == selected_customer]
    #print(f'Filtered Customer : {filter_customer}') 
    plant_options = [{'label': x, 'value': x} for x in sorted(filter_customer['plant'].unique())]
    print(f'Plant Options : {plant_options}')
    return plant_options, plant_options[0]['value'], 


#---- final callback to select plant and function for graph data
@app.callback(
    Output('carbuilds_graph', 'figure'),
    Input('plant_choice', 'value'),
    #Input('customer_choice', 'value'),
    #Input('region_choice', 'value)')
)

def update_graph(choosen_plant):
    print(f'Input plant filter : {choosen_plant}')
    df_plant = df[df.plant == choosen_plant]
    print(f'Selection for graph : {df_plant}')
    line_fig = line_fig = px.bar(df_plant, x='date', y='carbuilds', title=f'Carbuilds in {choosen_plant}')
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

