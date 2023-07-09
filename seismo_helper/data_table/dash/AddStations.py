from dash import html, dcc, no_update, Dash, dash_table, callback
from seismo_helper.settings import ALLOWED_HOSTS
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
from data_table.dash.Pageblank import footer, navbar
from dash.dependencies import Output, Input, State
import requests as rq

DATABASE_API = f'http://{ALLOWED_HOSTS[0]}:8000/api/'
BASE_LINK = f'http://{ALLOWED_HOSTS[0]}:8000/Events/'
app = DjangoDash('AddStations',external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div([
    navbar,
    html.H1('Добавление станций приёма сигнала'),
    html.Div(id='ddd', children=[dcc.Dropdown(['Локация'], 'Локация', id='dd')]),
    dcc.Input(id='name', placeholder='Название', type='text'),
    dcc.Input(id='X', placeholder='Широта', type='float'),
    dcc.Input(id='Y', placeholder='Долгота', type='float'),
    dcc.Input(id='Z', placeholder='Высота над уровнем моря', type='float'),
    html.Button('Добавить', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic'),
    footer
])

@app.callback(
    Output('ddd', 'children'),
    Input('dd', 'value')
)
def upd_dd(value):
    vv = rq.get(DATABASE_API + 'locations/').json()['results']
    A = [{'label': x['name'], 'value':x['id']} for x in vv]
    return [dcc.Dropdown(options=A, value=value, id='dd')]

@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    State('X', 'value'),
    State('Y', 'value'),
    State('Z', 'value'),
    State('name', 'value'),
    State('dd', 'value')
)
def update_output(n_clicks, x, y, z, name, loc_id):
    if loc_id != 'Локация':
        data = {
            "name": name,
            "x":x,
            "y":y,
            "z":z,
            "location": loc_id,
        }
        rq.post(DATABASE_API + 'stations/', data=data)