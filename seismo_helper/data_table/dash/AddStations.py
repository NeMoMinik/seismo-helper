from dash import html, dcc, no_update, dash_table
from seismo_helper.settings import ALLOWED_HOSTS, DATABASE_API
from django_plotly_dash import DjangoDash
from data_table.dash.Pageblank import footer, navbar, stylesheets
from dash.dependencies import Output, Input, State
import requests as rq
import pandas as pd

app = DjangoDash('AddStations', external_stylesheets=stylesheets)

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
    print(token)
    vv = rq.get(DATABASE_API + 'locations/', headers=token).json()['results']
    dt = rq.get(DATABASE_API + 'stations/', headers=token).json()['results']
    S = [[], [], [], [], []]
    for i in dt:
        S[0].append(i['id'])
        S[1].append(i['name'])
        S[2].append(i['x'])
        S[3].append(i['y'])
        S[4].append(i['z'])
    A = [{'label': x['name'], 'value': x['id']} for x in vv]
    df = pd.DataFrame(S).T.sort_values(0)
    return [dcc.Dropdown(options=A, value=value, id='dd'),
            dcc.Input(id='name', placeholder='Название', type='text', style={'margin-left': '1%'}),
            dcc.Input(id='X', placeholder='Широта', type='float', style={'margin-left': '1%'}),
            dcc.Input(id='Y', placeholder='Долгота', type='float', style={'margin-left': '1%'}),
            dcc.Input(id='Z', placeholder='Высота над уровнем моря', type='float',
                      style={'margin-left': '1%', 'width': '13%'}),
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
    State('X', 'value'),
    State('Y', 'value'),
    State('Z', 'value'),
    State('name', 'value'),
    State('dd', 'value'),
    State('session', 'data')
)
def update_output(n_clicks, x, y, z, name, loc_id, token):
    stuff = {"z": "Высота",
             "x": "Широта",
             "y": "Долгота",
             "A valid number is required.": "введите ЧИСЛЕННОЕ значение.",
             "name": "Название",
             "This field may not be blank.": "Поле не может быть пустым.",
             "This field is required.": "Это поле обязательно"}
    if (x or y or z) is not None and loc_id != 'Локация':
        data = {
            "name": name,
            "x": x,
            "y": y,
            "z": z,
            "location": loc_id,
        }
        r = rq.post(DATABASE_API + 'stations/', headers=token, data=data)
        text = "Успешно"
        txtstyle = {'color': 'Green'}
        if r.status_code == 400:
            text = ''
            for i in r.json():
                text += f"{stuff[i]}: {stuff[r.json()[i][0]]}\n"
        S = [[], [], [], [], []]
        dt = rq.get(DATABASE_API + 'stations/', headers=token).json()['results']
        for i in dt:
            S[0].append(i['id'])
            S[1].append(i['name'])
            S[2].append(i['x'])
            S[3].append(i['y'])
            S[4].append(i['z'])
        df = pd.DataFrame(S).T.sort_values(0)
        return [dash_table.DataTable(
            id='datatable',
            columns=table_columns,
            sort_action="native",
            sort_mode="single",
            data=df.to_dict('records'),
            style_cell={'textAlign': 'center'}),
            text]
    return no_update
