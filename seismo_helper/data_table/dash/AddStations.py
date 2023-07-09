from dash import html, dcc, no_update, Dash, dash_table, callback
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import plotly.express as px
from data_table.dash.Pageblank import footer, navbar
import os
from dash.dependencies import Output, Input, State

app = DjangoDash('AddStations',external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    navbar,
    html.H1('Добавление станций приёма сигнала'),
    html.Div([
        dcc.Input(id='name', placeholder='Название', type='text'),
        dcc.Input(id='X', placeholder='Широта', type='float'),
        dcc.Input(id='Y', placeholder='Долгота', type='float'),
        html.Button('Добавить', id='submit-val', n_clicks=0),
        html.Div(id='container-button-basic')
    ]),
    footer
])

@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    State('X', 'value'),
    State('Y', 'value'),
    State('name', 'value'),
)
def update_output(n_clicks, x, y, name):
    pass
