from dash import html, dcc, dash_table, no_update
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import pandas as pd
import plotly.express as px
from data_table.dash.Pageblank import footer, navbar
import base64
import os
import requests as rq
from seismo_helper.settings import ALLOWED_HOSTS
from django.shortcuts import render
from plotly.subplots import make_subplots
import numpy as np
from sklearn.linear_model import LinearRegression


global vv
global mdf
external_stylesheets_downl = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
UPLOAD_DIRECTORY = os.getcwd() + "\\media\\"

app = DjangoDash('DashDatatable', external_stylesheets=[dbc.themes.LUMEN, external_stylesheets_downl])
DATABASE_API = f'http://{ALLOWED_HOSTS[0]}:8000/api/'
BASE_LINK = f'http://{ALLOWED_HOSTS[0]}:8000/Events/'

table_columns = [
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
        'name': 'Начало',
        'sortable': True,
    },
    {
        'id': '3',
        'name': 'Конец',
        'sortable': True,
    },
    {
        'id': '4',
        'name': 'X',
        'sortable': False,
    },
    {
        'id': '5',
        'name': 'Y',
        'sortable': False,
    },
    {
        'id': '6',
        'name': 'Z',
        'sortable': False,
    },
    {
        'id': '7',
        'name': 'Магнитуда',
        'sortable': True,
    }
]
non_sortable_column_ids = [col['id'] for col in table_columns if col.pop('sortable') is False]
table_css = [
    {
        'selector': f'th[data-dash-column="{col}"] span.column-header--sort',
        'rule': 'display: none',
        'textAlign': 'center'
    }
    for col in non_sortable_column_ids
]


fig = go.Figure()

app.layout = html.Div(
    [navbar, html.Div(id="page-content", children=[dcc.Dropdown(['Все'], 'Все', id='loc-dropdown'), dcc.Graph(figure=fig, id='mapD'),]),html.Div(id="redirDiv"), footer]
)


@app.callback(Output('store', 'data'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_outputfile(contents, list_of_names, list_of_dates):
    if contents is None:
        return None
    with open(UPLOAD_DIRECTORY + list_of_names, "wb") as fh:
        data = contents.encode("utf8").split(b";base64,")[1]
        fh.write(base64.decodebytes(data))


@app.callback(Output("redirDiv", "children"),
              Input('mapD', 'clickData'))
def update_contents(clickData):
    if clickData:
        event_id = clickData['points'][0]['customdata'][0]
        link = f'Events/{event_id}'
        return dcc.Location(pathname=link, id="sid")

# UPDATE    

@app.callback(
    Output('page-content', 'children'),
    Input('loc-dropdown', 'value')
)
def update_output(value):
    global vv, mdf
    vv = rq.get(DATABASE_API + 'events/').json()['results']

    station_coords = rq.get(DATABASE_API + 'stations/').json()['results']
    
    site_lat = []
    site_lon = []
    for i in station_coords:
        site_lat.append(i['x'])
        site_lon.append(i['y'])

    MTGrapg = []
    W = [[], [], [], [], [], [], [], [], []]
    for i in vv:
        if i['location'] == value or value == 'Все':
            W[0].append(f"[{i['id']}]({BASE_LINK}{i['id']})")
            W[1].append(i['location'])
            W[2].append(i['start'])
            W[3].append(i['end'])
            W[4].append(i['x'])
            W[5].append(i['y'])
            W[6].append(i['z'])
            W[7].append(i['magnitude'])
            W[8].append(i['id'])
            MTGrapg.append({'Time':i['start'], 'Magnitude':i['magnitude']})

    mdf = pd.DataFrame(W).T.sort_values(0)
    df = pd.DataFrame(W[:8]).T.sort_values(0)
    Size = [W[7][i] for i in range(len(W[7]))]
    mdf.columns = ['№', 'Локация', 'Начало', 'Конец', 'X', 'Y', 'Z', 'Магнитуда', 'id']
    fig = go.Figure()

    fig.add_traces(list(px.scatter_mapbox(mdf, lat='Y', lon='X', size=Size, hover_data="id",
                                          color='Магнитуда', color_continuous_scale=px.colors.cyclical.IceFire).select_traces()))

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
    fig.update_layout(height=500, margin={"r": 0, "t": 0, "l": 0, "b": 0})


    pxMagTimeGraph = px.line(MTGrapg, x="Time", y="Magnitude", title="Магнитуда от времени")
    pxMagTimeGraph.update_traces(mode="markers", hovertemplate=None)

    MagCount = [0 for _ in range(100)]
    MagCountdf = []
    for i in range(len(W[0])):
        MagCount[int(W[7][i]*100 // 10)] += 1
    MagCountX = []
    MagCountY = []
    for i in range(100):
        if(MagCount[i]!= 0):
            MagCountdf.append({'Magnitude': i/10, 'Count':MagCount[i]})
            MagCountX.append(i/10)
            MagCountY.append(MagCount[i])
    MCdf = pd.DataFrame(MagCount)
    MagCountX = np.array(MagCountX)
    MagCountX = MagCountX.reshape(-1, 1)

    model = LinearRegression()
    model.fit(MagCountX, MagCountY)
    x_range = np.linspace(MagCountX.min(), MagCountX.max(), 100)
    y_range = model.predict(x_range.reshape(-1, 1))

    pxMagCountGrapf = px.scatter(MagCountdf, x="Magnitude", y="Count", title="Количество от магнитуды")
    pxMagCountGrapf.add_traces(go.Scatter(x=x_range, y=y_range, name='Тренд'))
    
    divs_children = [
        html.Div(dbc.NavItem(dbc.NavLink("Добавить станции", href=f'http://{ALLOWED_HOSTS[0]}:8000/Stations/', target='_blank', style={'color':'Black','width': '100%',
                'height': '40px','lineHeight': '40px','borderWidth': '1px','borderStyle': 'dashed','borderRadius': '5px','textAlign': 'center','vertical-align': 'middle','margin': '10px'})),
                 style={'width': '15%', 'display': 'inline-block', 'float': 'left', 'textAlign': 'center','margin-right':'15px'}),
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
        ), style={'width': '40%', 'display': 'inline-block'}),
        html.Div(dcc.Dropdown(['Все'] + list(set([x for x in mdf['Локация']])), value, id='loc-dropdown'),
                 style={'width': '40%', 'display': 'inline-block', 'float': 'right', 'textAlign': 'center',
                        'margin': '12px', 'height': '40px'}),


        html.Div(dcc.Graph(figure=fig, id='mapD')), 
        html.Div(dcc.Graph(id="MagTimeGraph", figure=pxMagTimeGraph),
            style={'width': '50%', 'display': 'inline-block', 'float': 'left'}),
        html.Div(dcc.Graph(id="MagCountGrapf", figure=pxMagCountGrapf),
            style={'width': '50%', 'display': 'inline-block', 'float': 'right'}),

        dash_table.DataTable(
            id='datatable-interactivity',
            columns=table_columns,
            css=[{"selector": "p", "rule": "text-Align: center"}] + [
                {'selector': f'th[data-dash-column="{col}"] span.column-header--sort', 'rule': 'display: none',
                 'textAlign': 'center'} for col in non_sortable_column_ids],
            data=df.to_dict('records'),
            sort_action="native",
            sort_mode="single",
            style_cell={'textAlign': 'center'},
        ),
        dcc.Store(id='store'),
        html.Div(id='contents'),
    ]
    
    return divs_children
