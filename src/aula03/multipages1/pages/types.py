from dash import html, dcc, Input, Output
import plotly.express as px
from utils import get_homicide_by_state, load_homicide_data

# Layout da Página de Homicídios por Estado
types_layout = html.Div([
    html.H1("Homicídios por Estado no Brasil"),
    dcc.Dropdown(
        id='state-dropdown',
        options=[{'label': estado, 'value': estado} for estado in load_homicide_data()['estado'].unique()],
        value='São Paulo'  # Valor padrão
    ),
    dcc.Graph(id='homicide-state-graph'),
    dcc.Link('Ir para Tendências de Homicídios', href='/trends'),
    html.Br(),
    dcc.Link('Voltar para a Página Inicial', href='/')
])

# Callback para atualizar o gráfico de homicídios por estado
def register_types_callbacks(app):
    @app.callback(
        Output('homicide-state-graph', 'figure'),
        [Input('state-dropdown', 'value')]
    )
    def update_homicide_state_graph(estado):
        state_data = get_homicide_by_state(estado)
        fig = px.bar(state_data, x='ano', y='homicidios', title=f'Homicídios em {estado}')
        return fig