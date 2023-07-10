import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash import html, dcc, no_update, Dash, dash_table, callback
from seismo_helper.settings import ALLOWED_HOSTS

BASE_LINK = f'http://{ALLOWED_HOSTS[0]}:8000/'

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
    children=[dmc.Text("Прикол"),
              dmc.Text("Контакты:"),
              html.Div(html.A("Телеграмм", href='https://t.me/Emil817', target="_blank", style={'color': '#000000'}))
              ],
    style={"backgroundColor": "#137ea7"},
)