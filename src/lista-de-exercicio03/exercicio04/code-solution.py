import pandas as pd
import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

np.random.seed(42)

dias = pd.date_range(start="2023-03-01", periods=31, freq="D")
cidades = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte']
poluentes = ['PM2.5', 'PM10', 'NO2', 'SO2', 'O3']

dados = []

for cidade in cidades:
    for poluente in poluentes:
        iqa = np.random.uniform(30, 150, size=31)
        for i, dia in enumerate(dias):
            dados.append({
                'Cidade': cidade,
                'Poluente': poluente,
                'Dia': dia,
                'IQA': iqa[i]
            })
df_pol = pd.DataFrame(dados)

# ##########################

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Monitoramento da Qualidade do Ar"),

    html.Div([
        html.Label("Selecione a Cidade:"),
        dcc.Dropdown(
            id='dropdown-cidade',
            options=[{'label': c, 'value': c} for c in df_pol['Cidade'].unique()],
            value='São Paulo'
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        html.Label("Selecione o Poluente:"),
        dcc.Dropdown(
            id='dropdown-poluente',
            options=[{'label': p, 'value': p} for p in df_pol['Poluente'].unique()],
            value='PM2.5'
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),

    dcc.Graph(id='grafico-poluição')
])

@app.callback(
    Output('grafico-poluição', 'figure'),
    [Input('dropdown-cidade', 'value'),
     Input('dropdown-poluente', 'value')]
)
def atualizar_grafico(cidade, poluente):
    filtrado = df_pol[(df_pol['Cidade'] == cidade) & (df_pol['Poluente'] == poluente)]
    fig = px.scatter(
        filtrado,
        x='Dia',
        y='IQA',
        title=f'IQA de {poluente} em {cidade}',
        trendline="lowess"
    )
    # Corrige: só altera o modo dos pontos, não da linha de tendência
    for trace in fig.data:
        if trace.mode == 'markers':
            trace.mode = 'lines+markers'
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)