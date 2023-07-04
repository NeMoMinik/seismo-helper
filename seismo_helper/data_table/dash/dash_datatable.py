from dash import html, dcc, no_update
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from django.db.models import Count
import random
import pandas as pd
from backend.models import Event
# from backend.models import

app = DjangoDash('DashDatatable')

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
    vv = Event.objects.all()
    print(vv)
    v = Zaglushka(15)
    df = pd.DataFrame(v).T.sort_values(0).T
    data = go.Figure(
        data=[go.Table(header=dict(values=['№', 'Локация', 'Время', 'Координаты', 'Магнитуда']), cells={"values": df.values})]
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
                for b in [{"l": "№", "c": 0}, {"l": "Локация", "c": 1}, {"l": "Время", "c": 2}, {"l": "Магнитуда", "c": 4}]
            ],
            "direction": "down",
            "y": 1,
        }
    ]
)
    return go.Figure(data=data)

def Zaglushka(n):
    return [[random.randint(0,100) for i in range(n)] for q in range(5)]