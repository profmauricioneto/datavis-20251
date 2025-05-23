import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
        
np.random.seed(0)
meses = pd.date_range('2023-01-01', periods=12, freq='ME')
regioes = ['Norte', 'Sul', 'Sudeste', 'Centro-Oeste', 'Nordeste']
dados = []
        
for regiao in regioes:
    vendas = np.random.randint(10000, 50000, size=12)
    for i in range(12):
        dados.append({'Região': regiao, 'Mês': meses[i], 'Vendas': vendas[i]})

df = pd.DataFrame(dados)

# Inicializa o app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("Vendas Mensais por Região"),
    
    dcc.Dropdown(
        id='regiao-dropdown',
        options=[{'label': r, 'value': r} for r in df['Região'].unique()],
        value='Sudeste'
    ),
    
    dcc.Graph(id='grafico-vendas')
])

@app.callback(
    Output('grafico-vendas', 'figure'),
    Input('regiao-dropdown', 'value')
)
def atualizar_grafico(regiao_selecionada):
    filtrado = df[df['Região'] == regiao_selecionada]
    fig = px.line(filtrado, x='Mês', y='Vendas', title=f'Vendas na Região {regiao_selecionada}')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
