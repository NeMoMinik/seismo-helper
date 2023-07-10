from dash import html, dcc, no_update, Dash, dash_table, callback
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
from data_table.dash.Pageblank import footer, navbar, stylesheets
from dash.dependencies import Output, Input, State
import requests as rq
import os

app = DjangoDash("SignUpPage", external_stylesheets=stylesheets)

app.layout = html.Div([
    navbar,
    html.H1('Сервис Seismo-helper'),
    html.P('Seismo-helper - сервис для автоматизированного мониторинга сейсмической активности'),
    html.Div([
        dcc.Input(id='username', placeholder='Имя пользователя', type='text'),
        # dcc.Input(id='email', placeholder='Почта', type='email'),
        dcc.Input(id='password', placeholder='Пароль', type='password'),
        html.Button('Регистрация', id='submit_val', n_clicks=0)]),
    dcc.Store(id="session", data=''),
    html.Div(id="hidden_div_for_callback"),
    footer
])


@app.callback(
    Output("hidden_div_for_callback", "children"),
    Input('submit_val', 'n_clicks'),
    State('username', 'value'),
    # State('email', 'value'),
    State('password', 'value'),
    State('session', 'data'),
    prevent_initial_call=True,
)
def register(clicks, username, password, data):  # email
    print(data)
    r = rq.post("http://127.0.0.1:8000/auth/users/", data={
        "username": username,
        # "email": email,
        "password": password
    }
            )
    print(r.content)
    return dcc.Location(pathname="About/", id="someid_doesnt_matter")