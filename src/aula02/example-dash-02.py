from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px

# Iniciar o app
app = Dash(__name__)

# Layout do app
app.layout = html.Div([
    # Título
    html.H1("Dashboard Interativo do Dataset Iris com dcc.Store", style={'textAlign': 'center'}),
    
    # Armazenar dados no dcc.Store
    dcc.Store(id='stored-data'),  # Armazena o dataset Iris
    
    # Controles
    html.Div([
        html.Label("Selecione a coluna para o eixo X:"),
        dcc.Dropdown(id='x-axis-dropdown'),
        
        html.Label("Selecione a coluna para o eixo Y:", style={'marginTop': '20px'}),
        dcc.Dropdown(id='y-axis-dropdown'),
        
        html.Label("Filtrar por espécie:", style={'marginTop': '20px'}),
        dcc.Checklist(id='species-filter', labelStyle={'display': 'block'})
    ], style={'width': '20%', 'padding': '20px', 'display': 'inline-block'}),
    
    # Gráfico e estatísticas
    html.Div([
        dcc.Graph(id='scatter-plot'),
        html.Div(id='summary-stats', style={'marginTop': '20px'})
    ], style={'width': '75%', 'display': 'inline-block', 'verticalAlign': 'top'})
])

def load_data(_):
    # Carregar o dataset Iris
    df = px.data.iris()
    
    # Criar opções para os dropdowns
    x_options = [{'label': col, 'value': col} for col in df.columns[:4]]  # Colunas numéricas
    y_options = x_options.copy()
    species_options = [{'label': sp, 'value': sp} for sp in df['species'].unique()]
    
    # Armazenar dados no dcc.Store
    return df.to_dict('records'), x_options, y_options, species_options

# Callback para atualizar o gráfico e estatísticas
@callback(
    [Output('scatter-plot', 'figure'),
     Output('summary-stats', 'children')],
    [Input('stored-data', 'data'),
     Input('x-axis-dropdown', 'value'),
     Input('y-axis-dropdown', 'value'),
     Input('species-filter', 'value')]
)
def update_graph(stored_data, x_col, y_col, selected_species):
    if stored_data is None or x_col is None or y_col is None:
        return {}, "Selecione colunas válidas."
    
    # Converter dados armazenados de volta para DataFrame
    df = pd.DataFrame(stored_data)
    
    # Filtrar dados com base nas espécies selecionadas
    filtered_df = df[df['species'].isin(selected_species)]
    
    # Criar gráfico de dispersão
    fig = px.scatter(
        filtered_df,
        x=x_col,
        y=y_col,
        color='species',  # Colorir por espécie
        title=f"{x_col} vs {y_col}",
        height=500
    )
    
    # Calcular estatísticas descritivas
    stats = filtered_df.groupby('species').agg({
        x_col: ['mean', 'std'],
        y_col: ['mean', 'std']
    }).reset_index()
    
    # Formatar tabela de estatísticas
    stats_table = html.Div([
        html.H4("Estatísticas por Espécie:"),
        html.Table([
            html.Tr([html.Th("Espécie"), html.Th(f"Média {x_col}"), html.Th(f"Desvio {x_col}"),
                    html.Th(f"Média {y_col}"), html.Th(f"Desvio {y_col}")])
        ] + [
            html.Tr([
                html.Td(sp),
                html.Td(round(row[x_col]['mean'], 2)),
                html.Td(round(row[x_col]['std'], 2)),
                html.Td(round(row[y_col]['mean'], 2)),
                html.Td(round(row[y_col]['std'], 2))
            ]) for sp, row in stats.iterrows()
        ])
    ])
    
    return fig, stats_table

# Executar o app
if __name__ == '__main__':
    app.run_server(debug=True)