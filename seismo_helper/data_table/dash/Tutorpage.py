from dash import html
from django_plotly_dash import DjangoDash
from data_table.dash.Pageblank import footer, navbar, stylesheets
import os
import base64
app = DjangoDash('TutorPage',external_stylesheets=stylesheets)

def openImg(path):
    with open(os.getcwd()+ path, "rb") as image_file:
        img_data = base64.b64encode(image_file.read())
        img_data = img_data.decode()
        img_data = "{}{}".format("data:image/jpg;base64, ", img_data)
        return html.Img(id="tag_id", src=img_data, alt="my image", width='100%', height='100%', className="T1", style={'margin':'0px'})

ImgT1 = openImg('\\media\\Photos_for_Front\\T1.png')
ImgT2 = openImg('\\media\\Photos_for_Front\\T2.png')

app.layout = html.Div([
    navbar,
    html.H1('Туториал по использованию сервиса'),
    html.Ul(id='my-list', children=[html.Li('Зарегистрироваться'),
            html.Li('На странице Events нужно загрузить miniseed-файлы, подождать пока сервер обработает их'),
            ImgT1,
            html.Li('На карте и в таблице под картой будут отображены обнаруженные точки сейсмической активности'),
            html.Li('Под картой также находятся графики зависимости магнитуды событий от времени и количества событий от магнитуды, красной линией на втором графики обозначен тренд основанный на линейной регрессии.'),
            ImgT2
            ]),
    footer
])
