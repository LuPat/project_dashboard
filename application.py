import flask
import dash
import plotly.io as pio
import dash_html_components as html
import dash_bootstrap_components as dbc

pio.templates.default = 'plotly_dark'

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
server = app.server

app.layout = html.Div('My Dashboard')



if __name__ == '__main__':
    app.run_server(debug=True)