import pandas as pd
import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

poluentes = ['PM2.5', 'PM10', 'NO2', 'SO2', 'O3']
cidades = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte']

dados_pol = []
for cidade in cidades:
    for poluente in poluentes:
        valores = np.random.uniform(20, 100, size=30)
        for i, val in enumerate(valores):
            dados_pol.append({
                'Cidade': cidade,
                'Poluente': poluente,
                'Dia': i + 1,
                'IQA': val
            })

df_pol = pd.DataFrame(dados_pol)

# Inicializa o app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("Índice de Qualidade do Ar por Cidade e Poluente"),
    
    dcc.Dropdown(
        id='cidade-dropdown',
        options=[{'label': c, 'value': c} for c in df_pol['Cidade'].unique()],
        value='São Paulo'
    ),
    dcc.Dropdown(
        id='poluente-dropdown',
        options=[{'label': p, 'value': p} for p in df_pol['Poluente'].unique()],
        value='PM2.5'
    ),
    dcc.Graph(id='grafico-iqa')
])

@app.callback(
    Output('grafico-iqa', 'figure'),
    [Input('cidade-dropdown', 'value'),
     Input('poluente-dropdown', 'value')]
)
def atualizar_grafico(cidade_selecionada, poluente_selecionado):
    filtrado = df_pol[(df_pol['Cidade'] == cidade_selecionada) & (df_pol['Poluente'] == poluente_selecionado)]
    fig = px.line(filtrado, x='Dia', y='IQA', title=f'IQA de {poluente_selecionado} em {cidade_selecionada}')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)