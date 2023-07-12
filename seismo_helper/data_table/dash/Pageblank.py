import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash import html, dcc, no_update, Dash, dash_table, callback
from seismo_helper.settings import ALLOWED_HOSTS
import base64
import os

BASE_LINK = f'http://{ALLOWED_HOSTS[0]}:8000/'

# external_stylesheets_downl = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
global stylesheets
stylesheets = [dbc.themes.LUMEN]

def openImg(path):
    with open(os.getcwd()+ path, "rb") as image_file:
        img_data = base64.b64encode(image_file.read())
        img_data = img_data.decode()
        img_data = "{}{}".format("data:image/jpg;base64, ", img_data)
        return html.Img(id="tag_id", src=img_data, alt="my image", width='305px', height='100px', className="T1", style={'margin':'0px'})

bvlogo = openImg('\\media\\Photos_for_Front\\BV_logo.png')
#dbc.DropdownMenu(children=[dbc.DropdownMenuItem("More pages", header=True),dbc.DropdownMenuItem("Page 2", href="#"),dbc.DropdownMenuItem("Page 3", href="#"),],nav=True,in_navbar=True,label="More",),
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Main Page", href=BASE_LINK+'Events/', target='_blank')),
        dbc.NavItem(dbc.NavLink("Tutorial", href=BASE_LINK+'Tutorial', target='_blank')),
        dbc.NavItem(dbc.NavLink("About", href=BASE_LINK+'About/', target='_blank')),
        dbc.NavItem(dbc.NavLink("Profile", href=BASE_LINK+'Profile/', target='_blank')),
        dbc.NavItem(dbc.NavLink("Log In", href=BASE_LINK+'Login/', target='_blank')),
    ],
    brand="Seismo-helper",
    brand_href=BASE_LINK,
    color="primary",
    dark=True,
)

footer = dmc.Footer(
    height=100,
    fixed=True,
    children=[dbc.Row([
        dbc.Col(html.Div(html.A(bvlogo, href='https://konkurs.sochisirius.ru/', target='_blank'), style={'width':'305px', 'height':'100px', 'margin-left':'auto','margin-right':'auto'})),
        dbc.Col(html.Div([
            dmc.Text("Seismo-helper"),
            html.Div(html.A("Информация ", href=BASE_LINK+'About/', target="_blank", style={'color': '#000000'})),
            dmc.Text("Контакты:"),
            html.A("Телеграмм", href='https://t.me/Emil817', target="_blank", style={'color': '#000000'})
        ]))
    ])],
    style={"backgroundColor": "#137ea7"},
)