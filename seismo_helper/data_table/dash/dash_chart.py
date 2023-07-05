from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from backend.models import Trace
from django_plotly_dash import DjangoDash
import scipy.io as sio

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
        d = d[5]
        fig = px.line(d)
    return fig
