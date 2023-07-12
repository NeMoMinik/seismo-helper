from dash import html, dcc, no_update, Dash, dash_table, callback
from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import plotly.express as px
from data_table.dash.Pageblank import footer, navbar, stylesheets
import os
from seismo_helper.settings import ALLOWED_HOSTS
import base64

def openImg(path):
    with open(os.getcwd()+ path, "rb") as image_file:
        img_data = base64.b64encode(image_file.read())
        img_data = img_data.decode()
        img_data = "{}{}".format("data:image/jpg;base64, ", img_data)
        return html.Img(id="tag_id", src=img_data, alt="my image", width='100%', height='100%', className="T1", style={'margin':'0px'})


BASE_LINK = f'http://{ALLOWED_HOSTS[0]}:8000/'

app = DjangoDash('AboutPage',external_stylesheets=stylesheets)

imgA1 = openImg('\\media\\Photos_for_Front\\A1.png')
imgA2 = openImg('\\media\\Photos_for_Front\\A2.png')
imgA3 = openImg('\\media\\Photos_for_Front\\A3.png')
imgA4 = openImg('\\media\\Photos_for_Front\\A4.png')
imgA5 = openImg('\\media\\Photos_for_Front\\A5.png')
imgA6 = openImg('\\media\\Photos_for_Front\\A6.png')
imgA7 = openImg('\\media\\Photos_for_Front\\A7.png')

app.layout = html.Div([
    navbar,
    html.H1('Сервис Seismo-helper', style={'text-align': 'center'}),
    html.P(f"Seismo-helper - сервис для автоматизированного мониторинга сейсмической активности, инструкция по использованию находится в туториале."),
    html.H2('Разработчики', style={'text-align': 'center'}),
    dbc.Row([
        dbc.Col([html.Div(imgA1), html.H3("Мастов Арсений"), html.P("Fullstack Developer")], style={'text-align': 'center'}),
        dbc.Col([html.Div(imgA2), html.H3("Старченко Александр"), html.P("ML, DS Engineer")], style={'text-align': 'center'}),
        dbc.Col([html.Div(imgA3), html.H3("Ольга Демидович"), html.P("DS Engineer, UX Designer")], style={'text-align': 'center'}),
        dbc.Col([html.Div(imgA4), html.H3("Борисенко Владислав"), html.P("Frontend Developer + UI & UX Designer")], style={'text-align': 'center'}),
        dbc.Col([html.Div(imgA5), html.H3("Шинелёв Маким"), html.P("ML Engineer")], style={'text-align': 'center'}),
    ]),
    html.H2('Руководители', style={'text-align': 'center'}),
    dbc.Row([
        dbc.Col([html.Div(imgA6,style={'height': '300px', 'width': '300px', 'margin-left':'auto', 'margin-right':'auto'}), html.H2("Матвеев Алексей")], style={'text-align': 'center'}),
        dbc.Col([html.Div(imgA7,style={'height': '300px', 'width': '300px', 'margin-left':'auto', 'margin-right':'auto'}), html.H2("Бекренёв Руслан")], style={'text-align': 'center'}),
    ]),
    footer
])