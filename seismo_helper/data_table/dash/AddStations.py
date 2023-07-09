from dash import html, dcc, no_update, Dash, dash_table, callback
from seismo_helper.settings import ALLOWED_HOSTS
import pandas as pd
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import plotly.express as px
from data_table.dash.Pageblank import footer, navbar
import os
from dash.dependencies import Output, Input, State
import requests as rq

DATABASE_API = f'http://{ALLOWED_HOSTS[0]}:8000/api/'
BASE_LINK = f'http://{ALLOWED_HOSTS[0]}:8000/Events/'
app = DjangoDash('AddStations',external_stylesheets=[dbc.themes.BOOTSTRAP])
fupd = 0
table_columns = [
    {
        'id': '0',
        'name': '№',
        'sortable': True,
        'textAlign': 'center'
    },
    {
        'id': '1',
        'name': 'name',
        'sortable': True,
        'textAlign': 'center'
    },
    {
        'id': '2',
        'name': 'X',
        'sortable': True,
        'textAlign': 'center'
    },
    {
        'id': '3',
        'name': 'Y',
        'sortable': True,
        'textAlign': 'center'
    },
    {
        'id': '4',
        'name': 'Z',
        'sortable': True,
        'textAlign': 'center'
    }]

app.layout = html.Div([
    navbar,
    html.H1('Добавление станций приёма сигнала'),
    html.Div(id='ddd', children=[dcc.Dropdown(['Локация'], 'Локация', id='dd')]),
    html.Div(id='container-button-basic'),
    footer
])

@app.callback(
    Output('ddd', 'children'),
    Input('dd', 'value')
)
def upd_dd(value):
    global fupd
    vv = rq.get(DATABASE_API + 'locations/').json()['results']
    dt = rq.get(DATABASE_API + 'stations/').json()['results']
    S = [[],[],[],[], []]
    for i in dt:
        S[0].append(i['id'])
        S[1].append(i['name'])
        S[2].append(i['x'])
        S[3].append(i['y'])
        S[4].append(i['z'])
    A = [{'label': x['name'], 'value':x['id']} for x in vv]
    df = pd.DataFrame(S).T.sort_values(0)
    if fupd == 0:
        fupd += 1
        return [dcc.Dropdown(options=A, value=value, id='dd'),
                dcc.Input(id='name', placeholder='Название', type='text'),
                dcc.Input(id='X', placeholder='Широта', type='float'),
                dcc.Input(id='Y', placeholder='Долгота', type='float'),
                dcc.Input(id='Z', placeholder='Высота над уровнем моря', type='float'),
                html.Button('Добавить', id='submit-val', n_clicks=0),
                dash_table.DataTable(
                    id='datatable',
                    columns=table_columns,
                    data=df.to_dict('records'),style_cell={'textAlign': 'center'})]
    else:
        return no_update


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
    if x != None and loc_id != 'Локация':
        data = {
            "name": name,
            "x":x,
            "y":y,
            "z":z,
            "location": loc_id,
        }
        rq.post(DATABASE_API + 'stations/', data=data)