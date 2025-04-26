from dash import html, dcc
from dash.dependencies import Input, Output
from pages.trends import trends_layout
from pages.types import types_layout

# Layout da página inicial
home_layout = html.Div([
    dcc.Link('Tendências de Homicídios', href='/trends'),
    html.Br(),
    dcc.Link('Homicídios por Estado', href='/types'),
    html.Br(),
    html.Div(id='page-content')
])

# Callback para alternar entre páginas
def register_home_callbacks(app):
    @app.callback(
        Output('page-content', 'children'),
        [Input('url', 'pathname')]
    )
    def display_page(pathname):
        if pathname == '/trends':
            return trends_layout
        elif pathname == '/types':
            return types_layout
        else:
            return home_layout