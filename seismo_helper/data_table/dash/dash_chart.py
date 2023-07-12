from dash import Dash, dcc, html, Input, Output
from backend.models import Trace
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
import requests as rq
from data_table.dash.Pageblank import navbar, footer, stylesheets
import dash_bootstrap_components as dbc
from seismo_helper.settings import ALLOWED_HOSTS

app = DjangoDash('Chart', external_stylesheets=stylesheets)

app.layout = html.Div([
    navbar,
    html.H1('Сейсмотрасса'),
    dcc.Graph(id="graph"),
    dcc.Input(id='id_event', type='hidden', value=''),
    footer
    ]
)
DATABASE_API = f'http://{ALLOWED_HOSTS[0]}:8000/api/'


@app.callback(
    Output("graph", "figure"),
    Input('id_event', 'value')
)
def update_line_chart(value):
    colors = [
        'rgb(255,0,0)',
        'rgb(0,255,0)',
        'rgb(0,0,255)'
    ]
    data = rq.get(f'{DATABASE_API}traces/?event={value}').json()['results']
    fig = make_subplots(rows=len(data), cols=1, shared_xaxes=True, shared_yaxes=True)
    for n, i in enumerate(data):
        for color, j in enumerate(i['channels']):
            d = np.load(i['path'] + j)
            fig.add_trace(go.Scatter(x=[i for i in range(0, len(d) * 5, 5)], y=d,
                                     mode='lines',
                                     name=j.split('.')[0],
                                     fillcolor=colors[color]
                                     ),
                          col=1,
                          row=n + 1
                          )
            fig.update_yaxes(title_text=i['station'], col=1, row=n + 1)
    fig.update_layout(height=356 * len(data))
    return fig
