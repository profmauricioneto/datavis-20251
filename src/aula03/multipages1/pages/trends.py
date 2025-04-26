from dash import html, dcc, Input, Output
import plotly.express as px
from utils import get_homicide_trends

# Layout da Página de Tendências
trends_layout = html.Div([
    html.H1("Tendências de Homicídios no Brasil"),
    dcc.Graph(id='homicide-trends-graph'),
    dcc.Interval(
        id='interval-component',
        interval=60 * 1000,  # Atualiza a cada 60 segundos
        n_intervals=0
    ),
    dcc.Link('Ir para Homicídios por Estado', href='/types'),
    html.Br(),
    dcc.Link('Voltar para a Página Inicial', href='/')
])

# Callback para atualizar o gráfico de tendências de homicídios
def register_trends_callbacks(app):
    @app.callback(
        Output('homicide-trends-graph', 'figure'),
        [Input('interval-component', 'n_intervals')]
    )
    def update_homicide_trends(n):
        trends = get_homicide_trends()
        fig = px.line(trends, x='ano', y='homicidios', title='Tendências de Homicídios no Brasil')
        return fig