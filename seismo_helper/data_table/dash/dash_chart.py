from dash import Dash, dcc, html, Input, Output
from backend.models import Trace
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
import requests as rq


app = DjangoDash('Chart')

app.layout = html.Div([
    dcc.Graph(id="graph"),
    dcc.Input(id='id_event', type='hidden', value='')]
)
DATABASE_API = 'http://127.0.0.1:8000/api/'


@app.callback(
    Output("graph", "figure"),
    Input('id_event', 'value')
)
def update_line_chart(value):
    data = list(filter(lambda x: x['event'] == value, rq.get(DATABASE_API + 'traces/').json()['results']))
    fig = make_subplots(rows=len(data), cols=1, shared_xaxes=True, shared_yaxes=True)
    for n, i in enumerate(data):
        for j in i['channels']:
            print(n, j)
            d = np.load(i['path'] + j)
            fig.add_trace(go.Scatter(x=[i for i in range(0, len(d) * 5, 5)], y=d,
                                     mode='lines',
                                     name=j.split('.')[0]
                                     ),
                          col=1,
                          row=n + 1
                          )
            fig.update_yaxes(title_text=i['station'], col=1, row=n + 1)
    return fig
