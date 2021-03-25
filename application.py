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

pio.templates.default = 'plotly_dark'

cars = pd.read_csv('./data/car_builds_long_format.csv', index_col=0, parse_dates=True)
cars['date'] = pd.to_datetime(cars['date'])
cars.index = cars['date']
print(cars.head())

plant = [{'label':i, 'value': i} for i in cars['plant'].unique()]
country = [{'label':i, 'value': i} for i in cars['country'].unique()]
region = [{'label':i, 'value': i} for i in cars['region'].unique()]


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
server = app.server


app.layout = html.Div(children=[
   html.H1(children='Hello Sherin'),
   html.Div(children='''Dash Framework: A web application framework for Python.'''),
   
   dcc.RadioItems(
       id = 'radio-region',
       options = region, 
       value = 'Middle East/Africa'),
   
   dcc.Graph(
      id='carbuilds_graph'
   )
])

@app.callback(
    Output('carbuilds_graph', 'figure'),
    Input('radio-region', 'value'))

def update_graph(selected_region):
    region_filter = cars[cars['region'] == selected_region]
    line_fig = px.bar(region_filter,
                       x= "date", y = 'carbuilds',
                       title=f'{selected_region}')
    return line_fig

if __name__ == '__main__':
    app.run_server(debug=True)
