from dash import html, dcc, dash_table, no_update
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import pandas as pd
import plotly.express as px
from data_table.dash.Pageblank import footer, navbar, stylesheets
import base64
import os
import requests as rq
from seismo_helper.settings import ALLOWED_HOSTS, DATABASE_API, BASE_LINK, UPLOAD_DIRECTORY
import numpy as np
from sklearn.linear_model import LinearRegression
from data_table.Upload_Miniseed import upload_miniseed

app = DjangoDash('DashDatatable', external_stylesheets=stylesheets)

table_columns = [  # Формат колонок для таблицы
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
    [
        navbar,
        html.Div(id='static-content', children=[
            dbc.Col(html.Div(dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Miniseed Files')
                ]),
                style={
                    'width': '95%',
                    'height': '40px',
                    'lineHeight': '40px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px',
                    'float': 'left0',
                    'vertical-align': 'middle'
                },
                multiple=True
            ))),
            dbc.Col(html.Div(
                dbc.NavItem(
                    dbc.NavLink("Добавить станции",
                                href=f'http://{ALLOWED_HOSTS[0]}:8000/Stations/',
                                target='_blank',
                                style={'color': 'Black', 'width': '100%',
                                       'height': '40px',
                                       'lineHeight': '40px',
                                       'borderWidth': '1px',
                                       'borderStyle': 'dashed',
                                       'borderRadius': '5px',
                                       'textAlign': 'center',
                                       'vertical-align': 'middle',
                                       'margin': '10px'})),
                style={'textAlign': 'center',
                       'margin-right': '15px'})),
        ],
                 ),
        html.Div(id="page-content", children=[
            dcc.Dropdown([{'label': 'Все локации', 'value': 'Все локации'}], 'Все локации', id='loc-dropdown'),
            dcc.Graph(figure=fig, id='mapD'), ], style={'margin-bottom': '10%'}),
        html.Div(id="redirDiv"),
        html.Div(id="redirDiv2"),
        dcc.Store(id='session', data=None),
        footer
    ]
)


@app.callback(Output('store', 'data'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'),
              State('loc-dropdown', 'value'),
              State('session', 'data')
              )
def update_outputfile(contents, list_of_names, list_of_dates, location, token):  # Функция, загружающая miniseed-файлы
    if contents is None or location == 'Все локации':
        return None
    if not os.path.exists(UPLOAD_DIRECTORY + str(location) + "\\"):
        os.makedirs(UPLOAD_DIRECTORY + str(location) + "\\")

    Paths = []
    for file_index in range(len(list_of_names)):
        if list_of_names[file_index][list_of_names[file_index].rfind('.'):] == '.miniseed':
            with open(UPLOAD_DIRECTORY + str(location) + "\\" + list_of_names[file_index], "wb") as miniseed_file:
                data = contents[file_index].encode("utf8").split(b";base64,")[1]
                miniseed_file.write(base64.decodebytes(data))
                Paths.append(UPLOAD_DIRECTORY + str(location) + "\\" + list_of_names[file_index])

    upload_miniseed(Paths, location, {"Authorization": f"Token {token}"})


@app.callback(Output("redirDiv", "children"),
              Input('mapD', 'clickData'))
def update_contents(clickdata):  # Функция для перехода с карты на страницу отдельного события
    if clickdata:
        event_id = clickdata['points'][0]['customdata'][0]
        link = f'Events/{event_id}'
        return dcc.Location(pathname=link, id="sid")


@app.callback(Output("redirDiv2", "children"),
              Input('MagTimeGraph', 'clickData'))
def redir_from_graph(clickdata):  # Функция для перехода с графика на страницу отдельного события
    if clickdata:
        event_id = clickdata['points'][0]['customdata'][0]
        link = f'Events/{event_id}'
        return dcc.Location(pathname=link, id="sid")


def update_map(requested_events=None, requested_stations=None, location=None):  # Обновление карты
    map_figure = go.Figure()
    map_figure.update_layout(mapbox_style="open-street-map", mapbox_zoom=3)
    map_figure.update_layout(height=500, margin={"r": 0, "t": 0, "l": 0, "b": 0})
    site_lat = [i['x'] for i in requested_stations]
    site_lon = [i['y'] for i in requested_stations]
    events_list_table = []
    for event in requested_events:
        if event['location'] == location or location == 'Все локации':
            if event['magnitude'] is not None:
                events_list_table.append([f"[{event['id']}]({BASE_LINK + 'Events/'}{event['id']})",
                                          event['location'],
                                          event['start'],
                                          event['end'],
                                          event['x'],
                                          event['y'],
                                          event['z'],
                                          event['magnitude'],
                                          event['id']])
    if len(events_list_table) != 0:
        print(events_list_table)
        map_df = pd.DataFrame(events_list_table)#.sort_values(0)

        markers_size_list = [event[7] for event in events_list_table if event[7] is not None]
        map_df.columns = ['№', 'Локация', 'Начало', 'Конец', 'X', 'Y', 'Z', 'Магнитуда', 'id']

        map_figure.add_traces(list(px.scatter_mapbox(map_df,
                                                     lat='Y',
                                                     lon='X',
                                                     size=markers_size_list,
                                                     hover_data="id",
                                                     color='Магнитуда',
                                                     color_continuous_scale=px.colors.cyclical.IceFire).select_traces()))

        map_figure.add_traces((go.Scattermapbox(
            lat=site_lon,
            lon=site_lat,
            name='Станции',
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=15,
                color='rgb(0, 255, 0)',
                opacity=1
            ),
            hoverinfo='none'
        )))

    return map_figure


def create_magnitude_graphs(events_list):
    magnitude_time_graph_df = [{'Time': i['start'], 'Magnitude': i['magnitude'], 'id': i['id']} for i in events_list]
    magnitude_time_graph = px.line(magnitude_time_graph_df, x="Time", y="Magnitude", hover_data="id",
                                   title="Магнитуда от времени")
    events_list_graphs = [
        [f"[{i['id']}]({BASE_LINK + 'Events/'}{i['id']})", i['location'], i['start'], i['end'], i['x'], i['y'], i['z'],
         i['magnitude'], i['id']] for i in events_list]
    magnitude_time_graph.update_traces(mode="markers", hovertemplate=None)
    magnitude_count_list = [0 for _ in range(100)]
    magnitude_count_df = [{"Magnitude": None, "Count": None}]
    for event in events_list_graphs:
        if event[7]:
            magnitude_count_list[int(event[7] * 100 // 10)] += 1

    magnitudes_list = []
    magnitudes_count_list = []
    for i in range(100):
        if magnitude_count_list[i] != 0:
            magnitude_count_df.append({'Magnitude': i / 10, 'Count': magnitude_count_list[i]})
            magnitudes_list.append(i / 10)
            magnitudes_count_list.append(magnitude_count_list[i])
    magn_count_graph = px.scatter(magnitude_count_df, x="Magnitude", y="Count", title="Количество от магнитуды",
                                      log_y=True)
    magnitudes_list = np.array(magnitudes_list)
    magnitudes_list = magnitudes_list.reshape(-1, 1)
    print(magnitudes_list)
    if len(magnitudes_list) != 0:
        magn_count_trend = LinearRegression()
        magn_count_trend.fit(magnitudes_list, magnitudes_count_list)
        x_range = np.linspace(magnitudes_list.min(), magnitudes_list.max(), 100)
        y_range = magn_count_trend.predict(x_range.reshape(-1, 1))
        magn_count_graph.add_traces(go.Scatter(x=x_range, y=y_range, name='Тренд'))

    return dbc.Row([
        dbc.Col(dcc.Graph(id="MagTimeGraph", figure=magnitude_time_graph), style={'width': '50%'}),
        dbc.Col(dcc.Graph(id="MagCountGrapf", figure=magn_count_graph), style={'width': '50%'})
    ])


def create_datatable(events_list):
    events_list_graphs = [
        [f"[{i['id']}]({BASE_LINK + 'Events/'}{i['id']})", i['location'], i['start'], i['end'], i['x'], i['y'], i['z'],
         i['magnitude'], i['id']] for i in events_list]
    datatable_df = pd.DataFrame(events_list_graphs[:8]).sort_values(0)
    return dash_table.DataTable(
        id='datatable-interactivity',
        columns=table_columns,
        css=[{"selector": "p",
              "rule": "text-Align: center"}] + [
                {'selector': f'th[data-dash-column="{col}"] span.column-header--sort', 'rule': 'display: none',
                 'textAlign': 'center'} for col in non_sortable_column_ids],
        data=datatable_df.to_dict('records'),
        sort_action="native",
        sort_mode="single",
        style_cell={'textAlign': 'center'},
    )


def create_dropdown(locations_requested, value):
    locations_for_dropdown = [{'label': x['name'], 'value': x['id']} for x in locations_requested]
    locations_for_dropdown.insert(0, {'label': 'Все локации', 'value': 'Все локации'})
    print(locations_for_dropdown, value)
    return dbc.Row([
        dbc.Col(html.Div(
            dcc.Dropdown(options=locations_for_dropdown, value=value,
                         id='loc-dropdown'),
            style={'textAlign': 'center',
                   'margin': '12px',
                   'height': '40px'})),
    ])


@app.callback(
    Output('page-content', 'children'),
    Input('loc-dropdown', 'value'),
    State('session', 'data')
)
def update_output(value, token):  # Функция для обновления карты, графиков и таблицы
    # Запросы в базу данных:
    divs_children = []
    events_list = rq.get(DATABASE_API + 'events/', headers={"Authorization": f"Token {token}"}).json()['results']
    stations_list = rq.get(DATABASE_API + 'stations/', headers={"Authorization": f"Token {token}"}).json()['results']
    locations_requested = rq.get(DATABASE_API + 'locations/', headers={"Authorization": f"Token {token}"}).json()['results']
    print(locations_requested)
    if len(events_list) == 0 or len(stations_list) == 0:
        divs_children = [create_dropdown(locations_requested, value),
                         dcc.Store(id='store'),
                         html.Div(id='contents'),
                         ]
        return divs_children
    divs_children = [
        create_dropdown(locations_requested, value),
        html.Div(dcc.Graph(figure=update_map(events_list, stations_list, value), id='mapD')),
        create_datatable(events_list),
        create_magnitude_graphs(events_list),
        dcc.Store(id='store'),
        html.Div(id='contents'),
    ]
    return divs_children
