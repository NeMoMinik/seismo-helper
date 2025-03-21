from dash import html, dcc, no_update
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
from data_table.dash.Pageblank import footer, navbar, stylesheets
from dash.dependencies import Output, Input, State
import requests as rq

app = DjangoDash('LoginPage', external_stylesheets=stylesheets)
AUTH = "http://127.0.0.1:8000/"
app.layout = html.Div([
    navbar,
    html.H1('Войдите или зарегистрируйтесь', style={'margin-top': '10%', 'text-align': 'center', 'font-size': '25px'}),
    html.Div([
        dbc.Col([
            dbc.Row(dcc.Input(id='username', placeholder='Имя пользователя', type='text'), style={'margin-top': '1%'}),
            dbc.Row(dcc.Input(id='password', placeholder='Пароль', type='password'), style={'margin-top': '1%'}),
            dbc.Row(html.Button('Войти', id='submit_val', n_clicks=0), style={'margin-top': '1%'}),
            dbc.Row(html.Button('Зарегистрироваться', id='signupbutton', n_clicks=0),
                    style={'margin-right': 'auto', 'text-align': 'center', 'margin-left': 'auto', 'margin-top': '5%',
                           'width': '60%'})
        ])
    ], style={'margin-right': 'auto', 'margin-left': 'auto', 'width': '20%'}),
    dcc.Store(id="session", data=''),
    html.Div(id="hidden_div_for_callback"),
    html.Div(id="redirdiv"),
    footer
])


@app.callback(
    Output("redirdiv", "children"),
    Input("signupbutton", "n_clicks"),
    prevent_initial_call=True
)
def signupredir(n):
    return dcc.Location(pathname='SignUp', id="sid")


@app.callback(
    Output("hidden_div_for_callback", "children"),
    Input("submit_val", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
    prevent_initial_call=True,
)
def log_in(n_clicks, username, password):
    r = rq.post(f"{AUTH}auth/token/login/", data={"username": username, "password": password}).json()
    print(r)
    if "auth_token" in r:
        r = rq.get(f"{AUTH}auth/users/me/", headers={"Authorization": f"Token {r['auth_token']}"}).json()
        return dcc.Location(pathname=f"Logging/{r['id']}", id="someid_doesnt_matter")
    else:
        return no_update
