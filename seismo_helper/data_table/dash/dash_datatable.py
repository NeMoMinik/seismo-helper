from dash import html, dcc, no_update, Dash, dash_table, callback
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State 
from django.db.models import Count
import pandas as pd
from backend.models import Event
import plotly.express as px

app = DjangoDash('DashDatatable')

vv = Event.objects.all().values('id', 'location__name', 'time', 'x', 'y', 'z', 'magnitude')
S = [[],[],[],[],[],[],[]]
for i in vv:
    S[0].append(i['id'])
    S[1].append(i['location__name'])
    S[2].append(i['time'])
    S[3].append(i['x'])
    S[4].append(i['y'])
    S[5].append(i['z'])
    S[6].append(i['magnitude'])
df = pd.DataFrame(S).T.sort_values(0)
table_columns  = [
    {
        'id': '0',
        'name': '№',
        'sortable': True,
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
fig = px.scatter_mapbox(mdf, lat = 'X', lon = 'Y', size = Size,
                        color = 'Магнитуда', color_continuous_scale = 'plasma',
                          zoom = 3, mapbox_style = 'open-street-map')
fig.update_layout(height=600)

non_sortable_column_ids = [col['id'] for col in table_columns if col.pop('sortable') is False]

table_css = [
    {
        'selector': f'th[data-dash-column="{col}"] span.column-header--sort',
        'rule': 'display: none',
    }
    for col in non_sortable_column_ids
]
app.layout = html.Div([
    dcc.Dropdown(['Все']+ list(set([x for x in mdf['Локация']])), 'Все', id='loc-dropdown'),
    dcc.Graph(figure=fig),
    dash_table.DataTable(
        id='datatable-interactivity',
            columns=table_columns,
        css=table_css,
        data=df.to_dict('records'),
        sort_action="native",
        sort_mode="single",
        style_cell={'textAlign': 'center'},
    ),
    html.Div(id='datatable-interactivity-container')
])


@callback(
    Input('loc-dropdown', 'value'),
)
def update_output(value):
    S = []
    for i in vv:
        if(i['location__name'] == value or value == 'Все'):
            S[0].append(i['id'])
            S[1].append(i['location__name'])
            S[2].append(i['time'])
            S[3].append(i['x'])
            S[4].append(i['y'])
            S[5].append(i['z'])
            S[6].append(i['magnitude'])
    df = pd.DataFrame(S).T.sort_values(0)
    df.columns = ['№','Локация','Время','X','Y','Z','Магнитуда']
    Size = [df[6][i] for i in range(len(df[6]))]
    fig = px.scatter_mapbox(df, lat = 3, lon = 4, size = Size,
                        color = 6, color_continuous_scale = 'plasma',
                          zoom = 3, mapbox_style = 'open-street-map')       