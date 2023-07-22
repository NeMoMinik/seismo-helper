from dash import html
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
from data_table.dash.Pageblank import footer, navbar, stylesheets
import os
from seismo_helper.settings import BASE_DIR
import base64


def openImg(path):
    with open(os.path.join(BASE_DIR, path), "rb") as image_file:
        img_data = base64.b64encode(image_file.read())
        img_data = img_data.decode()
        img_data = "{}{}".format("data:image/jpg;base64, ", img_data)
        return html.Img(id="tag_id", src=img_data, alt="my image", width='100%', height='100%', className="T1",
                        style={'margin': '0px'})


app = DjangoDash('AboutPage', external_stylesheets=stylesheets)

images = [openImg(f'media/Photos_for_Front/A{i}.png') for i in range(1, 8)]

app.layout = html.Div([
    navbar,
    html.H1('Сервис Seismo-helper', style={'text-align': 'center'}),
    html.P(
        "Seismo-helper - сервис для автоматизированного мониторинга сейсмической активности, инструкция по использованию находится в туториале."),
    html.H2('Разработчики', style={'text-align': 'center'}),
    dbc.Row([
        dbc.Col([html.Div(images[0]), html.H3("Мастов Арсений"), html.P("Fullstack Developer")],
                style={'text-align': 'center'}),
        dbc.Col([html.Div(images[1]), html.H3("Старченко Александр"), html.P("ML, DS Engineer")],
                style={'text-align': 'center'}),
        dbc.Col([html.Div(images[2]), html.H3("Ольга Демидович"), html.P("DS Engineer, UX Designer")],
                style={'text-align': 'center'}),
        dbc.Col([html.Div(images[3]), html.H3("Борисенко Владислав"), html.P("Project manager, Frontend Developer + UI & UX Designer")],
                style={'text-align': 'center'}),
        dbc.Col([html.Div(images[4]), html.H3("Шинелёв Маким"), html.P("ML Engineer")], style={'text-align': 'center'}),
    ]),
    html.H2('Руководители', style={'text-align': 'center'}),
    dbc.Row([
        dbc.Col([html.Div(images[5],
                          style={'height': '300px', 'width': '300px', 'margin-left': 'auto', 'margin-right': 'auto'}),
                 html.H2("Матвеев Алексей")], style={'text-align': 'center'}),
        dbc.Col([html.Div(images[6],
                          style={'height': '300px', 'width': '300px', 'margin-left': 'auto', 'margin-right': 'auto'}),
                 html.H2("Бекренёв Руслан")], style={'text-align': 'center'}),
    ]),
    footer
])
