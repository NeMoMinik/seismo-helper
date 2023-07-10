import dash
from dash import html, dcc, no_update, Dash, dash_table, callback
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from data_table.dash.Pageblank import footer, navbar, stylesheets
from dash.dependencies import Output, Input, State
import requests as rq
from backend.views import logged
app = DjangoDash('LoginPage',external_stylesheets=stylesheets)

app.layout = html.Div([
    navbar,
    html.H1('Войдите или зарегистрируйтесь'),
    html.Div([
        dcc.Input(id='username', placeholder='Имя пользователя', type='text'),
        dcc.Input(id='password', placeholder='Пароль', type='password'),
        html.Button('Добавить', id='submit_val', n_clicks=0),
    ]),
    footer,
    html.Div(id="hidden_div_for_callback")
])


@app.callback(
    Output("hidden_div_for_callback", "children"),
    Input("submit_val", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
    prevent_initial_call=True,
)
def log_in(n_clicks, username, password):
    r = rq.post("http://127.0.0.1:8000/auth/token/login/", data={"username": username, "password": password}).json()
    print(r)
    if "auth_token" in r:
        dash.callback_context.response().set_cookie("Authorization", "Token " + r['auth_token'])
        return dcc.Location(pathname="Events/", id="someid_doesnt_matter")
    else:
        return no_update
