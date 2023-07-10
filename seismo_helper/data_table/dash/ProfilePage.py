from dash import html, dcc, no_update, Dash, dash_table, callback
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import plotly.express as px
from data_table.dash.Pageblank import footer, navbar, stylesheets
import os
from dash.dependencies import Output, Input, State
import requests as rq
from seismo_helper.settings import ALLOWED_HOSTS


app = DjangoDash('ProfilePage',external_stylesheets=stylesheets)

app.layout = html.Div([
    navbar,
    html.H2('Ваш профиль'),
    html.Div(id='usrn', children=[]),
    dcc.Store(id="session", data=''),
    footer
])
@app.callback(
    Output('usrn', 'children'),
    State('session', 'data')    
)
def load_profile(aboba):
    data = rq.get(f'http://{ALLOWED_HOSTS[0]}:8000/auth/users/me', headers={'Authorization':'Token ' + aboba})
    print(data)
    return str(data)