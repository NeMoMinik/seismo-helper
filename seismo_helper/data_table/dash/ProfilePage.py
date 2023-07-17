from dash import html, dcc, no_update
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from data_table.dash.Pageblank import footer, navbar, stylesheets
from dash.dependencies import Output, Input, State
import requests as rq
from seismo_helper.settings import ALLOWED_HOSTS

app = DjangoDash('ProfilePage', external_stylesheets=stylesheets)
global profile_data
app.layout = html.Div([
    navbar,
    html.H2('Ваш профиль', style={'margin-right': 'auto', 'margin-left': 'auto'}),
    html.Div(id='usrn', style={'margin-right': 'auto', 'margin-left': 'auto', 'width': '20%'}, children=[]),
    dcc.Store(id="session", data=None),
    dbc.Row(html.Button("Редактировать", id="edit"), style={'margin-top':'1%', 'margin-right': 'auto', 'margin-left': 'auto', 'width': '20%'},),
    html.Div(id="q", style={'margin-right': 'auto', 'margin-left': 'auto', 'width': '20%'}, children=[html.Div(id="q2")]),
    html.Div(id="hidden_div_for_callback"),
    footer
])


@app.callback(
    Output('usrn', 'children'),
    Input('session', 'data')
)
def load_profile(aboba):
    style = {'margin-top': '1%', 'color': '#000000'}
    if aboba is not None:
        data = rq.get(f'http://{ALLOWED_HOSTS[0]}:8000/auth/users/me',
                      headers={'Authorization': 'Token ' + aboba}).json()
        global profile_data
        profile_data = data
        print(data)
        return dbc.Col([
            dbc.Row(html.P(data['username']), id="username", style=style),
            dbc.Row(html.P(data['email']), id="email",  style=style),
            dbc.Row(html.P(data['first_name']), id="first_name", style=style),
            dbc.Row(html.P(data['second_name']), id="second_name", style=style),
            dbc.Row(html.P(data['third_name']), id="third_name", style=style),
            dbc.Row(html.P(data['bio']), id="bio", style=style),
            dbc.Row(html.P(data['corporation']), id='corp', style=style),
            dbc.Row(html.Button("Редактировать", id="edit"), style={'margin-top': '1%'}),
            dcc.Store('id', data=data['id'])]
        )
    else:
        return dcc.Location(pathname=f"Login/", id="someid_doesnt_matter")


@app.callback(
    Output('q2', 'children'),
    Input("edit", "n_clicks"), prevent_initial_call=True)
def edit_profile(n):
    global profile_data
    data = profile_data
    return [dbc.Row(dcc.Input(id="username", value=data['username'], maxLength=150, disabled=True), style={'margin-top': '1%'}),
            dbc.Row(dcc.Input(id="email", value=data['email'], maxLength=150, disabled=True), style={'margin-top': '1%'}),
            dbc.Row(dcc.Input(id="first_name", value=data['first_name'], maxLength=150, placeholder="Имя"), style={'margin-top': '1%'}),
            dbc.Row(dcc.Input(id="second_name", value=data['second_name'], maxLength=150, placeholder="Фамилия"), style={'margin-top': '1%'}),
            dbc.Row(dcc.Input(id="third_name", value=data['third_name'], maxLength=150, placeholder="Отчество"), style={'margin-top': '1%'}),
            dbc.Row(dcc.Input(id="bio", value=data['bio'], maxLength=512, placeholder="Описание"), style={'margin-top': '1%'}),
            dbc.Row(dcc.Input(id='corp', value=data['corporation'], placeholder="Нет корпорации", disabled=True), style={'margin-top': '1%'}),
            dbc.Row(html.Button("Сохранить", id="save"), style={'margin-top': '1%'})]


@app.callback(
    Output("q", 'children'),
    Input("save", "n_clicks"),
    State('id', 'data'),
    State('session', 'data'),
    State('first_name', 'value'),
    State('second_name', 'value'),
    State('third_name', 'value'),
    State('bio', 'value'), prevent_initial_call=True
)
def update_profile(n, user_id, token, *dat):
    d = {
        'first_name': '',
        'second_name': '',
        'third_name': '',
        'bio': '',
    }
    for i, j in zip(list(d.keys()), dat):
        if j:
            d[i] = j
        else:
            d.pop(i)
    if len(d):
        r = rq.patch(f'http://{ALLOWED_HOSTS[0]}:8000/auth/users/{user_id}/', headers=token, data=d)
        print(r.content)
        return no_update