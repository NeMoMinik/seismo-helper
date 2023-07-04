from dash import html, dcc, no_update
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from django.db.models import Count
import random
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
    data = go.Figure(data=[go.Table(header=dict(values=['№', 'Локация', 'Время', 'Координаты', 'Магнитуда']),
                    cells=dict(values=Zaglushka(15)
                               ))])
    return go.Figure(data=data)

def Zaglushka(n):
    return [[random.randint(0,100) for i in range(n)] for q in range(5)]