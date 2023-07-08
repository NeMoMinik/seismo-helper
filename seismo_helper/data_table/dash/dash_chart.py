from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from backend.models import Trace
from django_plotly_dash import DjangoDash
import scipy.io as sio
import pandas
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

app = DjangoDash('Chart')

app.layout = html.Div([
    dcc.Graph(id="graph"),
    dcc.Input(id='id_event', type='hidden', value='')]
)


@app.callback(
    Output("graph", "figure"),
    Input('id_event', 'value')
)
def update_line_chart(value):
    data = Trace.objects.filter(event__id=value).all()
    fig = make_subplots(rows=len(data), cols=1, shared_xaxes=True, shared_yaxes=True)
    for n, i in enumerate(data):
        for j in i.channels.all():
            print(n, j.path)
            d = np.load(i.path + j.path)
            fig.add_trace(go.Scatter(x=[i for i in range(0, len(d) * 5, 5)], y=d,
                                     mode='lines',
                                     name=j.path.split('.')[0]
                                     ),
                          col=1,
                          row=n + 1
                          )
            fig.update_yaxes(title_text=i.station.name, col=1, row=n + 1)
            # fig.update_xaxes(title_text="time", col=1, row=n + 1, )
    return fig
