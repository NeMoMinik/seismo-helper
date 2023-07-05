from dash import html, dcc, no_update
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from django.db.models import Count
import pandas as pd
from backend.models import Event
<<<<<<< Updated upstream
# from backend.models import

app = DjangoDash('DashDatatable')
=======
import plotly.express as px

app = DjangoDash('DashDatatable')

vv = Event.objects.all().values('id', 'location__name', 'time', 'x', 'y', 'z', 'magnitude')
S = [[],[],[],[],[],[],[]]
for i in vv:
    S[0].append(i['id'])
    S[1].append(i['location__name'])
    S[2].append(i['time'])
    S[3].append(i['x'])
    S[4].append(i['y'])
    S[5].append(i['z'])
    S[6].append(float(i['magnitude']))
df = pd.DataFrame(S).T.sort_values(0)
table_columns  = [
    {
        'id': '0',
        'name': '№',
        'sortable': True,
    },
    {
        'id': '1',
        'name': 'Локация',
        'sortable': True,
    },
    {
        'id': '2',
        'name': 'Время',
        'sortable': True,
    },
    {
        'id': '3',
        'name': 'X',
        'sortable': False,
    },
    {
        'id': '4',
        'name': 'Y',
        'sortable': False,
    },
    {
        'id': '5',
        'name': 'Z',
        'sortable': False,
    },
    {
        'id': '6',
        'name': 'Магнитуда',
        'sortable': True,
    }
]
Size = [df[6][i] for i in range(len(df[6]))]
fig = px.scatter_mapbox(df, lat = 3, lon = 4, size = Size,
                        color = 6, color_continuous_scale = 'plasma',
                        zoom = 3, mapbox_style = 'open-street-map')
>>>>>>> Stashed changes

app.layout = html.Div(
    [html.H1("Таблица событий"),
    dcc.Graph(id='events_table'),
    dbc.Button(id='update_table', children='Обновить таблицу', n_clicks=0)]
)
@app.callback(
    Output('events_table', 'figure'),
    Input('update_table', 'n_clicks'),
)

def update_events_table(n):
    vv = Event.objects.all().values('id', 'location__name', 'time', 'x', 'y', 'z', 'magnitude')
    S = [[],[],[],[],[], [], []]
    for i in vv:
        S[0].append(i['id'])
        S[1].append(i['location__name'])
        S[2].append(i['time'])
        S[3].append(i['x'])
        S[4].append(i['y'])
        S[5].append(i['z'])
        S[6].append(i['magnitude'])
    df = pd.DataFrame(S).T.sort_values(0).T
    data = go.Figure(
        data=[go.Table(header=dict(values=['№', 'Локация', 'Время', 'x','y', 'z', 'Магнитуда']), cells={"values": df.values})]
    )
    data.update_layout(
    updatemenus=[
        {
            "buttons": [
                {
                    "method": "restyle",
                    "label": b["l"],
                    "args": [{"cells": {"values": df.T.sort_values(b["c"]).T.values}},[0],],
                }
                for b in [{"l": "№", "c": 0}, {"l": "Локация", "c": 1}, {"l": "Время", "c": 2}, {"l": "Магнитуда", "c": 6}]
            ],
            "direction": "down",
            "y": 1,
        }
    ]
)
    return go.Figure(data=data)