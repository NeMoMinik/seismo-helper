import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash import html, dcc, no_update, Dash, dash_table, callback
BASE_LINK = 'http://127.0.0.1:8000/Events/'

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Main Page", href=BASE_LINK, target='_blank')),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="Прикол",
    brand_href="#",
    color="primary",
    dark=True,
)

footer = dmc.Footer(
    height=100,
    fixed=True,
    children=[dmc.Text("Прикол"),
    dmc.Text("Контакты:"),
    html.Div(html.A("Телеграмм", href='https://t.me/Emil817', target="_blank"))
    ],
    style={"backgroundColor": "#9c86e2"},
)