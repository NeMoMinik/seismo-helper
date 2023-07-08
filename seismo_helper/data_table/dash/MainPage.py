from dash import html, dcc, no_update, Dash, dash_table, callback
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State 
from django.db.models import Count
import pandas as pd
from backend.models import Event, Station
import plotly.express as px
import dash_mantine_components as dmc
from data_table.dash.Pageblank import footer, navbar
import base64
import os
from urllib.parse import quote as urlquote
from flask import Flask 
import io

external_stylesheets_downl = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
UPLOAD_DIRECTORY = os.getcwd() + "\\media\\"

app = DjangoDash('DashDatatable',external_stylesheets=[dbc.themes.BOOTSTRAP, external_stylesheets_downl])

BASE_LINK = 'http://127.0.0.1:8000/Events/'
vv = Event.objects.all().values('id', 'location__name', 'time', 'x', 'y', 'z', 'magnitude')
z = 1
S = [[],[],[],[],[],[],[]]
for i in vv:
    S[0].append('[' + str(i['id']) + ']' + '(' + BASE_LINK + str(z) + ')')
    S[1].append(i['location__name'])
    S[2].append(i['time'])
    S[3].append(i['x'])
    S[4].append(i['y'])
    S[5].append(i['z'])
    S[6].append(i['magnitude'])
    z += 1
df = pd.DataFrame(S).T.sort_values(0)
table_columns  = [
    {
        'id': '0',
        'name': '№',
        'sortable': True,
        'presentation': 'markdown',
        'textAlign': 'center'
    },
    {
        'id': '1',
        'name': 'Локация',
        'sortable': True,
    },
    {
        'id': '2',
        'name': 'Время',
        'sortable': True,
    },
    {
        'id': '3',
        'name': 'X',
        'sortable': False,
    },
    {
        'id': '4',
        'name': 'Y',
        'sortable': False,
    },
    {
        'id': '5',
        'name': 'Z',
        'sortable': False,
    },
    {
        'id': '6',
        'name': 'Магнитуда',
        'sortable': True,
    }
]


mdf = df.copy()
Size = [df[6][i] for i in range(len(df[6]))]
mdf.columns = ['№','Локация','Время','X','Y','Z','Магнитуда']

station_coords = Station.objects.all().values('x', 'y')
site_lat = []
site_lon = []
for i in station_coords:
    site_lat.append(i['x'])
    site_lon.append(i['y'])

fig = go.Figure()

fig.add_traces((go.Scattermapbox(
        lat=site_lon,
        lon=site_lat,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=15,
            color='rgb(0, 255, 0)',
            opacity=1
        ),
    )))

fig.add_traces(list(px.scatter_mapbox(mdf, lat = 'Y', lon = 'X', size = Size,
                        color = 'Магнитуда', color_continuous_scale = 'plasma').select_traces()))



fig.update_layout(mapbox_style="open-street-map",
                  mapbox_zoom=3)

fig.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0})

#DATATABLE


non_sortable_column_ids = [col['id'] for col in table_columns if col.pop('sortable') is False]

table_css = [
    {
        'selector': f'th[data-dash-column="{col}"] span.column-header--sort',
        'rule': 'display: none',
        'textAlign': 'center'
    }
    for col in non_sortable_column_ids
]
app.layout = html.Div([
    navbar,
    html.Div(dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Miniseed Files')
        ]),
        style={
            'width': '100%',
            'height': '40px',
            'lineHeight': '40px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
            'vertical-align': 'middle'
        },
        multiple=False
    ),style={'width': '49%', 'display': 'inline-block'}),
    html.Div(dcc.Dropdown(['Все']+ list(set([x for x in mdf['Локация']])), 'Все', id='loc-dropdown'),style={'width': '45%', 'display': 'inline-block', 'float':'right', 'textAlign': 'center', 'margin': '10px','height': '40px'}),
    dcc.Graph(figure=fig, id='mapD'),
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=table_columns,
        css=[{"selector": "p", "rule": "text-Align: center"}],
        data=df.to_dict('records'),
        sort_action="native",
        sort_mode="single",
        style_cell={'textAlign': 'center'},
    ),
    dcc.Store(id='store'),
    footer
])


@app.callback(Output('store', 'data'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(contents, list_of_names, list_of_dates):
    if contents is None:
        return None
    with open(UPLOAD_DIRECTORY + list_of_names, "wb") as fh:
        data = contents.encode("utf8").split(b";base64,")[1]
        fh.write(base64.decodebytes(data))



#UPDATE

@app.callback(
    Output('mapD', 'figure'),
    Input('loc-dropdown', 'value'),
)
def update_output(value):
    W = [[],[],[],[],[],[],[]]
    for i in vv:
        if(i['location__name'] == value or value == 'Все'):
            W[0].append(i['id'])
            W[1].append(i['location__name'])
            W[2].append(i['time'])
            W[3].append(i['x'])
            W[4].append(i['y'])
            W[5].append(i['z'])
            W[6].append(i['magnitude'])
    mdf = pd.DataFrame(W).T.sort_values(0)
    Size = [W[6][i] for i in range(len(W[6]))]
    mdf.columns = ['№','Локация','Время','X','Y','Z','Магнитуда']


    fig = go.Figure()
    fig.add_traces(list(px.scatter_mapbox(mdf, lat = 'Y', lon = 'X', size = Size,
                        color = 'Магнитуда', color_continuous_scale = 'plasma').select_traces()))
    
    fig.add_traces((go.Scattermapbox(
        lat=site_lon,
        lon=site_lat,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=15,
            color='rgb(0, 255, 0)',
            opacity=1
        ),
        hoverinfo='none'
    )))

    fig.update_layout(mapbox_style="open-street-map",
                  mapbox_zoom=3)

    fig.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0})
    return fig