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
    fig = make_subplots(rows=len(data), cols=1)
    for n, i in enumerate(data):
          # go.Figure()
        print(i)
        for j in i.channels.all():
            print(n, j.path)
            d = np.load(i.path + j.path)
            fig.add_trace(go.Scatter(x=[i for i in range(len(d))], y=d,
                                     mode='lines',
                                     name=j.path), col=1, row=n + 1)
        # fig.add_trace(go.Scatter(d[6], mode="lines", name='N'))
        # fig.update_layout(yaxis_title=i.station.name, xaxis_title='time', title="magnitude trace")
        # fig.
    return fig
