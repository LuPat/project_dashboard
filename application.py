import numpy as np
import pandas as pd
import datetime as dt
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
# -----load general plotly template for graphs
pio.templates.default = 'plotly'
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

# ---- import data, set 'date' column to datetime and as index
cars = pd.read_csv(
    './data/car_builds_long_format.csv',
    index_col=0,
    parse_dates=True)
cars['date'] = pd.to_datetime(cars['date'])
cars['year'] = cars['date'].dt.year

# ---- groupby base dateset for barchart
df = cars.groupby(['region', 'country', 'customer',
                   'plant', 'date']).sum().reset_index()

# ---- data processing pie charts
cars_2020 = cars[(cars['year'] == 2020)]  # .reset_index()
cars_europe = cars_2020[(cars_2020['region'] == 'Europe')]
cars_europe = cars_europe.groupby('customer').sum().sort_values(
    'carbuilds', ascending=False).head(5).reset_index()
fig_pie1 = px.pie(
    cars_europe,
    values='carbuilds',
    names='customer',
    title='Share Europe')

cars_mea = cars_2020[(cars_2020['region'] == 'Middle East/Africa')]
cars_mea = cars_mea.groupby('customer').sum().sort_values(
    'carbuilds', ascending=False).head(5).reset_index()
fig_pie2 = px.pie(
    cars_mea,
    values='carbuilds',
    names='customer',
    title='Share Middle East/Africa')

# ---- data for data table
df_table = cars
df_grouped = df_table.groupby(
    ['customer', 'plant', 'date']).sum().reset_index()

# ---- create base data for data table
# df_table = cars[cars['region'] == 'Europe']
# df_table['year'] = df_table['date'].dt.year
# df_table = df_table.groupby(['region', 'year', 'date']).sum().reset_index()

# ---- define variables with unique names for customer, plant, country and region
# ---- may delete partly
customer_options = [{'label': i, 'value': i} for i in df['customer'].unique()]
plant_options = [{'label': i, 'value': i} for i in df['plant'].unique()]
country_options = [{'label': i, 'value': i} for i in df['country'].unique()]
region_options = [{'label': i, 'value': i} for i in df['region'].unique()]


# ---- activate the dash app
# suppress_callback_exceptions=True
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
server = app.server

# ---- create nav bar for body
navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand("Navbar", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://plot.ly",
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.NavItem(dbc.NavLink('Page 1', href='#')),
        dbc.NavItem(dbc.NavLink('Page 2', href='#')),

    ],
    color="dark",
    dark=True,
)


# ---- card with picture and dropdown menu for main seletcion
card_main = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="EMEA", tab_id="tab-1"),
                    dbc.Tab(label="Global", tab_id="tab-2"),
                ],
                id="card-tabs",
                card=True,
                active_tab="tab-1",
            )
        ),
        dbc.CardImg(src="/assets/big_data.jpeg", top=True, bottom=False,
                    title="Image by https://unsplash.com/@ev", alt='Learn Dash Bootstrap Card Component'),
        dbc.CardBody(
            [
                html.H6(
                    "Please choose region and customer",
                    id="card-content",
                    className="card-text",
                ),
                dcc.Dropdown(id='region_choice', options=region_options,
                             value='Europe', placeholder='select Region', clearable=True, style={"color": "#000000"}),
                dcc.Dropdown(
                    id='customer_choice',
                    placeholder='select Customer',
                    clearable=True,
                    style={
                        "color": "#000000"}),
                dcc.Dropdown(
                    id='plant_choice',
                    placeholder='select Customer Plant',
                    clearable=True,
                    style={
                        "color": "#000000"}),
            ],
        ),
    ],
    color="Primary",   # https://bootswatch.com/default/ for more card colors
    inverse=True,   # change color of text (black or white)
    outline=False,  # True = remove the block colors from the background and header
    # body=True
)

# ---- create card with graph inside
card_graph = dbc.Card(
    dcc.Graph(id='my_bar', figure={}), body=True, color="secondary",
)


card_table = dash_table.DataTable(
    id='datatable-interactivity',
    columns=[
        {"name": i, "id": i, "deletable": True,
            "selectable": True, "hideable": True}
        if i == "iso_alpha3" or i == "year" or i == "id"
        else {"name": i, "id": i, "deletable": True, "selectable": True}
        for i in df_table.columns
    ],
    data=df_table.to_dict('records'),  # the contents of the table
    editable=True,              # allow editing of data inside all cells
    # allow filtering of data by user ('native') or not ('none')
    filter_action="native",
    # enables data to be sorted per-column by user or not ('none')
    sort_action="native",
    sort_mode="single",         # sort across 'multi' or 'single' columns
    column_selectable="multi",  # allow users to select 'multi' or 'single' columns
    row_selectable="multi",     # allow users to select 'multi' or 'single' rows
    # choose if user can delete a row (True) or not (False)
    row_deletable=True,
    selected_columns=[],        # ids of columns that user selects
    selected_rows=[],           # indices of rows that user selects
    # all data is passed to the table up-front or not ('none')
    page_action="native",
    page_current=0,             # page number that user is on
    page_size=6,                # number of rows visible per page
    style_cell={                # ensure adequate header width when text is shorter than cell's text
        'minWidth': 95, 'maxWidth': 95, 'width': 95
    },
    style_cell_conditional=[    # align text columns to left. By default they are aligned to right
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['country', 'iso_alpha3']
    ],
    style_data={                # overflow cells' content into multiple lines
        'whiteSpace': 'normal',
        'height': 'auto'
    }
)

# ---- create data for second bar chart
# data_europe = cars
# fig = px.bar(data_europe, x='year', y='carbuilds',
#              hover_data=['region', 'carbuilds'],
#              labels={'pop':'Carbuilds Europe 2010 - 2021'}, height=400,
#              title='Carbuilds Europe 2010 - 2021')

# ---- main dash content body
app.layout = html.Div(children=[
    # ---- style header above main body
    dbc.Row(
        dbc.Col(
            html.Div(
                className="app-header",
                children=[
                    html.Div(
                        'Spiced - DashBoard - Car Builds ',
                        className="app-header--title"),
                ]
            ))),
    dbc.Row([], style={'height': '1vh'}),

    #---- navbar
    dbc.Row(navbar),
    # ---- style first row with 4 columns for kpi information
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader('Builds Total Europe 2020'),
                dbc.CardBody([
                    # html.H4("21.6MM cars"),
                    html.H4(
                        dbc.Badge(
                            "21.6MM UNITS",
                            className="btn btn-info")),
                ]),
            ]),
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Builds Middle East/Africa 2021"),
                dbc.CardBody([
                    html.H4(
                        dbc.Badge(
                            "2.4MM UNITS",
                            className="btn btn-info")),
                ]),
            ]),
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("That's your KPI3"),
                dbc.CardBody([
                    html.H4(
                        dbc.Badge(
                            "Succesful KPI",
                            className="btn btn-success")),
                ]),
            ],),
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("That's your KPI4"),
                dbc.CardBody([
                    html.H4(
                        dbc.Badge(
                            "Danger KPI",
                            className="btn btn-danger")),
                ]),
            ],
            )),
    ]),
    # ---- style second row with two columns for barchart and dropdown
    html.Div(children=[
        dbc.Row([
            dbc.Col(dcc.Graph(
                id='carbuilds_graph'),
                width=8, lg={'size': 8, "offset": 0, 'order': 'first'}
            ),
            dbc.Col(dbc.Card(children=[
                card_main,
            ]), ),
        ]),
    ], className='divFrame'),

    # ---- style third row with 2 columns for data table
    html.Div(children=[
        card_table
        # dbc.Row([
        #     dbc.Col(dcc.Graph(
        #         id='pie_europe',
        #         figure = fig_pie1
        #     ), width=4, lg={'size': 8,  "offset": 0, 'order': 'first'}
        #         ),
        #     dbc.Col(dcc.Graph(
        #         id='pie_mea',
        #         figure = fig_pie2
        #     ),width=4, lg={'size': 8,  "offset": 0, 'order': 'first'}
        #     ),
        # ]),
    ], className='divFrame')
], className='divBorder')


# ---- callback for tabs in cards
# @app.callback(
#     Output("card-content", "children"), [Input("card-tabs", "active_tab")]
# )
# def tab_content(active_tab):
#     return "This is tab {}".format(active_tab)

# ---- callback to select region in dropdown
@app.callback(
    Output(component_id='customer_choice', component_property='options'),
    Output(component_id='customer_choice', component_property='value'),
    Input(component_id='region_choice', component_property='value')
)
def update_customer(selected_region):
    # print(region)
    print(f'Selected Region : {selected_region}')
    filter_region = df[df['region'] == selected_region]
    customer_options = [{'label': i, 'value': i}
                        for i in sorted(filter_region['customer'].unique())]
    print(f'Customer Options : {customer_options}')
    return customer_options, customer_options[0]['value']

# ---- callback to select customer


@app.callback(
    Output('plant_choice', 'options'),
    Output('plant_choice', 'values'),
    #Input('customer_choice', 'options'),
    Input('customer_choice', 'value')
)
def update_plant(selected_customer):
    # print(selected_customer)
    # print(len(selected_customer))
    print(f'Input Update Plant : {selected_customer}')
    filter_customer = df[df['customer'] == selected_customer]
    #print(f'Filtered Customer : {filter_customer}')
    plant_options = [{'label': x, 'value': x}
                     for x in sorted(filter_customer['plant'].unique())]
    print(f'Plant Options : {plant_options}')
    return plant_options, plant_options[0]['value'],


# ---- final callback to select plant and function for graph data
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
    line_fig = line_fig = px.bar(
        df_plant,
        x='date',
        y='carbuilds',
        title=f'Carbuilds @ plant : {choosen_plant}')
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
        legend_title_font_color="grey",
        #xaxis_range=['2010-01-01', '2021-02-28']
    )
    return line_fig


if __name__ == '__main__':
    app.run_server(debug=True)
    #app.set("port", PORT)
