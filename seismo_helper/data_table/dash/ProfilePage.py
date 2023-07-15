from dash import html, dcc, no_update
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from data_table.dash.Pageblank import footer, navbar, stylesheets
from dash.dependencies import Output, Input, State
import requests as rq
from seismo_helper.settings import ALLOWED_HOSTS

app = DjangoDash('ProfilePage', external_stylesheets=stylesheets)

app.layout = html.Div([
    navbar,
    html.H2('Ваш профиль'),
    html.Div(id='usrn', style={'margin-right': 'auto', 'margin-left': 'auto', 'width': '20%'}, children=[]),
    dcc.Store(id="session", data=None),
    html.Div(id="hidden_div_for_callback"),
    footer
])


@app.callback(
    Output('usrn', 'children'),
    Input('session', 'data'),
)
def load_profile(aboba):
    if aboba is not None:
        data = rq.get(f'http://{ALLOWED_HOSTS[0]}:8000/auth/users/me',
                      headers={'Authorization': 'Token ' + aboba}).json()
        print(data)
        return dbc.Col([
            dbc.Row(dcc.Input(id="username", value=data['username'], maxLength=150, disabled=True), style={'margin-top': '1%'}),
            dbc.Row(dcc.Input(id="email", value=data['email'], maxLength=150, disabled=True), style={'margin-top': '1%'}),
            dbc.Row(dcc.Input(id="first_name", value=data['first_name'], maxLength=150, placeholder="Имя"), style={'margin-top': '1%'}),
            dbc.Row(dcc.Input(id="second_name", value=data['second_name'], maxLength=150, placeholder="Фамилия"), style={'margin-top': '1%'}),
            dbc.Row(dcc.Input(id="third_name", value=data['third_name'], maxLength=150, placeholder="Отчество"), style={'margin-top': '1%'}),
            dbc.Row(dcc.Input(id="bio", value=data['bio'], maxLength=512, placeholder="Описание"), style={'margin-top': '1%'}),
            dbc.Row(dcc.Input(id='corp', value=data['corporation'], placeholder="Нет корпорации", disabled=True), style={'margin-top': '1%'}),
            dbc.Row(html.Button("Сохранить", id="save"), style={'margin-top': '1%'}),
            dcc.Store('id', data=data['id'])]
        )
    else:
        return dcc.Location(pathname=f"Login/", id="someid_doesnt_matter")


@app.callback(
    Output("hidden_div_for_callback", 'children'),
    Input("save", "n_clicks"),
    State('id', 'data'),
    State('session', 'data'),
    State('first_name', 'value'),
    State('second_name', 'value'),
    State('third_name', 'value'),
    State('bio', 'value'),
)
def update_profile(n, user_id, aboba, *dat):
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
        r = rq.patch(f'http://{ALLOWED_HOSTS[0]}:8000/auth/users/{user_id}/', headers={'Authorization': 'Token ' + aboba}, data=d)
        print(r.content)
        return no_update
