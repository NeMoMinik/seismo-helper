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
    html.Div(dcc.Graph(id="graph"), style={'margin-bottom':'10%'}),
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

    traces_requested = rq.get(f'{DATABASE_API}traces/?event={value}', headers=token).json()['results']
    fig = make_subplots(rows=len(traces_requested), cols=1, shared_xaxes=True, shared_yaxes=True)
    for n, i in enumerate(traces_requested):
        st = rq.get(f"{DATABASE_API}stations/{i['station']}/", headers=token).json()['name']
        for color, j in enumerate(i['channels']):
            d = np.load(i['path'] + j)
            fig.add_trace(go.Scatter(x=[i for i in range(0, len(d) * i["timedelta"], i["timedelta"])],
                                     y=d,
                                     mode='lines',
                                     name=j.split('.')[0],
                                     line=dict(color=colors[color])
                                     ),
                          col=1,
                          row=n + 1
                          )
            fig.update_yaxes(title_text=st, col=1, row=n + 1)
        if i["p_peak"] is not None:
            fig.add_trace(go.Scatter(x=[i["p_peak"] * i["timedelta"]],
                                     y=[d[i["p_peak"]]],
                                     mode='markers',
                                     marker_symbol='cross-dot',  # https://plotly.com/python/marker-style/
                                        marker_line_color="black", marker_color="orange",
                                        marker_line_width=2, marker_size=15,
                                        hovertemplate="name: %{y}%{x}<br>number: %{marker.symbol}<extra></extra>",
                                     name="P PEAK"
                                     ),
                          col=1,
                          row=n + 1
                          )
        if i["s_peak"] is not None:
            fig.add_trace(go.Scatter(x=[i["s_peak"] * i["timedelta"]],
                                     y=[d[i["s_peak"]]],
                                     mode='markers',
                                     marker_symbol='x-dot',
                                        marker_line_color="black", marker_color="orange",
                                        marker_line_width=2, marker_size=15,
                                        hovertemplate="name: %{y}%{x}<br>number: %{marker.symbol}<extra></extra>",
                                     name="S PEAK"
                                     ),
                          col=1,
                          row=n + 1
                          )
    fig.update_layout(height=356 * len(traces_requested))
    return fig
