from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from backend.models import Trace
from django_plotly_dash import DjangoDash
import scipy.io as sio
import pandas
import plotly.graph_objects as go

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
    data = Trace.objects.filter(event__id=value)
    print(data)
    for i in data:
        d = sio.loadmat(i.path)
        d = d['seismology'][0][0][-1].T

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[i for i in range(len(d[5]))], y=d[5],
                                 mode='lines',
                                 name='S'))
        fig.add_trace(go.Scatter(x=[i for i in range(len(d[6]))], y=d[6],
                                 mode='lines',
                                 name='N'))
        fig.add_trace(go.Scatter(x=[i for i in range(len(d[7]))], y=d[7],
                                 mode='lines',
                                 name='E'))
        # fig.add_trace(go.Scatter(d[6], mode="lines", name='N'))
        fig.update_layout(yaxis_title=i.station.name, xaxis_title='time', title="magnitude trace")
    return fig
