from dash import html, dcc, no_update
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
from data_table.dash.Pageblank import footer, navbar, stylesheets
from dash.dependencies import Output, Input, State
import requests as rq

AUTH = "http://127.0.0.1:8000/"
app = DjangoDash("SignUpPage", external_stylesheets=stylesheets)

app.layout = html.Div([
    navbar,
    html.H1('Регистрация',
            style={'margin-top': '10%',
                'text-align': 'center',
                'font-size': '25px'}),
    html.Div([
        dbc.Col([
            dbc.Row(dcc.Input(id='username', placeholder='Имя пользователя', type='text'), style={'margin-top': '1%'}),
            dbc.Row(dcc.Input(id='email', placeholder='Почта', type='email'), style={'margin-top': '1%'}),
            dbc.Row(dcc.Input(id='password', placeholder='Пароль', type='password'), style={'margin-top': '1%'}),
            dbc.Row(html.Button('Регистрация', id='submit_val', n_clicks=0),
                    style={'margin-top': '1%'}),
            dbc.Row(html.Button('Войти', id='signinbutton', n_clicks=0),
                    style={'margin-right': 'auto',
                           'text-align': 'center',
                           'margin-left': 'auto',
                           'margin-top': '5%',
                           'width': '60%'}),
        ])], style={'margin-right': 'auto',
                    'margin-left': 'auto',
                    'width': '20%'}),
    dcc.Store(id="session", data=''),
    html.Div(id="hidden_div_for_callback"),
    html.Div(id="redirdiv"),
    footer
])


@app.callback(
    Output("redirdiv", "children"),
    Input("signinbutton", "n_clicks"),
    prevent_initial_call=True
)
def signupredir(n):
    return dcc.Location(pathname='Login', id="sid")


@app.callback(
    Output("hidden_div_for_callback", "children"),
    Input('submit_val', 'n_clicks'),
    State('username', 'value'),
    State('email', 'value'),
    State('password', 'value'),
    State('session', 'data'),
    prevent_initial_call=True,
)
def register(clicks, username, email, password, data):
    stuff = {"email": "Адрес электронной почты",
             "Enter a valid email address.": "Введите корректный адрес",
             "password": "Пароль",
             "This password is too short. It must contain at least 8 characters.": "Минимальная длина пароля -- 8 симаолов",
             "This password is entirely numeric.": "В пароле должны быть не только цифры!",
             'user with this email address already exists.': "Почта занята!"}
    print(data)
    r = rq.post(f"{AUTH}auth/users/", data={
        "username": username,
        "email": email,
        "password": password
    }
    )
    print(r.content)
    if r.status_code == 400:
        text = ''
        for i in r.json():
            try:
                text += f"{stuff[i]}: {stuff[r.json()[i][0]]}\n"
            except:
                text += i + "; "
        return text
    r = rq.post(f"{AUTH}auth/token/login/", data={"username": username, "password": password}).json()
    if "auth_token" in r:
        r = rq.get(f"{AUTH}auth/users/me/", headers={"Authorization": f"Token {r['auth_token']}"}).json()
        return dcc.Location(pathname=f"Logging/{r['id']}", id="someid_doesnt_matter")
    else:
        return no_update
