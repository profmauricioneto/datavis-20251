import pandas as pd
import numpy as np
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

np.random.seed(0)

meses = pd.date_range(start="2023-01-01", periods=12, freq="ME")
regioes = ['Norte', 'Sul', 'Sudeste', 'Centro-Oeste']
produtos = ['Notebook', 'Smartphone', 'Tablet']

dados = []

for regiao in regioes:
    for produto in produtos:
        vendas = np.random.randint(500, 5000, size=12)
        for i, mes in enumerate(meses):
            dados.append({
                'Região': regiao,
                'Produto': produto,
                'Mês': mes,
                'Vendas': vendas[i]
            })

df = pd.DataFrame(dados)

# generation data

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Análise de Vendas"),

    html.Div([
        html.Label("Selecione a Região:"),
        dcc.Dropdown(
            id='dropdown-regiao',
            options=[{'label': r, 'value': r} for r in df['Região'].unique()],
            value='Sudeste'
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        html.Label("Selecione o Produto:"),
        dcc.Dropdown(
            id='dropdown-produto',
            options=[{'label': p, 'value': p} for p in df['Produto'].unique()],
            value='Notebook'
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),

    dcc.Graph(id='grafico-vendas')
])

@app.callback(
    Output('grafico-vendas', 'figure'),
    Input('dropdown-regiao', 'value'),
    Input('dropdown-produto', 'value')
)
def atualizar_grafico(regiao, produto):
    filtrado = df[(df['Região'] == regiao) & (df['Produto'] == produto)]
    fig = px.line(
        filtrado,
        x='Mês',
        y='Vendas',
        title=f'Vendas de {produto} na Região {regiao}',
        markers=True
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)