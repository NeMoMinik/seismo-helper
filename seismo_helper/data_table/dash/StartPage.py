from dash import html, dcc, no_update, Dash, dash_table, callback
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import plotly.express as px
from data_table.dash.Pageblank import footer, navbar
import os
from seismo_helper.settings import ALLOWED_HOSTS
import dash_mantine_components as dmc


app = DjangoDash('StartPage',external_stylesheets=[dbc.themes.LUMEN])

BASE_LINK = f'http://{ALLOWED_HOSTS[0]}:8000/'


app.layout = html.Div([
    navbar,
    html.H1('SEISMO-HELPER'),
    html.Div(dbc.NavItem(dbc.NavLink("Мониторинг", href=BASE_LINK+'Events/', target='_blank', style={'color':'white'}),
                         style={'background':'#0D6EFD'}), style={'width': '30%', 'display': 'inline-block', 'float': 'left', 'textAlign': 'center',
                        'margin': '12px', 'height': '40px'}),
    footer
])
