from dash import dcc, html, Input, Output, State
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
import requests as rq
from data_table.dash.Pageblank import navbar, footer, stylesheets
from seismo_helper.settings import ALLOWED_HOSTS, DATABASE_API

app = DjangoDash('Chart', external_stylesheets=stylesheets)

app.layout = html.Div([
    navbar,
    html.H1('Сейсмотрасса'),
    html.Div(dcc.Graph(id="graph"),style={'margin-bottom':'10%'}),
    dcc.Input(id='id_event', type='hidden', value=''),
    dcc.Store(id='session', data=''),
    footer
])


@app.callback(
    Output("graph", "figure"),
    Input('id_event', 'value'),
    State('session', 'data')
)
def update_line_chart(value, token):
    colors = [  # https://colorscheme.ru/#4f52Pw0w0w0w0
        '#6C48D7',
        '#FF4540',
        '#39E444'
    ]

    traces_requested = rq.get(f'{DATABASE_API}traces/?event={value}', headers={"Authorization": f"Token {token}"}).json()['results']
    fig = make_subplots(rows=len(traces_requested), cols=1, shared_xaxes=True, shared_yaxes=True)
    for n, i in enumerate(traces_requested):
        for color, j in enumerate(i['channels']):
            d = np.load(i['path'] + j)
            fig.add_trace(go.Scatter(x=[i for i in range(0, len(d) * 5, 5)],
                                     y=d,
                                     mode='lines',
                                     name=j.split('.')[0],
                                     line=dict(color=colors[color])
                                     ),
                          col=1,
                          row=n + 1
                          )
            fig.update_yaxes(title_text=i['station'], col=1, row=n + 1)
    fig.update_layout(height=356 * len(traces_requested))
    return fig
