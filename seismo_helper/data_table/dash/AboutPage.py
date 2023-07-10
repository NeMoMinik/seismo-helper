from dash import html, dcc, no_update, Dash, dash_table, callback
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import plotly.express as px
from data_table.dash.Pageblank import footer, navbar
import os

app = DjangoDash('AboutPage',external_stylesheets=[dbc.themes.LUMEN])

app.layout = html.Div([
    navbar,
    html.H1('Сервис Seismo-helper'),
    html.P('Seismo-helper - сервис для автоматизированного мониторинга сейсмической активности'),
    footer
])