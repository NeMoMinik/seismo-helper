from dash import html
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
from data_table.dash.Pageblank import footer, navbar, stylesheets
import os
from seismo_helper.settings import ALLOWED_HOSTS, BASE_LINK
import base64

app = DjangoDash('StartPage',external_stylesheets=stylesheets)


with open((os.getcwd()+'\\media\\Photos_for_Front\\M1.jpg'), "rb") as image_file:
    img_data = base64.b64encode(image_file.read())
    img_data = img_data.decode()
    img_data = "{}{}".format("data:image/jpg;base64, ", img_data)
    # ...
    ImgTeam = html.Img(id="tag_id", src=img_data, alt="my image", width='100%', height='100%',
    className="Team_img", style={'margin':'0px'})

app.layout = html.Div([
    navbar,
    html.H1('SEISMO-HELPER', style={'text-align': 'center','background':'#137ea7','margin':'0px'}),
    html.Div(dbc.NavItem(dbc.NavLink("Мониторинг", href=BASE_LINK+'Events/', target='_blank', style={'color':'#000000','lineHeight': '50px', 'borderStyle': 'inset', 'margin-top':'15px', 'borderWidth': '5px', 'font-size':'28px'}),
                         style={'background':'#FFFFFF'}), style={'width': '40%', 'position': 'absolute', 'right':'30%', 'textAlign': 'center', 'height': '40px'}),
    dbc.Row([dbc.Col(ImgTeam)]),
    footer
])