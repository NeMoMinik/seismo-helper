from dash import html, dcc, no_update, Dash, dash_table, callback
from seismo_helper.settings import ALLOWED_HOSTS, DATABASE_API
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
from data_table.dash.Pageblank import footer, navbar, stylesheets
from dash.dependencies import Output, Input, State
import requests as rq
import pandas as pd

app = DjangoDash('AddLocations', external_stylesheets=stylesheets)

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
    }
]

app.layout = html.Div([
    navbar,
    html.H1('Добавление локаций'),
    html.Div(id='ddd', children=[dcc.Dropdown(['Локация'], 'Локация', id='dd')]),
    html.Div(id='container-button-basic'),
    dcc.Store(id="session", data=''),
    footer
])


@app.callback(
    Output('ddd', 'children'),
    Input('dd', 'value'),
    State('session', 'data')
)
def upd_dd(value, token):
    global fupd
    user = rq.get(f'http://{ALLOWED_HOSTS[0]}:8000/auth/users/me', headers=token).json()
    dt = rq.get(DATABASE_API + f'locations/?corporation={user["corporation"]}', headers=token).json()['results']
    S = [[], []]
    for i in dt:
        S[0].append(i['id'])
        S[1].append(i['name'])
    df = pd.DataFrame(S).T.sort_values(0)
    return [
        dcc.Input(id='name', placeholder='Название', type='text', style={'margin-left': '1%'}),
        html.Button('Добавить', id='submit-val', n_clicks=0, style={'margin-left': '1%'}),
        html.Div(id='tableDiv', children=[dash_table.DataTable(
            id='datatable',
            columns=table_columns,
            sort_action="native",
            sort_mode="single",
            data=df.to_dict('records'), style_cell={'textAlign': 'center'})])]


@app.callback(
    Output('tableDiv', 'children'),
    Input('submit-val', 'n_clicks'),
    State('name', 'value'),
    State('session', 'data'),
    prevent_initial_call=True
)
def update_output(n_clicks, name, token):
    stuff = {
             "A valid number is required.": "введите ЧИСЛЕННОЕ значение.",
             "name": "Название",
             "This field may not be blank.": "Поле не может быть пустым.",
             "This field is required.": "Это поле обязательно"}
    user = rq.get(f'http://{ALLOWED_HOSTS[0]}:8000/auth/users/me', headers=token).json()
    data = {
        "name": name,
        "corporation": user["corporation"]
    }
    r = rq.post(DATABASE_API + 'locations/', headers=token, data=data)
    print(r.content)
    text = "Успешно"
    if r.status_code == 400:
        text = ''
        for i in r.json():
            try:
                text += f"{stuff[i]}: {stuff[r.json()[i][0]]}\n"
            except KeyError:
                print(r.json()[i])
                # text += r.json()[i]
    S = [[], []]
    dt = rq.get(DATABASE_API + 'locations/', headers=token).json()['results']
    for i in dt:
        S[0].append(i['id'])
        S[1].append(i['name'])
    df = pd.DataFrame(S).T.sort_values(0)
    return [dash_table.DataTable(
        id='datatable',
        columns=table_columns,
        sort_action="native",
        sort_mode="single",
        data=df.to_dict('records'),
        style_cell={'textAlign': 'center'}),
        text]
