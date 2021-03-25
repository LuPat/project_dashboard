import flask
import dash
import dash_html_components as html


app = dash.Dash(__name__)
server = app.server‚

app.layout = html.Div('My Dashboard')


if __name__ == '__main__':
    app.run_server(debug=True)