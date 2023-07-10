from dash import html, dcc, no_update, Dash, dash_table, callback
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import plotly.express as px
from data_table.dash.Pageblank import footer, navbar
import os
app = DjangoDash('TutorPage',external_stylesheets=[dbc.themes.LUMEN])

app.layout = html.Div([
    navbar,
    html.H1('Туториал по использованию сервиса'),
    html.Ul(id='my-list', children=[html.Li('Зарегистрироваться'),
            html.Li('На странице Events нужно загрузить miniseed-файлы, подождать пока сервер обработает их'),
            html.Li('На карте и в таблице под картой будут отображены обнаруженные точки сейсмической активности')]),
    footer
])
