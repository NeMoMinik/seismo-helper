from dash import html, dcc
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from data_table.dash.Pageblank import footer, navbar, stylesheets
from dash.dependencies import Output, Input, State
import requests as rq
from seismo_helper.settings import ALLOWED_HOSTS


app = DjangoDash('ProfilePage',external_stylesheets=stylesheets)

app.layout = html.Div([
    navbar,
    html.H2('Ваш профиль'),
    html.Div(id='usrn', children=[]),
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
        data = rq.get(f'http://{ALLOWED_HOSTS[0]}:8000/auth/users/me', headers={'Authorization': 'Token ' + aboba}).json()
        print(data)
        return [dcc.Input(id="username", value=data['username']), dcc.Input(id="email", value=data['email'], disabled=True), dbc.Button(title="сменить почту", ), str(data)]
    else:
        return dcc.Location(pathname=f"Login/", id="someid_doesnt_matter")
